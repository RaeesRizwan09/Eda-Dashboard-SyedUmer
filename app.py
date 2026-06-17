# app.py
"""
app.py — Core Orchestrator for Onyx Coffee Lab Dashboards
Aesthetic Styling Framework: Cyber Coffee Intelligence / Midnight Onyx & Refined Copper Wire
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import base64
from datetime import datetime
from io import BytesIO
import charts
import filter

# ── BASE CONFIGURATION ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎛 Onyx Coffee Lab · Terroir Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── INJECT EXPERIMENTAL GLOW & HOVER CSS OVERRIDES ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,400&family=Space+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');

/* Main Canvas Configuration */
html, body, .stApp {
    background-color: #0D0F12 !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #F3F4F6;
}
.block-container {
    padding: 1.8rem 2.5rem 4rem;
    max-width: 1520px;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #080A0C !important;
    border-right: 1px solid #252C34;
}
[data-testid="stSidebar"] * {
    color: #8A95A5 !important;
}
[data-testid="stSidebar"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #D97443 !important;
    padding-top: 12px;
}
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div {
    background: #D97443 !important;
}

/* Custom Interactive Etched Glass Button */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #D97443 !important;
    border: 1px solid #D97443 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    width: 100%;
    border-radius: 0px;
    margin-top: 15px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(217, 116, 67, 0.12) !important;
    box-shadow: 0 0 14px rgba(217, 116, 67, 0.45);
    color: #F3F4F6 !important;
    transform: translateY(-1px);
}

/* Premium Lab Hero Sheet Header */
.hero-card {
    background: linear-gradient(135deg, #161A1F 0%, #0D0F12 100%);
    border: 1px solid #252C34;
    border-left: 4px solid #D97443;
    padding: 40px;
    border-radius: 2px;
    margin-bottom: 35px;
    position: relative;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.hero-card::after {
    content: 'LAB-ID // CQI.94';
    position: absolute;
    right: 30px; top: 30px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #252C34;
    letter-spacing: 2px;
}
.hero-micro-tag {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 3px;
    color: #D97443;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.hero-header-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 48px;
    font-weight: 700;
    color: #F3F4F6;
    line-height: 1.1;
    margin: 0;
}
.hero-header-title em {
    font-style: italic;
    color: #E5A93C;
    font-weight: 400;
}
.hero-summary-text {
    font-size: 14px;
    color: #8A95A5;
    margin-top: 12px;
    max-width: 750px;
    line-height: 1.6;
}
.hero-badge-strip {
    display: flex;
    gap: 10px;
    margin-top: 25px;
    flex-wrap: wrap;
}
.hero-individual-badge {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
    color: #8A95A5;
    background-color: #101418;
    border: 1px solid #252C34;
    padding: 6px 14px;
}

/* Technological Floating KPI Cards Matrix */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 15px;
    margin-bottom: 35px;
}
.kpi-box {
    background-color: #161A1F;
    border: 1px solid #252C34;
    padding: 22px 18px;
    border-radius: 0px;
    transition: all 0.25s ease;
}
.kpi-box:hover {
    border-color: #D97443;
    background-color: #1A1F26;
    transform: translateY(-2px);
}
.kpi-box-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: #8A95A5;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.kpi-box-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 34px;
    font-weight: 700;
    color: #D97443;
    line-height: 1;
}
.kpi-box-meta {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #4B5563;
    margin-top: 6px;
}

/* Custom Styled Technical Framework Core Sections */
.framework-section-wrapper {
    display: flex;
    align-items: center;
    gap: 15px;
    margin: 45px 0 25px;
}
.framework-section-bullet {
    width: 6px;
    height: 6px;
    background-color: #D97443;
    box-shadow: 0 0 8px #D97443;
}
.framework-section-title {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    letter-spacing: 3px;
    color: #F3F4F6;
    text-transform: uppercase;
    font-weight: 700;
}
.framework-section-line {
    flex: 1;
    height: 1px;
    background-color: #252C34;
}

/* High-clarity Chart Container Shell */
.analytics-shell {
    background-color: #161A1F;
    border: 1px solid #252C34;
    border-radius: 2px;
    margin-bottom: 20px;
    overflow: hidden;
}
.analytics-shell-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    background-color: #101418;
    border-bottom: 1px solid #252C34;
}
.analytics-shell-title {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 1.5px;
    color: #8A95A5;
}
.analytics-shell-action-link {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #E5A93C;
    text-decoration: none;
    border: 1px solid #363F4D;
    padding: 2px 8px;
    transition: all 0.2s;
}
.analytics-shell-action-link:hover {
    border-color: #E5A93C;
    background-color: rgba(229, 169, 60, 0.08);
}
.analytics-shell-body img {
    width: 100%;
    height: auto;
    display: block;
}

/* Custom Dataframe & Input Styling Modifications */
[data-testid="stDataFrame"] {
    border: 1px solid #252C34 !important;
}
.stTabs [data-baseweb="tab-list"] {
    background-color: #101418 !important;
    border-bottom: 1px solid #252C34 !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 1.5px !important;
    color: #8A95A5 !important;
    padding: 10px 20px !important;
    background-color: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #D97443 !important;
    background-color: #161A1F !important;
    font-weight: bold !important;
}

/* High-end Sticker Bags Callouts */
.sticker-callout {
    background-color: #101418;
    border-left: 3px solid #C43A45;
    padding: 15px 20px;
    margin: 10px 0 20px;
    font-size: 13px;
    color: #8A95A5;
    line-height: 1.6;
}
.sticker-callout strong {
    color: #F3F4F6;
}

/* Filter Badge Tokens */
.badge-token {
    display: inline-flex;
    align-items: center;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #D97443;
    background: rgba(217, 116, 67, 0.08);
    border: 1px solid rgba(217, 116, 67, 0.2);
    padding: 3px 10px;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── DATA LOADING INGESTION PIPELINE ──────────────────────────────────────────
@st.cache_data
@st.cache_data
def ingest_clean_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    
    # --- KAGGLE COLUMN TRANSLATION LAYER ---
    # Automatically convert standard Kaggle formats (Spaces, Dots, Caps) to lower_underscore format
    df.columns = (
        df.columns.str.lower()
        .str.replace('.', '_', regex=False)
        .str.replace(' ', '_', regex=False)
    )
    
    # Specific hardcoded patches for common Kaggle variants if necessary:
    rename_dict = {
        "country_of_origin": "country_of_origin",
        "total_cup_points": "total_cup_points",
        "altitude_mean_meters": "altitude_mean_meters"
    }
    # If the file uses shorthand headers like 'country' or 'total_points', patch them here:
    if "country" in df.columns and "country_of_origin" not in df.columns:
        df = df.rename(columns={"country": "country_of_origin"})
    if "total_points" in df.columns and "total_cup_points" not in df.columns:
        df = df.rename(columns={"total_points": "total_cup_points"})
    if "altitude" in df.columns and "altitude_mean_meters" not in df.columns:
        df = df.rename(columns={"altitude": "altitude_mean_meters"})
    # ----------------------------------------

    # Clip unrealistic outlier altitude values
    if "altitude_mean_meters" in df.columns:
        # Convert to numeric if it loaded as text
        df["altitude_mean_meters"] = pd.to_numeric(df["altitude_mean_meters"], errors='coerce')
        df.loc[df["altitude_mean_meters"] > 8500, "altitude_mean_meters"] = np.nan
        
    # Standardize textual columns strings
    for col in ["country_of_origin", "species", "processing_method", "variety", "color"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace("nan", np.nan)
            
    return df

DATA_TARGET = os.path.join("data", "coffee_ratings.csv")
if not os.path.exists(DATA_TARGET):
    st.error("Technical core dataset 'coffee_ratings.csv' cannot be located under data/ path directory.")
    st.stop()

raw_df = ingest_clean_dataset(DATA_TARGET)

# ── PARAMETER RECTIFIER SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 20px 0 5px 0;">
        <div style="font-family:'Space Mono', monospace; font-size:9px; color:#4B5563; letter-spacing:3px; text-transform:uppercase;">Intel System Core</div>
        <div style="font-family:'Cormorant Garamond', serif; font-size:24px; color:#F3F4F6; margin-top:2px; font-style:italic;">Control Registry</div>
        <div style="height:1px; background-color:#252C34; margin:15px 0 10px 0;"></div>
    </div>
    """, unsafe_allow_html=True)

    if "filter_reset_switch" not in st.session_state:
        st.session_state.filter_reset_switch = False
    state_suffix = "_rst" if st.session_state.filter_reset_switch else ""

    opts_country = sorted(raw_df["country_of_origin"].dropna().unique().tolist())
    opts_species = sorted(raw_df["species"].dropna().unique().tolist())
    opts_process = sorted(raw_df["processing_method"].dropna().unique().tolist())

    min_score_val = float(raw_df[raw_df["total_cup_points"] > 10]["total_cup_points"].min())
    max_score_val = float(raw_df["total_cup_points"].max())

    alt_series = raw_df["altitude_mean_meters"].dropna()
    min_alt_val = int(alt_series.min()) if not alt_series.empty else 0
    max_alt_val = int(alt_series.max()) if not alt_series.empty else 4000

    # Custom Multi-select and Filter widgets
    sel_countries  = st.multiselect("Geographic Origin", options=opts_country, default=[], key=f"c_co{state_suffix}")
    sel_species    = st.multiselect("Botanical Lineage", options=opts_species, default=[], key=f"c_sp{state_suffix}")
    sel_processing = st.multiselect("Processing Mode",   options=opts_process, default=[], key=f"c_pr{state_suffix}")
    
    sel_score = st.slider("Cupping Score Bounds", min_value=min_score_val, max_value=max_score_val, 
                          value=(min_score_val, max_score_val), format="%.1f", key=f"c_sc{state_suffix}")
                          
    sel_alt   = st.slider("Elevation Threshold (m)", min_value=min_alt_val, max_value=max_alt_val, 
                        value=(min_alt_val, max_alt_val), key=f"c_al{state_suffix}")
                        
    charts_top_n = st.slider("Rank Horizon Limit", 5, 20, 10, key=f"c_tn{state_suffix}")

    if st.button("⚡ Purge Operational Filters"):
        st.session_state.filter_reset_switch = not st.session_state.filter_reset_switch
        st.rerun()
    if st.session_state.filter_reset_switch:
        st.session_state.filter_reset_switch = False

