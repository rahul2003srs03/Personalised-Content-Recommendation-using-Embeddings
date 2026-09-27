"""
Figure generator for the project presentation.

Builds every chart and diagram embedded in
docs/Personalized_Content_Recommendation_Presentation.pptx.

Every number plotted here is read live from the project's own artefacts
(data/evaluation_report.json, data/sentiment_metrics.json,
data/processed_news.csv, data/embeddings.npy) - nothing is hard-coded.

Output: docs/assets/*.png

Usage:  python docs/generate_figures.py
"""
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# --------------------------------------------------------------------------- #
# Palette - kept in step with the C-DAC deck template (blue accents).
# --------------------------------------------------------------------------- #
NAVY = "#1F4E79"
BLUE = "#2E75B6"
LIGHT_BLUE = "#9DC3E6"
GREY = "#7F7F7F"
LIGHT_GREY = "#D9D9D9"
GREEN = "#2E9E5B"
AMBER = "#C9A227"
RED = "#C0392B"
SENTIMENT_COLOURS = {"Positive": GREEN, "Neutral": "#95A5A6", "Negative": RED}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": "#BFBFBF",
    "axes.labelcolor": "#333333",
    "text.color": "#333333",
    "xtick.color": "#555555",
    "ytick.color": "#555555",
    "axes.titlecolor": NAVY,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


