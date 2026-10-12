#!/usr/bin/env python3
"""Render four supporting plots from frozen ML result tables.

No models are refitted and no source records or labels are changed.
This is a reproducible graphical rendering, not a byte-for-byte copy
of the original 9 October 2026 PNG illustrations.

Run at repository root:
    python src/plot_archived_ml_figures.py
"""
from __future__ import annotations
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import roc_auc_score, roc_curve

MODELS = ("Logistic regression", "Random forest", "XGBoost",
          "SVM (RBF)", "B2 source and season")


def display_name(model):
    return "Source + season baseline" if model == "B2 source and season" else model


def validate(y, scores):
    if set(y.unique()) != {0, 1}:
        raise ValueError("Expected both E. coli outcome classes")
    if scores.isna().any() or not scores.between(0, 1).all():
        raise ValueError("Predictions must be finite probabilities in [0, 1]")


def plot_roc(y, predictions, title, destination):
    fig, ax = plt.subplots(figsize=(8.7, 6.5))
    for model in MODELS:
        scores = predictions[model]
        validate(y, scores)
        x, z, _ = roc_curve(y, scores)
        auc = roc_auc_score(y, scores)
        ax.plot(x, z, linewidth=1.8, label=f"{display_name(model)}: AUC {auc:.3f}")
    ax.plot([0, 1], [0, 1], "--", label="Chance", linewidth=1)
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="False-positive rate",
           ylabel="True-positive rate", title=title)
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(destination, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_calibration(y, predictions, destination):
    fig, ax = plt.subplots(figsize=(8.2, 6.7))
    ax.plot([0, 1], [0, 1], "--", label="Perfect calibration", linewidth=1)
    for model in MODELS:
        scores = predictions[model]
        validate(y, scores)
        observed, predicted = calibration_curve(
            y, scores, n_bins=8, strategy="quantile")
        ax.plot(predicted, observed, marker="o", markersize=4, linewidth=1.6,
                label=display_name(model))
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="Mean predicted probability",
           ylabel="Observed detection frequency",
           title="E. coli detection: out-of-time calibration, 2016–2023")
    ax.legend(loc="upper left", fontsize=8.5)
    ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(destination, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_shap(summary, destination):
    if not {"feature", "mean_absolute_SHAP"}.issubset(summary.columns):
        raise ValueError("Missing SHAP-summary columns")
    ranked = summary.sort_values("mean_absolute_SHAP",
                                 ascending=False).head(15).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9.1, 7.6))
    ax.barh(ranked["feature"], ranked["mean_absolute_SHAP"])
    ax.set(xlabel="Mean absolute SHAP value",
           title="XGBoost global feature importance\nTraining years only (2009–2023)")
    ax.grid(axis="x", alpha=0.16)
    fig.tight_layout()
    fig.savefig(destination, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, default=Path("results/figures"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    rolling = pd.read_csv(args.results / "03_primary_out_of_time_predictions.csv")
    rolling = rolling.loc[rolling["year"].between(2016, 2023)].copy()
    if len(rolling) != 584:
        raise ValueError("Unexpected 2016–2023 count; check archived predictions")
    y = rolling["y"].astype(int)
    plot_roc(y, rolling, "E. coli detection: rolling-origin validation, 2016–2023",
             args.output / "roc_rolling_2016_2023.png")
    plot_calibration(y, rolling, args.output / "calibration_rolling.png")

    long = pd.read_csv(args.results / "06_2024_nitrogen_scenario_predictions.csv")
    long = long.loc[long["scenario"] == "primary_no_nitrate_or_TN"]
    wide = long.pivot(index="sample_id", columns="model", values="probability")
    outcome = long.groupby("sample_id")["y"].first().reindex(wide.index).astype(int)
    if len(outcome) != 76 or outcome.sum() != 53:
        raise ValueError("Unexpected count or prevalence for 2024")
    plot_roc(outcome, wide, "E. coli detection: separately examined 2024 data",
             args.output / "roc_test_2024.png")
    plot_shap(pd.read_csv(args.results / "08_shap_training_only.csv"),
              args.output / "shap_XGBoost_train_only.png")
    print(f"Created four PNG figures in {args.output}")


if __name__ == "__main__":
    main()