# ── ENGINE COMPILATION LAYER ──────────────────────────────────────────────────
df_filtered = filter.apply_filters(
    raw_df, sel_countries, sel_species, sel_processing, sel_score, sel_alt
)

# ── BRAND HEADER COMPONENT ────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-card">
    <div class="hero-micro-tag">// Advanced Sensometric Analytics Platform</div>
    <div class="hero-header-title">THE ONYX COFFEE LAB · <em>Terroir Intelligence</em></div>
    <div class="hero-summary-text">
        Isolating sensory architectures, structural anomalies, and geographical chemical markers across 
        {raw_df['country_of_origin'].nunique()} verified production origins encompassing {len(raw_df):,} graded single-origin specialty lots.
    </div>
    <div class="hero-badge-strip">
        <span class="hero-individual-badge">🧬 {raw_df['species'].nunique()} GENERA</span>
        <span class="hero-individual-badge">📍 {raw_df['country_of_origin'].nunique()} ESCARPMENTS</span>
        <span class="hero-individual-badge">⛓ {raw_df['processing_method'].nunique()} PHASES</span>
        <span class="hero-individual-badge">📊 {len(raw_df):,} EVALUATIONS</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Active Token Render Pipelines
active_tokens = []
if sel_countries:  active_tokens.append(f"ORIGINS: {len(sel_countries)}")
if sel_species:    active_tokens.append(f"GENERA: {', '.join(sel_species)}")
if sel_processing: active_tokens.append(f"MODES: {len(sel_processing)}")
if sel_score != (min_score_val, max_score_val): active_tokens.append(f"SCORE: {sel_score[0]:.1f}–{sel_score[1]:.1f}")