# --------------------------------------------------------------------------- #
# Fact loading
# --------------------------------------------------------------------------- #
def load_facts() -> dict:
    """Read every figure this script plots straight out of the repo artefacts."""
    f: dict = {}

    with open(os.path.join(DATA_DIR, "evaluation_report.json"), encoding="utf-8") as fh:
        f["report"] = json.load(fh)

    metrics_path = os.path.join(DATA_DIR, "sentiment_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, encoding="utf-8") as fh:
            f["sentiment"] = json.load(fh)
    else:
        f["sentiment"] = f["report"]["sentiment"]

    emb = np.load(os.path.join(DATA_DIR, "embeddings.npy"), mmap_mode="r")
    f["emb_rows"], f["emb_dim"] = int(emb.shape[0]), int(emb.shape[1])
    f["emb_dtype"] = str(emb.dtype)
    f["emb_mb"] = round(
        os.path.getsize(os.path.join(DATA_DIR, "embeddings.npy")) / (1024 * 1024), 1
    )

    df = pd.read_csv(
        os.path.join(DATA_DIR, "processed_news.csv"), usecols=["category", "sentiment"]
    )
    f["articles"] = int(len(df))
    f["categories"] = int(df["category"].nunique())
    f["sentiment_mix"] = df["sentiment"].value_counts().to_dict()
    f["top_categories"] = df["category"].value_counts().head(10).to_dict()

    users = pd.read_csv(os.path.join(DATA_DIR, "user_simulation.csv"))
    f["users"] = int(len(users))
    return f


def _save(fig, name: str, dpi: int = 200) -> str:
    os.makedirs(ASSETS_DIR, exist_ok=True)
    path = os.path.join(ASSETS_DIR, name)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(f"  wrote {os.path.relpath(path, PROJECT_ROOT)}")
    return path


def _strip(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        if side not in keep:
            ax.spines[side].set_visible(False)


# --------------------------------------------------------------------------- #
# 1. System architecture / data-flow diagram
# --------------------------------------------------------------------------- #
def fig_architecture(f: dict) -> str:
    fig, ax = plt.subplots(figsize=(12.4, 5.0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 42)
    ax.axis("off")

    def box(x, y, w, h, title, sub, fill, edge, tc="white", fs=9.5, sfs=7.8):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.35,rounding_size=1.1",
            linewidth=1.4, facecolor=fill, edgecolor=edge, zorder=3))
        ax.text(x + w / 2, y + h * 0.62, title, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=tc, zorder=4)
        if sub:
            ax.text(x + w / 2, y + h * 0.24, sub, ha="center", va="center",
                    fontsize=sfs, color=tc, zorder=4)

    def arrow(x1, y1, x2, y2, colour=NAVY, style="-|>"):
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle=style, mutation_scale=13,
            linewidth=1.5, color=colour, shrinkA=1, shrinkB=1, zorder=2))

    # --- Offline pipeline band ------------------------------------------- #
    ax.add_patch(FancyBboxPatch(
        (1.0, 21.0), 98.0, 19.5, boxstyle="round,pad=0.4,rounding_size=1.2",
        facecolor="#F4F8FC", edgecolor=LIGHT_BLUE, linewidth=1.1, zorder=0))
    ax.text(3.0, 38.4, "OFFLINE PIPELINE  ·  python main.py  (run once)",
            fontsize=9.5, fontweight="bold", color=NAVY, zorder=1)

    box(2.5, 26.0, 15.0, 8.4, "Raw dataset",
        f"archive/data.csv\nKaggle Global News", "#FFFFFF", GREY, tc="#333333")
    box(21.0, 26.0, 15.5, 8.4, "1  Preprocessing",
        "clean · de-duplicate\nsrc/preprocessing.py", BLUE, NAVY)
    box(40.0, 26.0, 16.5, 8.4, "2  Sentiment tagging",
        "TF-IDF + LogisticReg\nsrc/sentiment_analysis.py", BLUE, NAVY)
    box(60.0, 26.0, 15.5, 8.4, "3  User simulation",
        f"{f['users']:,} readers · 3-10 items\nsrc/user_simulator.py", BLUE, NAVY)
    box(79.0, 26.0, 19.5, 8.4, "4  Embedding generation",
        f"all-MiniLM-L6-v2 · {f['emb_dim']}-dim\nsrc/recommendation.py",
        BLUE, NAVY, fs=9.2)

    for x in (17.5, 36.5, 56.5, 75.5):
        arrow(x, 30.2, x + 3.5, 30.2)

    # --- Artefact store --------------------------------------------------- #
    ax.text(2.5, 14.0, "ARTEFACT\nSTORE  ·  data/", fontsize=9.5,
            fontweight="bold", color=NAVY, va="center", linespacing=1.5)
    box(15.0, 11.0, 21.0, 6.4, "processed_news.csv",
        f"{f['articles']:,} articles · {f['categories']} categories", "#FFF6E5", AMBER, tc="#5C4200")
    box(39.0, 11.0, 20.0, 6.4, "user_simulation.csv",
        f"{f['users']:,} reading histories", "#FFF6E5", AMBER, tc="#5C4200")
    box(62.0, 11.0, 21.0, 6.4, "embeddings.npy",
        f"{f['emb_rows']:,} x {f['emb_dim']} {f['emb_dtype']} · {f['emb_mb']} MB",
        "#FFF6E5", AMBER, tc="#5C4200")

    arrow(25.0, 26.0, 25.0, 17.7)
    arrow(67.5, 26.0, 49.0, 17.7)
    arrow(88.0, 26.0, 72.5, 17.7)

    # --- Serving layer ---------------------------------------------------- #
    ax.text(3.0, 7.4, "ONLINE SERVING LAYER", fontsize=9.5,
            fontweight="bold", color=NAVY)
    box(15.0, 0.6, 22.0, 6.0, "Recommendation Engine",
        "mean-pooled profile → cosine rank", NAVY, NAVY)
    box(41.0, 0.6, 20.0, 6.0, "FastAPI REST service",
        "127.0.0.1:8000 · 7 routes + /docs", NAVY, NAVY)
    box(65.0, 0.6, 20.0, 6.0, "Streamlit dashboard",
        "localhost:8501 · 4 tabs", NAVY, NAVY)

    arrow(25.5, 11.0, 25.5, 6.9)
    arrow(49.0, 11.0, 49.5, 6.9)
    arrow(72.5, 11.0, 73.0, 6.9)
    arrow(37.0, 3.6, 41.0, 3.6)
    arrow(61.0, 3.6, 65.0, 3.6)

    # Offline evaluation harness (reads the same artefacts, writes the report).
    box(85.5, 0.6, 13.0, 6.0, "evaluate.py",
        "quality metrics →\nevaluation_report.json",
        "#FFFFFF", NAVY, tc=NAVY, fs=9.5, sfs=7.4)
    arrow(83.0, 12.0, 90.0, 6.9, colour=GREY)

    return _save(fig, "fig_architecture.png")


