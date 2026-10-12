#!/usr/bin/env python3
"""Temporal modelling of E. coli detection in Peshawar water samples.

This script implements the analysis underlying the October 2026 manuscript
revision (EW-ART-05-2026-000506). It predicts measured E. coli detection in
municipal tap and tube-well samples, not categories calculated from a WQI.

The primary estimate is based on nested rolling-origin prediction years
2016–2023. A separately described 2024 cohort was examined during previous
analyses and must not be called an untouched independent test set.

To run against the analysis-ready Excel workbook::

    python src/peshawar_ml.py --data data/WQ_Peshawar_2009-2024_analysis_ready.xlsx \
        --out runs/primary --with-smote --with-shap --permutations 200

For a reduced, non-publication software check add ``--quick`` and choose a
separate output directory. The input workbook is never written to.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, brier_score_loss,
                             confusion_matrix, roc_auc_score, roc_curve,
                             precision_recall_curve)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

SEED = 42
RF_TREES = 500  # --quick temporarily lowers this for software testing
SEASONS = ['Winter','Pre-Monsoon','Summer','Post-Monsoon']
PHYS = ['ph','temp_c','turbidity_ntu','tds_mg_l','hardness_mg_l_caco3',
        'chloride_mg_l','sulphate_mg_l','nitrate_mg_l','phosphate_mg_l',
        'ammonium_mg_l','do_mg_l','bod5_mg_l','cod_mg_l',
        'alkalinity_mg_l_caco3','toc_mg_l','tn_mg_l','uv254_cm1',
        'chla_ug_l','orp_mv']
ENC = ['src_tube_well'] + ['season_'+s for s in SEASONS[1:]]
SCENARIOS = {
    'primary_no_nitrate_or_TN': [x for x in PHYS if x not in ('nitrate_mg_l','tn_mg_l')] + ENC,
    'sensitivity_no_nitrate': [x for x in PHYS if x != 'nitrate_mg_l'] + ENC,
    'sensitivity_both_unverified': PHYS + ENC,
}
B1='B1 source only'
B2='B2 source and season'
B3='B3 LR plus 3 chemical predictors'
B4='B4 decision tree depth 3'
MODEL_NAMES=['Logistic regression','Random forest','XGBoost','SVM (RBF)', B1,B2,B3,B4]
GRID={
    'Logistic regression': [{'C': c} for c in (0.01,0.1,1.,10.)],
    'Random forest': [{'max_depth': d, 'min_samples_leaf': l} for d in (3,6,None) for l in (5,20)],
    'XGBoost': [{'max_depth': d,'n_estimators': n} for d in (2,3,4) for n in (100,300)],
    'SVM (RBF)': [{'C': c} for c in (0.1,1.,10.)],
}


def say(msg):
    print(msg,flush=True)


def write(df,out,name):
    df.to_csv(out/name,index=False,float_format='%.10g')


def make_model(name,p):
    if name == 'Logistic regression':
        return Pipeline([('scale',StandardScaler()),('model',LogisticRegression(C=p['C'],max_iter=5000,random_state=SEED))])
    if name == 'Random forest':
        return RandomForestClassifier(n_estimators=RF_TREES,max_depth=p['max_depth'],
             min_samples_leaf=p['min_samples_leaf'],random_state=SEED,n_jobs=-1)
    if name == 'XGBoost':
        return XGBClassifier(learning_rate=0.05,max_depth=p['max_depth'],
             n_estimators=p['n_estimators'],subsample=0.8,eval_metric='logloss',
             random_state=SEED,n_jobs=1,verbosity=0,tree_method='hist')
    if name == 'SVM (RBF)':
        return Pipeline([('scale',StandardScaler()),('model',SVC(C=p['C'],kernel='rbf',
             probability=True,random_state=SEED))])
    if name == B1:
        return Pipeline([('scale',StandardScaler()),('model',LogisticRegression(max_iter=5000,random_state=SEED))])
    if name == B2 or name == B3:
        return Pipeline([('scale',StandardScaler()),('model',LogisticRegression(max_iter=5000,random_state=SEED))])
    if name == B4:
        return DecisionTreeClassifier(max_depth=3,random_state=SEED)
    raise KeyError(name)


def features_for(name,main):
    if name == B1: return ['src_tube_well']
    if name == B2: return ENC
    if name == B3: return ENC+['turbidity_ntu','bod5_mg_l','ammonium_mg_l']
    return main


def predict(name,p,train,test,main):
    feats=features_for(name,main)
    mdl=make_model(name,p).fit(train[feats],train['y'].astype(int))
    return mdl.predict_proba(test[feats])[:,1]


def tune(name,train,valid,main,quick=False):
    if name not in GRID: return {},np.nan,[]
    # The quick option exercises the code but must not supply manuscript results.
    grid=(GRID[name][::2] if quick else GRID[name])
    candidates=[]
    for p in grid:
        pp=predict(name,p,train,valid,main)
        candidates.append((float(roc_auc_score(valid.y,pp)),p,pp))
    # Break ties using pre-specified grid order rather than looking ahead
    score,p,pp=max(candidates,key=lambda x:x[0])
    return p,score,pp


def sens_threshold(yy,pp,target=.8):
    a=np.sort(np.asarray(pp)[np.asarray(yy)==1])[::-1]
    if not len(a): raise ValueError('No positive samples in validation period')
    return float(a[max(0,int(np.ceil(target*len(a)))-1)])


def operating_point(y,p,threshold):
    tn,fp,fn,tp=confusion_matrix(y,np.asarray(p)>=threshold,labels=[0,1]).ravel()
    return {'TN':int(tn),'FP':int(fp),'FN':int(fn),'TP':int(tp),
            'sensitivity':float(tp/(tp+fn)) if tp+fn else np.nan,
            'specificity':float(tn/(tn+fp)) if tn+fp else np.nan,
            'PPV':float(tp/(tp+fp)) if tp+fp else np.nan,
            'NPV':float(tn/(tn+fn)) if tn+fn else np.nan}


def metrics(y,p):
    return {'AUC':float(roc_auc_score(y,p)),
            'AP':float(average_precision_score(y,p)),
            'Brier':float(brier_score_loss(y,p)),
            'prevalence':float(np.mean(y))}


def bootstrap_auc_2024(y,p,reps=2000,seed=42):
    """Within-one-year, individual-sample interval; temporal independence unverified."""
    yy=np.asarray(y); pp=np.asarray(p)
    rng=np.random.default_rng(seed); vals=[]
    for _ in range(reps):
        ii=rng.integers(len(yy),size=len(yy))
        if len(set(yy[ii]))<2: continue
        vals.append(roc_auc_score(yy[ii],pp[ii]))
    return np.percentile(vals,[2.5,97.5]).tolist() if vals else [np.nan,np.nan]


def yearblock_intervals(df, model, reps=2000, seed=42):
    """Paired year-block bootstrap; only 8 year groups, approximate sensitivity check."""
    x=df.sort_values(['year','sample_id']).reset_index(drop=True)
    yy=x.y.to_numpy(dtype=int); pp=x[model].to_numpy(dtype=float)
    bb=x[B2].to_numpy(dtype=float)
    years=sorted(x.year.unique())
    groups={int(yr):np.flatnonzero(x.year.to_numpy()==yr) for yr in years}
    rng=np.random.default_rng(seed)
    aa,dd=[],[]
    for _ in range(reps):
        draw=rng.choice(years,size=len(years),replace=True)
        ix=np.concatenate([groups[int(j)] for j in draw])
        if len(np.unique(yy[ix]))<2: continue
        aa.append(roc_auc_score(yy[ix],pp[ix]))
        dd.append(aa[-1]-roc_auc_score(yy[ix],bb[ix]))
    return (np.percentile(aa,[2.5,97.5]).tolist(),
            np.percentile(dd,[2.5,97.5]).tolist())


def data_audit(raw,ml,out,input_path):
    counts=[('total_rows',len(raw),'not an error count'),
            ('missing_cells',int(raw.isna().sum().sum()),''),
            ('duplicate_sample_ids',int(raw.sample_id.duplicated().sum()),''),
            ('ml_rows_tap_and_tube_well',len(ml),''),
            ('Ecoli_positive_ml',int(ml.y.sum()),''),
            ('COD_censored_total',int(raw.cod_below_lod.sum()),''),
            ('DO_supersaturated_total',int(raw.qc_do_supersaturated.sum()),''),
            ('TN_below_inorganic_flag_total',int(raw.qc_tn_below_inorganic_n.sum()),''),
            ('DO_or_TN_flag_ml',int(((ml.qc_do_supersaturated==1)|(ml.qc_tn_below_inorganic_n==1)).sum()),''),
            ('TN_below_as_reported_nitrate_total',int((raw.tn_mg_l<raw.nitrate_mg_l).sum()),'Different reported analytes: nitrate as NO3 ion, TN as N; comparison invalid'),
            ('TN_below_NO3_as_N_if_nitrate_ion_total',int((raw.tn_mg_l<raw.nitrate_mg_l/4.4268).sum()),'Screening comparison only; does not establish a laboratory QA/QC failure'),
            ('TN_below_as_reported_nitrate_ml',int((ml.tn_mg_l<ml.nitrate_mg_l).sum()),'Comparison invalid: nitrate as NO3 ion, TN as N'),
            ('TN_below_NO3_as_N_if_nitrate_ion_ml',int((ml.tn_mg_l<ml.nitrate_mg_l/4.4268).sum()),'Screening comparison only; laboratory confirmation of QA/QC needed'),
            ('TDS_to_EC_outside_typical_band_total',int(((raw.tds_mg_l/raw.ec_us_cm<.55)|(raw.tds_mg_l/raw.ec_us_cm>.75)).sum()),''),
            ('Temperature_exactly_25_total',int((raw.temp_c==25).sum()),'check with laboratory')]
    write(pd.DataFrame(counts,columns=['check','value','caution']),out,'01_data_audit.csv')
    write(ml.groupby(['year','source'],as_index=False).agg(n=('y','size'),positive=('y','sum')),
          out,'01_ml_counts_year_source.csv')
    input_hash=hashlib.sha256(input_path.read_bytes()).hexdigest()
    (out/'01_input_sha256.txt').write_text(f'{input_path.name}  {input_hash}\n',encoding='utf-8')


def prepare(raw):
    needed=['sample_id','year','source','season','ecoli_cfu_100ml','cod_below_lod',
            'qc_do_supersaturated','qc_tn_below_inorganic_n']+PHYS
    missing=[x for x in needed if x not in raw.columns]
    if missing: raise ValueError('Dataset is missing columns: '+', '.join(missing))
    if raw.sample_id.duplicated().any():raise ValueError('Duplicate sample IDs detected')
    d=raw.copy()
    d['year']=pd.to_numeric(d.year,errors='raise').astype(int)
    if not set(d.season.unique()).issubset(set(SEASONS)):
        raise ValueError('Unrecognised season names: '+str(set(d.season.unique())-set(SEASONS)))
    for c in PHYS:
        d[c]=pd.to_numeric(d[c],errors='raise')
    # The COD replacement only affects the in-memory model dataset; raw Excel is unmodified
    d['cod_mg_l']=d['cod_mg_l'].astype(float)
    d.loc[d.cod_below_lod==1,'cod_mg_l']=2/np.sqrt(2)
    d=d[d.source.isin(['tap','tube_well'])].copy()
    d['y']=(d.ecoli_cfu_100ml>0).astype(int)
    d['src_tube_well']=(d.source=='tube_well').astype(int)
    for s in SEASONS[1:]: d['season_'+s]=(d.season==s).astype(int)
    for c in SCENARIOS['sensitivity_both_unverified']:
        if d[c].isna().any():raise ValueError('Predictor '+c+' contains missing data; do not silently impute')
    d['sample_id']=d['sample_id'].astype(str)
    return d


def plot_results(predictions, out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    images=out/'figures';images.mkdir(exist_ok=True)
    for period, data in [('rolling_2016_2023',predictions[predictions.year<2024]),
                         ('test_2024',predictions[predictions.year==2024])]:
        fig,ax=plt.subplots(figsize=(7,5))
        for n in ['Logistic regression','Random forest','XGBoost','SVM (RBF)',B2]:
            fpr,tpr,_=roc_curve(data.y,data[n])
            ax.plot(fpr,tpr,label=f'{n} (AUC {roc_auc_score(data.y,data[n]):.3f})')
        ax.plot([0,1],[0,1],linestyle=':',color='gray')
        ax.set(xlabel='False positive rate',ylabel='True positive rate',title=f'ROC: {period}')
        ax.legend(fontsize=8);fig.tight_layout()
        fig.savefig(images/f'roc_{period}.png',dpi=300);plt.close(fig)
    # Primary rolling Brier calibration curve, descriptive not a recalibration fit
    fig,ax=plt.subplots(figsize=(6,5))
    dat=predictions[predictions.year<2024]
    for n in ['Logistic regression','Random forest','XGBoost',B2]:
        bins=pd.qcut(dat[n],q=8,duplicates='drop')
        cal=dat.groupby(bins,observed=True).agg(actual=('y','mean'),pred=(n,'mean'))
        ax.plot(cal.pred,cal.actual,'o-',label=n,markersize=3)
    ax.plot([0,1],[0,1],':',color='gray')
    ax.set(xlabel='Mean predicted probability',ylabel='Observed positive rate',title='Rolling calibration (descriptive)')
    ax.legend(fontsize=8);fig.tight_layout()
    fig.savefig(images/'calibration_rolling.png',dpi=300);plt.close(fig)


def smotenc_analysis(ml, feats, params, threshold_target):
    """Secondary test, keeping season a *single* categorical variable in SMOTENC."""
    from imblearn.over_sampling import SMOTENC
    num=[f for f in feats if f not in ENC]
    cat=['src_tube_well','season_code']
    temp=ml.copy()
    temp['season_code']=pd.Categorical(temp.season,categories=SEASONS).codes
    if (temp.season_code<0).any(): raise ValueError('Unknown season in SMOTE input')
    rawcols=num+cat
    def balanced_fit(train,name,par):
        sm=SMOTENC(categorical_features=[len(num),len(num)+1],random_state=SEED)
        xx,yy=sm.fit_resample(train[rawcols],train.y)
        bb=pd.DataFrame(np.asarray(xx),columns=rawcols)
        for f in num:bb[f]=pd.to_numeric(bb[f])
        bb['src_tube_well']=np.rint(bb.src_tube_well).astype(int)
        seas=np.rint(bb.season_code).astype(int)
        if not np.isin(seas,np.arange(4)).all(): raise ValueError('Invalid SMOTE-NC season')
        for j,s in enumerate(SEASONS[1:],start=1):bb['season_'+s]=(seas==j).astype(int)
        mdl=make_model(name,par).fit(bb[feats],yy)
        return mdl
    train=temp[temp.year<=2021];valid=temp[temp.year.isin([2022,2023])]
    alltrain=temp[temp.year<=2023];test=temp[temp.year==2024]
    rows=[]
    for name in ['Logistic regression','Random forest','XGBoost']:
        p=params[name]
        m0=balanced_fit(train,name,p)
        threshold=sens_threshold(valid.y,m0.predict_proba(valid[feats])[:,1],threshold_target)
        m1=balanced_fit(alltrain,name,p)
        pp=m1.predict_proba(test[feats])[:,1]
        rec={'model':name,'test_n':len(test),'threshold':threshold,**metrics(test.y,pp),
             **operating_point(test.y,pp,threshold),
             'note':'exploratory training-only SMOTE-NC; fixed hyperparameters from 2024 inner tuning'}
        rows.append(rec)
    return pd.DataFrame(rows)


def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument('--data',required=True,type=Path,help='Original WQ_Peshawar_2009-2024_analysis_ready.xlsx')
    ap.add_argument('--out',type=Path,default=Path('wq_reanalysis_results'))
    ap.add_argument('--quick',action='store_true',help='Non-publication smoke test: smaller hyperparameter grid, trees and resampling')
    ap.add_argument('--with-smote',action='store_true',help='Extra SMOTE-NC sensitivity')
    ap.add_argument('--with-shap',action='store_true',help='Extra training-only XGBoost SHAP explanation')
    ap.add_argument('--permutations',type=int,default=200,help='Global label permutations: descriptive null only; 0 disables')
    args=ap.parse_args()
    global RF_TREES
    RF_TREES = 80 if args.quick else 500
    if not args.data.is_file():ap.error(f'Dataset does not exist: {args.data}')
    if args.permutations<0:ap.error('--permutations must be non-negative')
    out=args.out.resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError('Output directory must be empty to prevent mixing runs: '+str(out))
    out.mkdir(parents=True,exist_ok=True)
    (out/'figures').mkdir(exist_ok=True)
    reps=50 if args.quick else 2000
    perms=min(8,args.permutations) if args.quick else args.permutations
    say('Reading: '+str(args.data))
    raw=pd.read_excel(args.data,sheet_name='analysis_data')
    ml=prepare(raw)
    assert len(raw)==1800 and len(ml)==1200, 'Unexpected sample count, investigate before proceeding.'
    assert len(ml[ml.year==2024])==76, '2024 cohort differs from previously reported data'
    data_audit(raw,ml,out,args.data)
    versions={'Python':platform.python_version(),'pandas':pd.__version__,
             'numpy':np.__version__,'scikit-learn':__import__('sklearn').__version__,
             'xgboost':__import__('xgboost').__version__,'seed':SEED,
             'bootstrap_resamples':reps,'label_permutations':perms,'quick_nonpublication':bool(args.quick)}
    (out/'00_versions.json').write_text(json.dumps(versions,indent=2),encoding='utf-8')
    primary=SCENARIOS['primary_no_nitrate_or_TN']
    tune_rows=[]; fold_results=[]; pred_records=[]
    outer_years=list(range(2016,2025))
    say('Nested temporal model tuning and predictions for years 2016-2024...')
    for yr in outer_years:
        inner_tr=ml[ml.year<yr-2]
        inner_va=ml[(ml.year>=yr-2)&(ml.year<yr)]
        outer_tr=ml[ml.year<yr]
        outer_te=ml[ml.year==yr]
        if not len(inner_tr) or not len(inner_va) or not len(outer_te):raise RuntimeError(f'Empty fold for {yr}')
        if inner_tr.year.max()>=inner_va.year.min() or outer_tr.year.max()>=yr:
            raise RuntimeError('Temporal leakage detected')
        rec={'sample_id':outer_te.sample_id.to_numpy(),'year':outer_te.year.to_numpy(),
             'source':outer_te.source.to_numpy(),'season':outer_te.season.to_numpy(),
             'y':outer_te.y.to_numpy()}
        # thresholds come from the past-only validation block, not the predicted year
        for n in MODEL_NAMES:
            if n in GRID:
                prm,v_auc,va_pred=tune(n,inner_tr,inner_va,primary,args.quick)
            else:
                prm={};va_pred=predict(n,prm,inner_tr,inner_va,primary)
                v_auc=roc_auc_score(inner_va.y,va_pred)
            pred=predict(n,prm,outer_tr,outer_te,primary)
            thr=sens_threshold(inner_va.y,va_pred,0.80)
            rec[n]=pred
            op=operating_point(outer_te.y,pred,thr)
            row={'year':yr,'period':'2024 previously examined holdout' if yr==2024 else 'nested rolling 2016-2023',
                 'model':n,'n_year':len(outer_te),'train_until':yr-1,'inner_train_until':yr-3,
                 'inner_validation_years':f'{yr-2}-{yr-1}',
                 'selected_hyperparameters':json.dumps(prm,sort_keys=True),
                 'inner_validation_AUC':v_auc,'validation_80pct_sensitivity_threshold':thr,
                 **metrics(outer_te.y,pred),**op}
            fold_results.append(row)
            tune_rows.append({'prediction_year':yr,'model':n,'hyperparameters':json.dumps(prm,sort_keys=True),
                              'inner_train_end_year':yr-3,'inner_validation_start':yr-2,
                              'inner_validation_end':yr-1,'validation_AUC':v_auc,'threshold':thr})
        pred_records.append(pd.DataFrame(rec))
        say(f'  {yr}: {len(outer_te)} held-out samples; tuning ends by {yr-1}')
    pred=pd.concat(pred_records,ignore_index=True)
    assert len(pred)==660 and len(pred[pred.year<2024])==584
    assert pred.sample_id.nunique()==len(pred)
    write(pred,out,'03_primary_out_of_time_predictions.csv')
    write(pd.DataFrame(tune_rows),out,'02_fold_hyperparameters.csv')
    write(pd.DataFrame(fold_results),out,'04_by_year_model_performance.csv')
    roll=pred[pred.year<2024]
    test=pred[pred.year==2024]
    aggregate=[]
    for n in MODEL_NAMES:
        for label,subset in [('rolling_2016_2023',roll),('previously_inspected_2024',test)]:
            r={'period':label,'model':n,'n':len(subset),**metrics(subset.y,subset[n])}
            if label=='rolling_2016_2023':
                ci,delta_ci=yearblock_intervals(roll,n,reps,SEED+9)
                r.update({'AUC_CI95_lower':ci[0],'AUC_CI95_upper':ci[1],
                    'delta_auc_vs_B2':metrics(subset.y,subset[n])['AUC']-metrics(subset.y,subset[B2])['AUC'],
                    'delta_CI95_lower':delta_ci[0],'delta_CI95_upper':delta_ci[1],
                    'CI_method':'paired year-block bootstrap; only 8 years'})
            else:
                ci=bootstrap_auc_2024(test.y,test[n],reps,SEED+10)
                r.update({'AUC_CI95_lower':ci[0],'AUC_CI95_upper':ci[1],
                    'CI_method':'individual record bootstrap; within 2024; independence unverified'})
            aggregate.append(r)
    write(pd.DataFrame(aggregate),out,'05_main_aggregated_results.csv')
    # Exploratory 2024 nitrogen feature scenarios; same past-only model tuning.
    # Nitrate is reported as NO3 ion (not nitrate-N); TN is expressed as N.
    # Keep the scenario identifiers unchanged to match the deposited audit outputs.
    say('Evaluating nitrogen feature-sensitivity scenarios...')
    scenario_rows=[]; ablation_predictions=[]
    for scenario,feats in SCENARIOS.items():
        train=ml[ml.year<=2021];val=ml[ml.year.isin([2022,2023])]
        hist=ml[ml.year<=2023];te=ml[ml.year==2024]
        for n in MODEL_NAMES:
            p,va_auc,vp=tune(n,train,val,feats,args.quick) if n in GRID else ({},np.nan,None)
            if vp is None:vp=predict(n,p,train,val,feats);va_auc=roc_auc_score(val.y,vp)
            th=sens_threshold(val.y,vp,.80)
            pp=predict(n,p,hist,te,feats)
            scenario_rows.append({'scenario':scenario,'model':n,'n_predictors':len(features_for(n,feats)),
                 '2024_test_n':len(te),'hyperparameters':json.dumps(p,sort_keys=True),
                 'validation_AUC':va_auc,'threshold_80pct_val':th,
                 **metrics(te.y,pp),**operating_point(te.y,pp,th),
                 'warning':'2024 has been inspected; scenario selection is exploratory'})
            ablation_predictions.extend([{'scenario':scenario,'model':n,'sample_id':sid,
                'year':2024,'y':int(yy),'probability':float(pr)}
                for sid,yy,pr in zip(te.sample_id,te.y,pp)])
        say('  2024 feature sensitivity completed: '+scenario)
    write(pd.DataFrame(scenario_rows),out,'06_2024_nitrogen_scenario_metrics.csv')
    write(pd.DataFrame(ablation_predictions),out,'06_2024_nitrogen_scenario_predictions.csv')
    # Legacy QC-flag exclusion, rerun with past-only tuning for B2, LR and XGBoost.
    # The TN-derived QC flag requires reassessment now that nitrate units are
    # confirmed as NO3 ion. Results are exploratory and are not a QA/QC verdict.
    say('Re-evaluating QC exclusions with nested past-only tuning...')
    keep=ml[(ml.qc_do_supersaturated==0)&(ml.qc_tn_below_inorganic_n==0)]
    qc_rows=[];qc_preds=[]
    for yr in range(2016,2024):
        subtr=keep[keep.year<yr-2];va=keep[(keep.year>=yr-2)&(keep.year<yr)]
        his=keep[keep.year<yr];te=keep[keep.year==yr]
        for n in [B2,'Logistic regression','XGBoost']:
            p,_,_=tune(n,subtr,va,primary,args.quick)
            pp=predict(n,p,his,te,primary)
            qc_preds.extend([{'year':yr,'sample_id':sid,'y':int(y),'model':n,'probability':float(pr)}
                             for sid,y,pr in zip(te.sample_id,te.y,pp)])
    qc_d=pd.DataFrame(qc_preds)
    for n,g in qc_d.groupby('model'):
        qc_rows.append({'model':n,'n':len(g),**metrics(g.y,g.probability),
                        'caution':'Exploratory cohort: historical TN QC flag may be invalid after nitrate unit clarification'})
    write(qc_d,out,'07_qc_exclusion_rolling_predictions.csv')
    write(pd.DataFrame(qc_rows),out,'07_qc_exclusion_rolling_summary.csv')
    flagged=ml.assign(flagged=((ml.qc_do_supersaturated==1)|(ml.qc_tn_below_inorganic_n==1)).astype(int))
    qc_counts=flagged.groupby(['year','source','y'],as_index=False).agg(excluded=('flagged','sum'),total=('flagged','size'))
    write(qc_counts,out,'07_qc_exclusion_counts_by_year_source_outcome.csv')
    if args.with_smote:
        say('Secondary SMOTE-NC (season encoded as one categorical feature)...')
        final_params={r['model']:json.loads(r['hyperparameters']) for r in tune_rows if r['prediction_year']==2024}
        smot=smotenc_analysis(ml,primary,final_params,.80)
        write(smot,out,'08_smote_NC_2024_sensitivity.csv')
    if perms:
        say(f'Global-label permutation diagnostic ({perms} permutations); NOT a test of superiority to B2...')
        # XGBoost on primary no-nitrate/TN predictors; fixed 2024 fold parameters.
        prs={r['model']:json.loads(r['hyperparameters']) for r in tune_rows if r['prediction_year']==2024}
        p=prs['XGBoost'];hist=ml[ml.year<=2023];te=ml[ml.year==2024]
        observed=roc_auc_score(te.y,predict('XGBoost',p,hist,te,primary))
        generator=np.random.default_rng(SEED)
        null=[]
        for i in range(perms):
            shuffled=hist.copy();shuffled['y']=generator.permutation(shuffled.y.to_numpy())
            null.append(float(roc_auc_score(te.y,predict('XGBoost',p,shuffled,te,primary))))
        write(pd.DataFrame({'permutation_number':range(1,perms+1),'test_AUC_under_global_label_shuffle':null}),out,'08_global_label_permutation_null.csv')
        (out/'08_global_label_permutation_summary.json').write_text(json.dumps({
            'observed_AUC':observed,'null_AUC_mean':float(np.mean(null)),
            'null_AUC_95th_percentile':float(np.percentile(null,95)),
            'one_sided_empirical_p':float((1+sum(x>=observed for x in null))/(perms+1)),
            'warning':'Global label shuffle tests no label-feature association. It does NOT test incremental benefit over source and season.'},indent=2),encoding='utf-8')
    if args.with_shap:
        try:
            import shap
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            prs={r['model']:json.loads(r['hyperparameters']) for r in tune_rows if r['prediction_year']==2024}
            t=ml[ml.year<=2023]
            model=make_model('XGBoost',prs['XGBoost']).fit(t[primary],t.y)
            values=shap.TreeExplainer(model).shap_values(t[primary])
            write(pd.DataFrame({'feature':primary,'mean_absolute_SHAP':np.abs(values).mean(axis=0)})
                  .sort_values('mean_absolute_SHAP',ascending=False),out,'08_shap_training_only.csv')
            shap.summary_plot(values,t[primary],show=False,max_display=15)
            plt.tight_layout();plt.savefig(out/'figures'/'shap_XGBoost_train_only.png',dpi=300);plt.close()
        except Exception as exc:
            (out/'08_shap_error.txt').write_text(repr(exc),encoding='utf-8')
            say('SHAP step not available, saved explanation; core models unaffected: '+repr(exc))
    plot_results(pred,out)
    readme='''# Water-quality ML modelling notes — verify before citation

Input Excel workbook is READ ONLY. Audit retains original values. A modelling-only COD
LOD/sqrt(2) replacement follows the prior pipeline; laboratory LOD requires confirmation.

PRIMARY 21 encoded features: 17 physicochemical features (EXCLUDING nitrate and total
nitrogen), plus source and three season indicators. Pesticide/herbicide totals are also
excluded because constituent compounds remain unspecified.

Nested rolling 2016-2023: Each predicted year Y is NEVER used to tune or train its own
model. Inner training years <Y-2; validation Y-2 and Y-1; after tuning, refit on all
pre-Y data. B2 baseline is source and season. Thresholds target >=80% sensitivity
ON THE INNER VALIDATION YEARS, NOT necessarily on the prediction year.

2024 model performance: Model tuning on <=2021 / 2022-2023 validation, fit on <=2023,
2024 prediction. However 2024 test has been inspected repeatedly in past work, so it
is NOT an untouched external test. Do NOT claim independent replication. Rolling
2016-2023 and 2024 are DISJOINT in the headline table; no double counting.

UNCERTAINTY: year-block bootstrap uses only 8 years and is exploratory.
2024 individual record bootstrap may understate uncertainty due to site/temporal
clustering and the small sample. Negative paired AUC differences show no superiority;
CIs crossing zero do NOT prove equivalence.

ADDITIONAL 2024 nitrogen-feature scenarios are EXPLORATORY. The laboratory has
confirmed that nitrate is expressed as NO3 ion (not NO3-N) and TN as N; the
ammonium reporting basis and legacy TN QA/QC flag require review. WQI, nitrate
exceedance, CF/PLI and other chemical-index conclusions are outside this script.

The global-label-permutation diagnostic is NOT a paired statistical superiority test
against B2. QC-exclusion sensitivity changes the evaluation cohort, and the
original TN QC flags must be reassessed following the nitrate-unit clarification.

Public release requires co-author approval of data rights and provenance, laboratory
QA/QC review, and final checks against the manuscript and Supplementary Information.

--quick is ONLY a software check: its hyperparameter search and bootstrap are reduced.
Never publish quick-mode results.
'''
    (out/'README_INTERPRETATION.txt').write_text(readme,encoding='utf-8')
    zip_path=out.parent/(out.name+'.zip')
    with ZipFile(zip_path,'w',ZIP_DEFLATED) as z:
        for f in sorted(out.rglob('*')):
            if f.is_file():z.write(f,arcname=f.relative_to(out))
    say('DONE. Results folder: '+str(out))
    say('ZIP FOR SHARING: '+str(zip_path))
    summary=pd.DataFrame(aggregate)
    say(summary[['period','model','n','AUC','AP','Brier']].to_string(index=False,float_format=lambda x:f'{x:.3f}'))

if __name__=='__main__':
    try: main()
    except Exception as exc:
        say('STOPPED WITH ERROR: '+str(exc))
        raise