if active_tokens:
    token_html = "".join(f'<span class="badge-token">// {t}</span>' for t in active_tokens)
    st.markdown(f'<div style="margin:-15px 0 25px 0;">{token_html}</div>', unsafe_allow_html=True)

if df_filtered.empty:
    st.error("Zero data records intersected with the active filter parameters matrix. Re-verify the control registry inputs.")
    st.stop()

# ── FLOATING READOUT NUMERIC HARDWARE CARDS ────────────────────────────────────
clean_points = df_filtered[df_filtered["total_cup_points"] > 40]["total_cup_points"]
calc_avg = clean_points.mean() if not clean_points.empty else 0.0
calc_max = df_filtered["total_cup_points"].max()
calc_lots = len(df_filtered)
calc_countries = df_filtered["country_of_origin"].nunique()

top_origin_series = df_filtered[df_filtered["total_cup_points"] > 40].groupby("country_of_origin")["total_cup_points"].mean()
calc_top_org = top_origin_series.idxmax() if not top_origin_series.empty else "None"

arabica_count = df_filtered["species"].str.lower().str.contains("arabica").sum()
calc_arabica_ratio = (arabica_count / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0.0

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-box">
        <div class="kpi-box-label">// Avg Quality Index</div>
        <div class="kpi-box-value">{calc_avg:.2f}</div>
        <div class="kpi-box-meta">Global Score Mean</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-box-label">// Absolute Ceiling</div>
        <div class="kpi-box-value">{calc_max:.1f}</div>
        <div class="kpi-box-meta">Highest Lot Point</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-box-label">// Apex Terroir Map</div>
        <div class="kpi-box-value" style="font-size:20px; padding-top:6px; overflow:hidden; white-space:nowrap;">{calc_top_org}</div>
        <div class="kpi-box-meta">Highest Grouped Mean</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-box-label">// Lot Throughput</div>
        <div class="kpi-box-value">{calc_lots:,}</div>
        <div class="kpi-box-meta">Audited across {calc_countries} regions</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-box-label">// Arabica Lineage</div>
        <div class="kpi-box-value">{calc_arabica_ratio:.1f}%</div>
        <div class="kpi-box-meta">Proportional Volumetric Share</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── RENDER SHELL WRAPPER PIPELINE ─────────────────────────────────────────────
def output_lab_canvas(figure_object, title_label: str, export_name: str):
    if figure_object is None:
        st.caption("Insufficient metric density to populate technical layout frame.")
        return
    buffer_io = BytesIO()
    figure_object.savefig(buffer_io, format="png", dpi=175, bbox_inches="tight")
    buffer_io.seek(0)
    base64_string = base64.b64encode(buffer_io.read()).decode()
    timestamp_str = datetime.now().strftime("%H%M%S")
    download_uri = f"data:image/png;base64,{base64_string}"
    
    st.markdown(f"""
    <div class="analytics-shell">
        <div class="analytics-shell-header">
            <span class="analytics-shell-title">{title_label.upper()}</span>
            <a class="analytics-shell-action-link" href="{download_uri}" download="ONYX_{export_name}_{timestamp_str}.png">↓ GET SCATTER PNG</a>
        </div>
        <div class="analytics-shell-body">
            <img src="{download_uri}" alt="{title_label}" />
        </div>
    </div>
    """, unsafe_allow_html=True)
    plt.close(figure_object)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION CONTROLLER EXECUTION PLATFORM
# ══════════════════════════════════════════════════════════════════════════════

def render_section_header(code: str, label_text: str):
    st.markdown(f"""
    <div class="framework-section-wrapper">
        <div class="framework-section-bullet"></div>
        <span class="framework-section-title">[ {code} // {label_text} ]</span>
        <div class="framework-section-line"></div>
    </div>
    """, unsafe_allow_html=True)

tab_m1, tab_m2, tab_m3, tab_m4, tab_m5, tab_m6 = st.tabs([
    "01 · Geographic Origin", "02 · Sensory Geometry", "03 · Alchemy Process", 
    "04 · Terroir Vectors", "05 · High-Density Matrix", "06 · Lot Inquest"
])

with tab_m1:
    render_section_header("01", "Macroscopic Geographic Trajectories")
    col1, col2 = st.columns(2)
    with col1:
        output_lab_canvas(charts.plot_top_countries(df_filtered, charts_top_n), "Regional Quality Rankings", "rankings")
    with col2:
        output_lab_canvas(charts.plot_processing_distribution(df_filtered, charts_top_n), "Post-Harvest Strategy Concentration", "processing_shares")
    st.markdown("""
    <div class="sticker-callout">
        <strong>Macro Observation Vector:</strong> Quality indicators express high elastic variance across small mountainous microclimates. 
        Evaluating processing method distribution shows how different regions optimize environmental moisture parameters.
    </div>
    """, unsafe_allow_html=True)

with tab_m2:
    render_section_header("02", "Sensory Chemistry Structure Mapping")
    col1, col2 = st.columns([2, 3])
    with col1:
        output_lab_canvas(charts.plot_sensory_radar(df_filtered), "Unified Flavor Profile Geometry", "radar")
    with col2:
        output_lab_canvas(charts.plot_sensory_boxes(df_filtered), "Organoleptic Dispersion Metrics", "boxes")
    
    output_lab_canvas(charts.plot_correlation_heatmap(df_filtered), "Multivariate Inter-Attribute Co-dependency Index", "heatmap")

with tab_m3:
    render_section_header("03", "The Alchemy of Post-Harvest Processing")
    col1, col2 = st.columns(2)
    with col1:
        output_lab_canvas(charts.plot_species_kde(df_filtered), "Total Quality Probability Density by Genus", "species_density")
    with col2:
        output_lab_canvas(charts.plot_processing_violins(df_filtered), "Score Variance across Post-Harvest Methods", "processing_violins")
        
    output_lab_canvas(charts.plot_variety_strip(df_filtered, charts_top_n), "Cultivar Strain Dispersion Matrix", "variety_strip")

with tab_m4:
    render_section_header("04", "Terroir Metrics & Longitudinal Stability Vectors")
    col1, col2 = st.columns(2)
    with col1:
        output_lab_canvas(charts.plot_altitude_scatter(df_filtered), "Linear Modeling: Elevation Scaling Effect", "altitude_regression")
    with col2:
        output_lab_canvas(charts.plot_score_timeline(df_filtered), "Longitudinal Quality Stability Vintage Over Time", "vintage_timeline")
        
    output_lab_canvas(charts.plot_terroir_bubble(df_filtered), "Multidimensional Environmental Bubble Architecture", "terroir_bubble")

with tab_m5:
    render_section_header("05", "High-Density Pairwise Feature Systems")
    fig_pair = charts.plot_pairwise_matrix(df_filtered)
    if fig_pair:
        buf = BytesIO()
        fig_pair.savefig(buf, format="png", dpi=140, bbox_inches="tight")
        buf.seek(0)
        st.image(buf, use_container_width=True)
        plt.close(fig_pair)
    else:
        st.caption("Pairwise matrix requires data density configurations.")

with tab_m6:
    render_section_header("06", "Lot Auditing Registry & Technical Failure Inquest")
    
    col_d1, col_d2 = st.columns([3, 2])
    with col_d1:
        st.markdown("<div style='font-family:monospace; font-size:11px; margin-bottom:8px; color:#8A95A5;'>[ TECHNICAL DATASTREAM INSIGHT ]</div>", unsafe_allow_html=True)
        view_cols = ["country_of_origin", "species", "processing_method", "variety", "total_cup_points", "aroma", "flavor", "acidity", "body", "category_one_defects", "category_two_defects", "quakers"]
        avail_cols = [c for c in view_cols if c in df_filtered.columns]
        st.dataframe(df_filtered[avail_cols].head(100), use_container_width=True)
    with col_d2:
        output_lab_canvas(charts.plot_defect_analysis(df_filtered), "Defect Trajectory Evaluation Profile", "defect_analysis")
        
    # Multi-Format Technical Export Matrix
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:monospace; font-size:11px; color:#8A95A5;'>[ PROTOCOL DATA TRANSFER REGISTRY ]</div>", unsafe_allow_html=True)
    
    csv_bytes = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 EXTRACT FILTERED QUANTITATIVE STREAM (.CSV)",
        data=csv_bytes,
        file_name=f"ONYX_LAB_DATASTREAM_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ── FOOTER REGISTER TERMINAL ──────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top: 70px; padding: 20px 0 10px 0; border-top: 1px solid #252C34; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
    <div style="font-family: 'Cormorant Garamond', serif; font-size: 15px; color: #8A95A5; font-style: italic;">Onyx Sensometric System · Core Platform Version 4.01.alpha</div>
    <div style="font-family: 'Space Mono', monospace; font-size: 9px; color: #4B5563; letter-spacing: 1px;">SYSTEM RUN REGISTER ACTIVE // SECURE ACCESS GRANTED</div>
</div>
""", unsafe_allow_html=True)