# --------------------------------------------------------------------------- #
# 2. Corpus profile: sentiment mix + top categories
# --------------------------------------------------------------------------- #
def fig_corpus(f: dict) -> str:
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(12.4, 4.5), gridspec_kw={"width_ratios": [1, 1.45]}
    )

    # --- Sentiment mix (donut) ------------------------------------------- #
    order = ["Neutral", "Negative", "Positive"]
    mix = {k: int(f["sentiment_mix"].get(k, 0)) for k in order}
    total = sum(mix.values()) or 1
    wedges, _ = ax1.pie(
        list(mix.values()),
        colors=[SENTIMENT_COLOURS[k] for k in order],
        startangle=90, counterclock=False,
        wedgeprops={"width": 0.42, "edgecolor": "white", "linewidth": 2},
    )
    ax1.text(0, 0.10, f"{total:,}", ha="center", va="center",
             fontsize=18, fontweight="bold", color=NAVY)
    ax1.text(0, -0.20, "articles tagged", ha="center", va="center",
             fontsize=9.5, color=GREY)
    ax1.set_title("Sentiment mix of the corpus", fontsize=12,
                  fontweight="bold", pad=12)
    ax1.legend(
        wedges,
        [f"{k}  —  {v:,}  ({v / total * 100:.1f}%)" for k, v in mix.items()],
        loc="lower center", bbox_to_anchor=(0.5, -0.16),
        frameon=False, fontsize=9.5, handlelength=1.1,
    )

    # --- Top-10 categories (horizontal bars) ------------------------------ #
    cats = list(f["top_categories"].items())[::-1]
    labels = [c for c, _ in cats]
    values = [v for _, v in cats]
    ypos = np.arange(len(labels))
    bars = ax2.barh(ypos, values, height=0.68, color=BLUE, edgecolor=NAVY, linewidth=0.6)
    bars[-1].set_color(NAVY)
    ax2.set_yticks(ypos, labels, fontsize=9.5)
    ax2.set_xlabel("Articles", fontsize=9.5)
    ax2.set_xlim(0, max(values) * 1.16)
    ax2.set_title(
        f"Top 10 of {f['categories']} topic categories (long-tail catalogue)",
        fontsize=12, fontweight="bold", pad=12,
    )
    for y, v in zip(ypos, values):
        ax2.text(v + max(values) * 0.015, y, f"{v:,}", va="center",
                 fontsize=9, color="#333333")
    ax2.grid(axis="x", linestyle=":", linewidth=0.7, color=LIGHT_GREY)
    ax2.set_axisbelow(True)
    _strip(ax2, keep=("bottom",))
    ax2.tick_params(axis="y", length=0)

    fig.tight_layout()
    return _save(fig, "fig_corpus.png")


