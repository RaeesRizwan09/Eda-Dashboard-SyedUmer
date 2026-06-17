# charts.py
"""charts.py — Dark Mode Analytics Engines for Onyx Coffee Lab"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# ── DESIGN CONSTANTS ─────────────────────────────────────────────────────────
ONYX_BG = "#0D0F12"
SLATE_CARD = "#161A1F"
GRID_COLOR = "#252C34"
COPPER = "#D97443"
GOLD = "#E5A93C"
CHERRY = "#C43A45"
MINT = "#3D9970"
TEXT_MAIN = "#F3F4F6"
TEXT_MUTED = "#8A95A5"

def _apply_dark_canvas(fig, ax):
    """Applies premium dark-lab styling parameters to a plot axis."""
    fig.patch.set_facecolor(ONYX_BG)
    ax.set_facecolor(SLATE_CARD)
    ax.tick_params(colors=TEXT_MUTED, labelsize=9)
    ax.xaxis.label.set_color(TEXT_MUTED)
    ax.yaxis.label.set_color(TEXT_MUTED)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
        spine.set_linewidth(0.8)
    ax.grid(color=GRID_COLOR, linewidth=0.5, alpha=0.6)

def _title(ax, label: str):
    ax.set_title(label.upper(), fontsize=10, fontname="monospace", color=TEXT_MAIN, pad=14, weight="bold")

# ── MODULE 01: ORIGIN DYNAMICS ────────────────────────────────────────────────
def plot_top_countries(df, top_n=10):
    data = df[df["total_cup_points"] > 60].groupby("country_of_origin")["total_cup_points"].mean().sort_values(ascending=False).head(top_n)
    if data.empty: return None
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    colors = sns.color_palette("flare_r", n_colors=len(data))
    bars = ax.barh(data.index[::-1], data.values[::-1], color=colors, height=0.6, edgecolor=ONYX_BG, linewidth=1)
    
    # Value overlay inside the bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width - 3, bar.get_y() + bar.get_height()/2, f"{width:.2f}", 
                va='center', ha='right', color=TEXT_MAIN, fontsize=8, weight='bold', fontname='monospace')
                
    ax.set_xlim(data.min() - 2, data.max() + 0.5)
    _title(ax, f"Top {top_n} Origins by Mean Cup Points")
    fig.tight_layout()
    return fig

def plot_processing_distribution(df, top_n=8):
    top_countries = df["country_of_origin"].value_counts().head(top_n).index
    sub = df[df["country_of_origin"].isin(top_countries) & df["processing_method"].notna()]
    if sub.empty: return None
    
    ct = pd.crosstab(sub["country_of_origin"], sub["processing_method"], normalize="index") * 100
    ct = ct.reindex(top_countries)
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    ct.plot(kind="bar", stacked=True, ax=ax, color=[COPPER, GOLD, MINT, CHERRY, "#5B6B7C"], width=0.6, edgecolor=ONYX_BG, linewidth=0.5)
    
    ax.legend(facecolor=SLATE_CARD, edgecolor=GRID_COLOR, labelcolor=TEXT_MAIN, fontsize=8, loc='upper left', bbox_to_anchor=(1, 1))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_ylabel("Lot Share (%)", fontsize=9)
    _title(ax, "Processing Method Shares across Key Origins")
    fig.tight_layout()
    return fig

# ── MODULE 02: SENSORY CHEMISTRY ──────────────────────────────────────────────
def plot_sensory_radar(df):
    attrs = ["aroma", "flavor", "aftertaste", "acidity", "body", "balance", "uniformity", "sweetness"]
    means = df[attrs].mean()
    if means.isna().all(): return None
    
    angles = np.linspace(0, 2 * np.pi, len(attrs), endpoint=False).tolist()
    values = means.tolist()
    angles += angles[:1]
    values += values[:1]
    
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(ONYX_BG)
    ax.set_facecolor(SLATE_CARD)
    
    ax.plot(angles, values, color=COPPER, linewidth=2, linestyle="solid")
    ax.fill(angles, values, color=COPPER, alpha=0.25)
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), [a.upper() for a in attrs], color=TEXT_MUTED, fontsize=8, fontname='monospace')
    ax.grid(color=GRID_COLOR, linewidth=0.7)
    ax.set_rlabel_position(180)
    ax.tick_params(colors=TEXT_MUTED, labelsize=7)
    
    _title(ax, "Mean Cup Geometry Profile")
    fig.tight_layout()
    return fig

def plot_sensory_boxes(df):
    attrs = ["aroma", "flavor", "aftertaste", "acidity", "body", "balance"]
    sub = df[attrs].melt()
    if sub.empty: return None
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    sns.boxplot(x="variable", y="value", data=sub, ax=ax, palette="flare", width=0.5,
                linewidth=1.2, fliersize=1.5, boxprops=dict(edgecolor=TEXT_MAIN),
                whiskerprops=dict(color=TEXT_MUTED), capprops=dict(color=TEXT_MUTED))
                
    ax.set_xticklabels([x.get_text().upper() for x in ax.get_xticklabels()], fontname='monospace')
    ax.set_xlabel("")
    ax.set_ylabel("Intensity Score", fontsize=9)
    _title(ax, "Attribute Intensity Dispersion")
    fig.tight_layout()
    return fig

def plot_correlation_heatmap(df):
    attrs = ["total_cup_points", "aroma", "flavor", "aftertaste", "acidity", "body", "balance", "sweetness"]
    corr = df[attrs].corr()
    if corr.empty: return None
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    fig.patch.set_facecolor(ONYX_BG)
    ax.set_facecolor(SLATE_CARD)
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(220, 25, as_cmap=True)
    
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1.0, center=0, annot=True, fmt=".2f",
                annot_kws={"size": 7, "fontname": "monospace", "weight": "bold"}, square=False, ax=ax, cbar=False)
                
    ax.set_xticklabels([x.get_text().upper() for x in ax.get_xticklabels()], rotation=45, ha="right", fontname='monospace', fontsize=8)
    ax.set_yticklabels([y.get_text().upper() for y in ax.get_yticklabels()], rotation=0, fontname='monospace', fontsize=8)
    _title(ax, "Sensory Correlation Matrix Matrix")
    fig.tight_layout()
    return fig

# ── MODULE 03: ALCHEMY OF PROCESSING ─────────────────────────────────────────
def plot_species_kde(df):
    if df["species"].nunique() < 1: return None
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    colors = {"Arabica": COPPER, "Robusta": MINT}
    for sp, color in colors.items():
        subset = df[(df["species"] == sp) & (df["total_cup_points"] > 65)]
        if len(subset) > 3:
            sns.kdeplot(x="total_cup_points", data=subset, ax=ax, fill=True, alpha=0.2, color=color, linewidth=2, label=sp)
            
    ax.legend(facecolor=SLATE_CARD, edgecolor=GRID_COLOR, labelcolor=TEXT_MAIN, fontsize=8)
    ax.set_xlabel("Total Cup Points")
    _title(ax, "Sensory Density Function by Botanical Species")
    fig.tight_layout()
    return fig

def plot_processing_violins(df):
    sub = df[df["processing_method"].notna() & (df["total_cup_points"] > 70)]
    counts = sub["processing_method"].value_counts()
    valid_methods = counts[counts > 5].index
    sub = sub[sub["processing_method"].isin(valid_methods)]
    if sub.empty: return None
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    sns.violinplot(x="processing_method", y="total_cup_points", data=sub, ax=ax, palette="copper", linewidth=1, inner="quartile")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    ax.set_xlabel("")
    ax.set_ylabel("Total Cup Points")
    _title(ax, "Sensory Architecture via Processing Method")
    fig.tight_layout()
    return fig

def plot_variety_strip(df, top_n=8):
    top_var = df["variety"].value_counts().head(top_n).index
    sub = df[df["variety"].isin(top_var) & (df["total_cup_points"] > 70)]
    if sub.empty: return None
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    sns.stripplot(x="variety", y="total_cup_points", data=sub, ax=ax, palette="flare", alpha=0.5, size=4, jitter=0.25)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    ax.set_xlabel("")
    ax.set_ylabel("Total Cup Points")
    _title(ax, "Lot Dispersion across Primary Varieties")
    fig.tight_layout()
    return fig

# ── MODULE 04: TERROIR & MACRO-ANALYSIS ─────────────────────────────────────
def plot_altitude_scatter(df):
    sub = df[df["altitude_mean_meters"].notna() & (df["altitude_mean_meters"] < 3500) & (df["total_cup_points"] > 65)]
    if sub.empty: return None
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    sns.regplot(x="altitude_mean_meters", y="total_cup_points", data=sub, ax=ax,
                scatter_kws={"alpha": 0.3, "color": GOLD, "s": 15},
                line_kws={"color": COPPER, "linewidth": 1.5})
                
    ax.set_xlabel("Mean Operational Altitude (meters)")
    ax.set_ylabel("Total Cup Points")
    _title(ax, "Terroir Metric: Altitude vs. Total Cup Points")
    fig.tight_layout()
    return fig

def plot_score_timeline(df):
    if "grading_date" not in df.columns: return None
    df_copy = df.copy()
    df_copy["year"] = pd.to_datetime(df_copy["grading_date"], errors='coerce').dt.year
    sub = df_copy[df_copy["year"].notna() & (df_copy["total_cup_points"] > 65)]
    yearly = sub.groupby("year")["total_cup_points"].agg(["mean", "std", "count"]).dropna()
    if yearly.empty: return None
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    ax.plot(yearly.index, yearly["mean"], color=COPPER, marker="o", linewidth=1.5, markersize=4, label="Annual Mean")
    ax.fill_between(yearly.index, yearly["mean"] - yearly["std"]*0.5, yearly["mean"] + yearly["std"]*0.5, color=COPPER, alpha=0.15, label="Variance Band")
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))
    ax.legend(facecolor=SLATE_CARD, edgecolor=GRID_COLOR, labelcolor=TEXT_MAIN, fontsize=8)
    ax.set_xlabel("Grading Timeline (Years)")
    ax.set_ylabel("Total Score")
    _title(ax, "Global Vintage Stability Timeline")
    fig.tight_layout()
    return fig

def plot_terroir_bubble(df):
    sub = df[df["altitude_mean_meters"].notna() & (df["altitude_mean_meters"] < 3000) & (df["total_cup_points"] > 65)]
    agg = sub.groupby("country_of_origin").agg(
        mean_score=("total_cup_points", "mean"),
        mean_alt=("altitude_mean_meters", "mean"),
        lot_count=("total_cup_points", "count")
    ).reset_index()
    if agg.empty: return None
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    sc = ax.scatter(agg["mean_alt"], agg["mean_score"], s=agg["lot_count"] * 2.5, 
                    c=agg["mean_score"], cmap="flare", alpha=0.7, edgecolors=ONYX_BG, linewidths=0.5)
                    
    cbar = plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=8, colors=TEXT_MUTED)
    cbar.outline.set_edgecolor(GRID_COLOR)
    
    ax.set_xlabel("Mean Elevation (m)")
    ax.set_ylabel("Mean Country Score")
    _title(ax, "Macro Terroir Bubble Architecture")
    fig.tight_layout()
    return fig

# ── MODULE 05 & 06: PAIRWISE MATRIX & DEFECT AUDITS ──────────────────────────
def plot_defect_analysis(df):
    agg = df.groupby("country_of_origin").agg(
        cat1=("category_one_defects", "mean"),
        cat2=("category_two_defects", "mean"),
        quakers=("quakers", "mean")
    ).sort_values(by="cat2", ascending=False).head(8)
    if agg.empty: return None
    
    fig, ax = plt.subplots(figsize=(7, 3.8))
    _apply_dark_canvas(fig, ax)
    
    agg.plot(kind="bar", ax=ax, color=[CHERRY, GOLD, COPPER], width=0.6, edgecolor=ONYX_BG, linewidth=0.5)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    ax.set_xlabel("")
    ax.set_ylabel("Mean Count per Lot")
    _title(ax, "Technical Defect Profiling by Origin")
    fig.tight_layout()
    return fig

def plot_pairwise_matrix(df):
    attrs = ["aroma", "flavor", "acidity", "body", "species"]
    sub = df[df[attrs].notna().all(axis=1) & (df["total_cup_points"] > 70)]
    if sub.empty: return None
    
    plt.rcParams.update({
        'text.color': TEXT_MAIN, 'axes.labelcolor': TEXT_MUTED,
        'xtick.color': TEXT_MUTED, 'ytick.color': TEXT_MUTED,
        'figure.facecolor': ONYX_BG, 'axes.facecolor': SLATE_CARD
    })
    
    g = sns.pairplot(sub, vars=["aroma", "flavor", "acidity", "body"], hue="species",
                     palette={"Arabica": COPPER, "Robusta": MINT}, height=1.5, aspect=1.2,
                     plot_kws=dict(alpha=0.4, s=8, edgecolor="none"), diag_kws=dict(fill=True, alpha=0.3))
                     
    for ax in g.axes.flatten():
        if ax is not None:
            ax.set_facecolor(SLATE_CARD)
            for spine in ax.spines.values():
                spine.set_color(GRID_COLOR)
            ax.grid(color=GRID_COLOR, linewidth=0.4, alpha=0.4)
            
    g.legend.set_title("SPECIES")
    g.legend.get_frame().set_facecolor(SLATE_CARD)
    g.legend.get_frame().set_edgecolor(GRID_COLOR)
    plt.subplots_adjust(top=0.92)
    g.fig.suptitle("PAIRWISE INTERACTION LAB MATRIX", fontsize=9, fontname="monospace", color=TEXT_MAIN, weight="bold")
    return g.fig