# --------------------------------------------------------------------------- #
# 3. Embedding retrieval accuracy: Precision@K vs random baseline
# --------------------------------------------------------------------------- #
def fig_retrieval(f: dict) -> str:
    er = f["report"]["embedding_retrieval"]
    rq = f["report"]["recommendation_quality"]
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(12.4, 4.4), gridspec_kw={"width_ratios": [1.15, 1]}
    )

    # --- Precision@K vs baseline ----------------------------------------- #
    ks = [1, 5, 10]
    vals = [er[f"precision@{k}"] * 100 for k in ks]
    base = er["random_baseline"] * 100
    x = np.arange(len(ks))
    bars = ax1.bar(x, vals, width=0.5, color=[NAVY, BLUE, LIGHT_BLUE],
                   edgecolor=NAVY, linewidth=0.8, zorder=3, label="Measured")
    ax1.axhline(base, color=RED, linestyle="--", linewidth=1.6, zorder=4,
                label=f"Random baseline ({base:.2f}%)")
    for xi, v in zip(x, vals):
        ax1.text(xi, v + 1.0, f"{v:.1f}%", ha="center", fontsize=10.5,
                 fontweight="bold", color=NAVY, zorder=5)
        ax1.text(xi, v / 2, f"{v / base:.0f}x\nrandom", ha="center", va="center",
                 fontsize=9, color="white", fontweight="bold", zorder=5)
    ax1.set_xticks(x, [f"Precision@{k}" for k in ks], fontsize=10)
    ax1.set_ylabel("Nearest neighbours in the same topic (%)", fontsize=9.5)
    ax1.set_ylim(0, max(vals) * 1.34)
    ax1.set_title(
        f"Embedding retrieval accuracy\n{er['sampled_articles']} sampled articles · "
        f"{f['categories']} categories as ground truth",
        fontsize=11.5, fontweight="bold", pad=10,
    )
    ax1.legend(frameon=False, fontsize=9, loc="upper right")
    ax1.grid(axis="y", linestyle=":", linewidth=0.7, color=LIGHT_GREY)
    ax1.set_axisbelow(True)
    _strip(ax1)

    # --- Recommendation quality: measured vs baseline --------------------- #
    names = ["Topic\nconsistency", "Diversity@10", "Catalogue\ncoverage"]
    measured = [
        rq["category_consistency"] * 100,
        rq["diversity@N"] * 100,
        rq["catalogue_coverage"] * 100,
    ]
    baselines = [rq["consistency_baseline"] * 100, None, None]

    x = np.arange(len(names))
    w = 0.36
    ax2.bar(x - w / 2, measured, width=w, color=NAVY, edgecolor=NAVY,
            linewidth=0.8, zorder=3, label="Measured")
    ax2.bar(
        [x[0] + w / 2], [baselines[0]], width=w, color=LIGHT_GREY,
        edgecolor=GREY, linewidth=0.8, zorder=3, label="Random baseline",
    )
    for xi, v in zip(x, measured):
        ax2.text(xi - w / 2, v + 1.4, f"{v:.1f}%", ha="center", fontsize=10,
                 fontweight="bold", color=NAVY, zorder=5)
    ax2.text(x[0] + w / 2, baselines[0] + 1.4, f"{baselines[0]:.1f}%",
             ha="center", fontsize=9.5, color=GREY, zorder=5)
    ax2.annotate(
        f"{measured[0] / baselines[0]:.1f}x lift",
        xy=(x[0], measured[0] + 9), ha="center", fontsize=9.5,
        fontweight="bold", color=GREEN,
    )
    ax2.set_xticks(x, names, fontsize=9.5)
    ax2.set_ylabel("Percent", fontsize=9.5)
    ax2.set_ylim(0, max(measured) * 1.34)
    ax2.set_title(
        f"Recommendation quality\n{rq['sampled_users']} simulated readers · "
        f"top-{rq['top_n']} lists",
        fontsize=11.5, fontweight="bold", pad=10,
    )
    ax2.legend(frameon=False, fontsize=9, loc="upper right")
    ax2.grid(axis="y", linestyle=":", linewidth=0.7, color=LIGHT_GREY)
    ax2.set_axisbelow(True)
    _strip(ax2)

    fig.tight_layout()
    return _save(fig, "fig_retrieval.png")


# --------------------------------------------------------------------------- #
# 4. Sentiment: confusion matrix + per-class precision / recall / F1
# --------------------------------------------------------------------------- #
def fig_sentiment(f: dict) -> str:
    s = f["sentiment"]
    labels = s["labels"]
    cm = np.array(s["confusion_matrix"], dtype=float)
    row_pct = cm / cm.sum(axis=1, keepdims=True) * 100

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(12.4, 4.5), gridspec_kw={"width_ratios": [1, 1.2]}
    )

    # --- Confusion matrix ------------------------------------------------- #
    im = ax1.imshow(row_pct, cmap="Blues", vmin=0, vmax=100)
    ax1.set_xticks(range(len(labels)), labels, fontsize=10)
    ax1.set_yticks(range(len(labels)), labels, fontsize=10)
    ax1.set_xlabel("Predicted label", fontsize=9.5)
    ax1.set_ylabel("True label (dataset ground truth)", fontsize=9.5)
    ax1.set_title(
        f"Sentiment confusion matrix\naccuracy {s['accuracy'] * 100:.1f}% on "
        f"{s['samples']:,} held-out headlines",
        fontsize=11.5, fontweight="bold", pad=10,
    )
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax1.text(
                j, i - 0.11, f"{int(cm[i, j]):,}", ha="center", va="center",
                fontsize=11, fontweight="bold",
                color="white" if row_pct[i, j] > 55 else "#1A1A1A",
            )
            ax1.text(
                j, i + 0.20, f"{row_pct[i, j]:.1f}%", ha="center", va="center",
                fontsize=8.5,
                color="#E8F1FA" if row_pct[i, j] > 55 else GREY,
            )
    cbar = fig.colorbar(im, ax=ax1, fraction=0.045, pad=0.03)
    cbar.set_label("% of true class (row)", fontsize=8.5)
    cbar.ax.tick_params(labelsize=8)

    # --- Per-class precision / recall / F1 -------------------------------- #
    pc = s["per_class"]
    metrics = ["precision", "recall", "f1"]
    colours = [NAVY, BLUE, LIGHT_BLUE]
    x = np.arange(len(labels))
    w = 0.26
    for m_i, (m, col) in enumerate(zip(metrics, colours)):
        vals = [pc[l][m] * 100 for l in labels]
        off = (m_i - 1) * w
        ax2.bar(x + off, vals, width=w, color=col, edgecolor=NAVY,
                linewidth=0.6, zorder=3,
                label={"f1": "F1-score"}.get(m, m.capitalize()))
        for xi, v in zip(x, vals):
            ax2.text(xi + off, v + 1.4, f"{v:.0f}", ha="center", fontsize=8.5,
                     color="#333333", zorder=5)

    ax2.set_xticks(
        x, [f"{l}\n(n={pc[l]['support']:,})" for l in labels], fontsize=9.5
    )
    ax2.set_ylabel("Percent", fontsize=9.5)
    ax2.set_ylim(0, 108)
    ax2.axhline(s["accuracy"] * 100, color=GREEN, linestyle="--", linewidth=1.4,
                zorder=4, label=f"Overall accuracy ({s['accuracy'] * 100:.1f}%)")
    ax2.set_title(
        "Per-class performance\nbalanced class weights lift minority-class recall",
        fontsize=11.5, fontweight="bold", pad=10,
    )
    ax2.legend(frameon=False, fontsize=8.8, ncol=2, loc="upper center")
    ax2.grid(axis="y", linestyle=":", linewidth=0.7, color=LIGHT_GREY)
    ax2.set_axisbelow(True)
    _strip(ax2)

    fig.tight_layout()
    return _save(fig, "fig_sentiment.png")


# --------------------------------------------------------------------------- #
def main() -> dict:
    print("Generating presentation figures ...")
    f = load_facts()
    fig_architecture(f)
    fig_corpus(f)
    fig_retrieval(f)
    fig_sentiment(f)
    print("Done.")
    return f


if __name__ == "__main__":
    main()
