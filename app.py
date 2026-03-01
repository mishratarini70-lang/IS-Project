# =============================================================================
#  IHCL / TAJ HOTELS — "ACCELERATE 2030" STRATEGIC IT INFRASTRUCTURE DEMO
#  MBA Strategic Information Systems Project
#  Single-file Streamlit App | app.py
#  Dependencies: streamlit, pandas, numpy, plotly
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Page config (must be the very first Streamlit call) ──────────────────────
st.set_page_config(
    page_title="IHCL Accelerate 2030 | IT Infrastructure Demo",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
#  BRAND CONSTANTS
# =============================================================================
GOLD    = "#B8962E"
NAVY    = "#1A1A2E"
CREAM   = "#F5F0E8"
GREEN   = "#2E7D5A"
RUST    = "#A0522D"
SILVER  = "#A9A9A9"
LIGHT   = "#F0EBE0"
MID     = "#D4C5A0"

# =============================================================================
#  GLOBAL CSS — Taj Hotels luxury corporate identity
# =============================================================================
st.markdown(f"""
<style>
  /* ── Import fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

  /* ── Root & background ── */
  html, body, [data-testid="stAppViewContainer"] {{
      background-color: {NAVY};
      font-family: 'Inter', sans-serif;
  }}
  [data-testid="stMain"] {{
      background-color: {NAVY};
  }}

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, #0D0D1A 0%, #1A1A2E 60%, #141428 100%);
      border-right: 1px solid {GOLD}44;
  }}
  [data-testid="stSidebar"] * {{
      color: {CREAM} !important;
  }}
  [data-testid="stSidebar"] .stRadio label {{
      font-family: 'Inter', sans-serif;
      font-size: 0.85rem;
      letter-spacing: 0.04em;
      padding: 6px 0;
  }}

  /* ── Headings ── */
  h1, h2, h3 {{
      font-family: 'Playfair Display', serif !important;
      color: {GOLD} !important;
  }}
  h4, h5, h6 {{
      font-family: 'Inter', sans-serif !important;
      color: {CREAM} !important;
      font-weight: 500;
  }}
  p, li, span, div {{
      color: {CREAM};
  }}

  /* ── Metric cards ── */
  [data-testid="metric-container"] {{
      background: linear-gradient(135deg, #242438 0%, #1E1E32 100%);
      border: 1px solid {GOLD}55;
      border-radius: 10px;
      padding: 16px;
  }}
  [data-testid="stMetricValue"] {{
      color: {GOLD} !important;
      font-family: 'Playfair Display', serif !important;
      font-size: 1.7rem !important;
  }}
  [data-testid="stMetricLabel"] {{
      color: {MID} !important;
      font-size: 0.75rem !important;
      letter-spacing: 0.06em;
      text-transform: uppercase;
  }}
  [data-testid="stMetricDelta"] {{
      color: {GREEN} !important;
      font-size: 0.8rem !important;
  }}

  /* ── Sliders ── */
  [data-testid="stSlider"] > div > div > div > div {{
      background: {GOLD} !important;
  }}
  .stSlider label {{
      color: {CREAM} !important;
      font-family: 'Inter', sans-serif;
      font-size: 0.85rem;
  }}

  /* ── Divider ── */
  hr {{
      border-color: {GOLD}33 !important;
  }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {{
      background: transparent;
      border-bottom: 1px solid {GOLD}44;
  }}
  .stTabs [data-baseweb="tab"] {{
      color: {MID} !important;
      font-family: 'Inter', sans-serif;
      font-size: 0.82rem;
      letter-spacing: 0.05em;
  }}
  .stTabs [aria-selected="true"] {{
      color: {GOLD} !important;
      border-bottom: 2px solid {GOLD} !important;
  }}

  /* ── Custom insight box ── */
  .insight-box {{
      background: linear-gradient(135deg, #1B2A1B 0%, #162616 100%);
      border-left: 3px solid {GREEN};
      border-radius: 6px;
      padding: 14px 18px;
      margin: 12px 0;
  }}
  .insight-box p {{
      color: #A8D5B5 !important;
      font-size: 0.85rem;
      line-height: 1.6;
      margin: 0;
  }}

  /* ── ROI highlight box ── */
  .roi-box {{
      background: linear-gradient(135deg, #2A2005 0%, #1F1800 100%);
      border: 1px solid {GOLD}88;
      border-radius: 10px;
      padding: 20px 24px;
      text-align: center;
      margin: 8px 0;
  }}
  .roi-box h2 {{
      font-family: 'Playfair Display', serif !important;
      color: {GOLD} !important;
      font-size: 2rem !important;
      margin: 4px 0 !important;
  }}
  .roi-box p {{
      color: {MID} !important;
      font-size: 0.78rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin: 0;
  }}

  /* ── Section header banner ── */
  .section-banner {{
      background: linear-gradient(90deg, {GOLD}22 0%, transparent 100%);
      border-left: 4px solid {GOLD};
      padding: 10px 18px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 18px;
  }}
  .section-banner h3 {{
      font-family: 'Playfair Display', serif !important;
      color: {GOLD} !important;
      margin: 0 !important;
      font-size: 1.2rem !important;
  }}
  .section-banner p {{
      color: {MID} !important;
      font-size: 0.78rem;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin: 2px 0 0 0;
  }}

  /* ── Hide Streamlit branding ── */
  #MainMenu, footer, header {{visibility: hidden;}}
  [data-testid="stToolbar"] {{display: none;}}
</style>
""", unsafe_allow_html=True)


# =============================================================================
#  HELPER FUNCTIONS
# =============================================================================

def inr(value: float, crore_threshold: float = 1e7) -> str:
    """Format a number as Indian Rupees with Cr/L suffix."""
    if value >= crore_threshold:
        return f"₹{value/1e7:.2f} Cr"
    elif value >= 1e5:
        return f"₹{value/1e5:.1f} L"
    else:
        return f"₹{value:,.0f}"

def roi_card(label: str, value: str, sub: str = ""):
    """Render a styled gold ROI highlight card."""
    st.markdown(f"""
    <div class="roi-box">
        <p>{label}</p>
        <h2>{value}</h2>
        {"<p style='color:#A8D5B5!important;font-size:0.75rem;text-transform:none;letter-spacing:0'>" + sub + "</p>" if sub else ""}
    </div>
    """, unsafe_allow_html=True)

def insight(text: str):
    """Render a green insight callout box."""
    st.markdown(f'<div class="insight-box"><p>💡 {text}</p></div>',
                unsafe_allow_html=True)

def section_banner(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="section-banner">
        <h3>{title}</h3>
        {"<p>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)

def plotly_layout(fig, title="", height=420):
    """Apply consistent dark Taj brand theme to any Plotly figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(family="Playfair Display", size=15,
                                         color=GOLD), x=0.02, xanchor="left"),
        paper_bgcolor="rgba(20,20,40,0.0)",
        plot_bgcolor="rgba(20,20,40,0.4)",
        font=dict(family="Inter", color=CREAM, size=11),
        height=height,
        margin=dict(l=20, r=20, t=50, b=40),
        legend=dict(bgcolor="rgba(20,20,40,0.6)", bordercolor=GOLD+"44",
                    borderwidth=1, font=dict(size=10)),
        xaxis=dict(gridcolor=GOLD+"1A", zerolinecolor=GOLD+"33",
                   tickfont=dict(color=MID)),
        yaxis=dict(gridcolor=GOLD+"1A", zerolinecolor=GOLD+"33",
                   tickfont=dict(color=MID)),
    )
    return fig


# =============================================================================
#  CACHED DATA GENERATORS
# =============================================================================

@st.cache_data
def gen_erp_data(seed=42):
    """Generate 100 ERP procurement transactions across 6 properties."""
    np.random.seed(seed)
    props = ["MUM-01","DEL-02","GOA-03","JAI-04","BLR-05","UDR-06"]
    cats  = {
        "F&B Supplies":              (58_000,  12_000),
        "Housekeeping":              (34_000,   6_000),
        "Linens":                    (1_15_000, 20_000),
        "Spa & Wellness":            (1_02_000, 22_000),
        "Engineering & Maintenance": (2_45_000, 50_000),
        "IT Hardware":               (6_50_000,1_60_000),
    }
    cat_names = list(cats.keys())
    rows = []
    for i in range(1, 101):
        cat  = np.random.choice(cat_names, p=[0.28,0.14,0.14,0.10,0.18,0.16])
        mu, sg = cats[cat]
        amt  = max(15_000, int(np.random.normal(mu, sg)))
        rows.append({"Transaction_ID": f"PO-{i:04d}",
                     "Property_ID":    np.random.choice(props),
                     "Category":       cat,
                     "Amount_INR":     amt,
                     "Status":         np.random.choice(
                         ["Paid","Approved","Pending","Overdue"],
                         p=[0.62,0.18,0.13,0.07])})
    return pd.DataFrame(rows)

@st.cache_data
def gen_cpms_data(seed=42):
    """Generate 200 CPMS bookings across room types and channels."""
    np.random.seed(seed)
    locations = ["Mumbai","Delhi","Goa","Jaipur","Bangalore","Udaipur","Chennai","London"]
    room_rate = {"Deluxe":17_500, "Taj Club":38_000, "Suite":75_000}
    rows = []
    for i in range(1, 201):
        room    = np.random.choice(["Deluxe","Taj Club","Suite"], p=[0.38,0.35,0.27])
        channel = np.random.choice(["Direct","OTA","Corporate"], p=[0.58,0.26,0.16])
        loc     = np.random.choice(locations)
        nights  = np.random.choice(range(1,8), p=[0.10,0.20,0.25,0.20,0.13,0.08,0.04])
        rate    = room_rate[room] * (4.8 if loc == "London" else 1)
        spend   = int(rate * nights * np.random.uniform(0.93, 1.11))
        rows.append({"Booking_ID": f"TH-{i:04d}", "Location": loc,
                     "Room_Type": room,  "Channel": channel,
                     "Nights": nights,   "Revenue_INR": spend})
    return pd.DataFrame(rows)

@st.cache_data
def gen_crm_data(seed=42):
    """Generate 200 CRM guest profiles with NPS correlated to loyalty tier."""
    np.random.seed(seed)
    tier_cfg = {
        "Silver":   (3,  7,  8.0, 0.7),
        "Gold":     (9,  25, 8.7, 0.5),
        "Platinum": (28, 60, 9.3, 0.4),
        "Epicure":  (61,100, 9.85,0.15),
    }
    diets = ["Vegetarian","Vegan","Jain","Gluten-Free","Halal","No Preference"]
    rows  = []
    for i in range(1, 201):
        tier  = np.random.choice(list(tier_cfg), p=[0.35,0.34,0.20,0.11])
        lo,hi,mu,sg = tier_cfg[tier]
        nps   = float(np.clip(np.round(np.random.normal(mu, sg), 1), 1, 10))
        stays = np.random.randint(lo, hi+1)
        rows.append({"Guest_ID":  f"GX-{i:04d}",
                     "Tier":      tier,
                     "Stays":     stays,
                     "NPS":       nps,
                     "Diet":      np.random.choice(diets,
                                  p=[0.24,0.10,0.12,0.12,0.10,0.32])})
    return pd.DataFrame(rows)

@st.cache_data
def gen_ems_data(seed=42):
    """Generate 24-hour IoT EMS time-series for 10 rooms (Floor 7)."""
    np.random.seed(seed)
    hours = list(range(24))
    occ_rows, no_iot_rows, iot_rows = [], [], []
    for h in hours:
        # Occupied load: peaks at evening
        base_occ  = 2.0 + 0.055 * abs(h - 4)
        occ_kw    = round(np.clip(np.random.normal(base_occ, 0.12), 1.9, 3.8), 3)
        # Vacant WITHOUT IoT (lights/HVAC left running at ~60% of occupied)
        no_iot_kw = round(occ_kw * np.random.uniform(0.55, 0.65), 3)
        # Vacant WITH IoT Eco-Mode (~10-20% of occupied)
        iot_kw    = round(occ_kw * np.random.uniform(0.08, 0.18), 3)
        occ_rows.append(occ_kw); no_iot_rows.append(no_iot_kw)
        iot_rows.append(iot_kw)
    return pd.DataFrame({
        "Hour":            hours,
        "Occupied":        occ_rows,
        "Vacant_No_IoT":   no_iot_rows,
        "Vacant_IoT":      iot_rows,
    })


# =============================================================================
#  SIDEBAR NAVIGATION
# =============================================================================

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 18px 0 10px 0;">
        <div style="font-family:'Playfair Display',serif; color:{GOLD};
                    font-size:1.6rem; letter-spacing:0.05em;">TAJ</div>
        <div style="font-family:'Inter',sans-serif; color:{MID};
                    font-size:0.65rem; letter-spacing:0.18em;
                    text-transform:uppercase; margin-top:2px;">
            Hotels & Resorts · IHCL
        </div>
        <div style="width:60%; height:1px; background:{GOLD}55;
                    margin:10px auto;"></div>
        <div style="font-family:'Inter',sans-serif; color:{GOLD}99;
                    font-size:0.62rem; letter-spacing:0.14em;
                    text-transform:uppercase;">Accelerate 2030</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="font-family:'Inter'; font-size:0.68rem; color:{MID};
                letter-spacing:0.1em; text-transform:uppercase;
                padding:12px 0 6px 0;">Navigation</div>
    """, unsafe_allow_html=True)

    page = st.radio(
        label="",
        options=[
            "🏛️  Executive Overview",
            "🏗️  ERP · Asset-Light Scaling",
            "📊  CPMS · Revenue & Profitability",
            "💎  CRM · Hyper-Personalisation",
            "🌿  IoT EMS · Eco-Efficiency",
        ],
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div style="position:absolute; bottom:24px; left:0; right:0;
                text-align:center;">
        <div style="font-family:'Inter'; font-size:0.6rem; color:{GOLD}55;
                    letter-spacing:0.08em;">MBA Strategic IS Project</div>
        <div style="font-family:'Inter'; font-size:0.58rem; color:{MID}66;
                    margin-top:3px;">© IHCL 2025 · Simulated Data</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
#  PAGE 1 — EXECUTIVE OVERVIEW
# =============================================================================

if "Executive Overview" in page:

    st.markdown(f"""
    <div style="padding: 8px 0 24px 0;">
        <div style="font-family:'Inter'; font-size:0.7rem; color:{GOLD}99;
                    letter-spacing:0.16em; text-transform:uppercase;">
            Strategic Information Systems · MBA Project
        </div>
        <h1 style="font-family:'Playfair Display',serif; color:{GOLD};
                   font-size:2.4rem; margin:6px 0 4px 0; line-height:1.1;">
            Accelerate 2030
        </h1>
        <div style="font-family:'Inter'; color:{MID}; font-size:0.88rem;
                    font-weight:300; letter-spacing:0.02em;">
            IHCL's technology-driven strategy for asset-light expansion,
            hyper-personalisation & ESG sustainability
        </div>
        <div style="width:80px; height:2px; background:{GOLD};
                    margin-top:14px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI cards row 1 ─────────────────────────────────────────────────────
    section_banner("2030 Vision Targets", "Key Performance Indicators")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Target Properties",    "700+",     "↑ from 340 today")
    c2.metric("Renewable Energy Goal","100%",     "By FY2030")
    c3.metric("Direct Revenue Share", "65%+",     "↑ from ~54% (2024)")
    c4.metric("NPS Target (Epicure)", "9.8 / 10", "Loyalty-led growth")

    st.markdown("<br>", unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Asset-Light Portfolio", "50%+",      "Managed & Franchised")
    c6.metric("Carbon Intensity Red.", "46%",        "Scope 1+2 by 2030")
    c7.metric("CRM Personalisation",   "1-to-1",    "Powered by IHCL One")
    c8.metric("IT Infra Investment",   "₹2,400 Cr", "FY2024-30 roadmap")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Strategic pillars ────────────────────────────────────────────────────
    section_banner("Four IS Modules Modelled in This Dashboard",
                   "Aligned to IHCL Strategic Pillars")

    p1, p2, p3, p4 = st.columns(4)

    def pillar(col, icon, system, desc, color):
        col.markdown(f"""
        <div style="background:linear-gradient(135deg,#1E1E32,#16162A);
                    border:1px solid {color}55; border-top:3px solid {color};
                    border-radius:8px; padding:18px 16px; height:160px;">
            <div style="font-size:1.5rem; margin-bottom:8px;">{icon}</div>
            <div style="font-family:'Playfair Display',serif; color:{color};
                        font-size:0.95rem; font-weight:600;">{system}</div>
            <div style="font-family:'Inter'; color:{MID}; font-size:0.75rem;
                        margin-top:6px; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    pillar(p1,"🏗️","ERP · Procurement",
           "Centralised bulk purchasing & vendor consolidation across all properties.",
           GOLD)
    pillar(p2,"📊","CPMS · Bookings",
           "Maximise direct channel revenue & reduce OTA commission leakage.",
           RUST)
    pillar(p3,"💎","CRM · Loyalty",
           "Hyper-personalisation via IHCL One to drive Epicure-tier upgrades & LTV.",
           SILVER)
    pillar(p4,"🌿","IoT EMS · Energy",
           "BMS-led energy automation to hit 100% renewable & cut OpEx per key.",
           GREEN)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Revenue waterfall chart ──────────────────────────────────────────────
    section_banner("Projected ROI Waterfall — IS Investment Impact (Per Property / Year)")
    measures = ["absolute","relative","relative","relative","total"]
    x_labels = ["Baseline Revenue","ERP Savings","CPMS Direct Uplift",
                 "CRM LTV Uplift","IoT OpEx Reduction"]
    y_vals   = [1_50_00_000, 18_00_000, 22_00_000, 14_00_000, 9_00_000]

    fig_wf = go.Figure(go.Waterfall(
        orientation="v", measure=measures,
        x=x_labels, y=y_vals,
        connector=dict(line=dict(color=GOLD+"66", width=1.5, dash="dot")),
        decreasing=dict(marker_color=RUST),
        increasing=dict(marker_color=GREEN),
        totals=dict(marker_color=GOLD),
        text=[inr(v) for v in y_vals], textposition="outside",
        textfont=dict(color=CREAM, size=10),
    ))
    plotly_layout(fig_wf,
        "Projected Value Addition per Property per Annum (₹)", height=380)
    fig_wf.update_traces(connector_line_color=GOLD+"44")
    fig_wf.update_layout(showlegend=False,
                          yaxis_tickformat=",.0f",
                          yaxis=dict(tickprefix="₹"))
    st.plotly_chart(fig_wf, use_container_width=True)

    insight("The integrated IS stack is projected to add ₹63 Lakhs per property "
            "annually through procurement savings (ERP), reduced OTA commission "
            "(CPMS), Epicure-tier revenue uplift (CRM), and energy OpEx reduction "
            "(IoT EMS) — totalling an estimated ₹2,100+ Cr group-wide by 2030 "
            "assuming 350 additional properties.")


# =============================================================================
#  PAGE 2 — ERP MODULE
# =============================================================================

elif "ERP" in page:

    st.markdown(f"""
    <h1>ERP · Asset-Light Scaling</h1>
    <p style="color:{MID}; font-size:0.85rem; margin-top:-10px;">
        Centralised Procurement Intelligence — Vendor Spend Analysis & Bulk Discount ROI
    </p>
    """, unsafe_allow_html=True)

    df = gen_erp_data()

    # ── Aggregations ─────────────────────────────────────────────────────────
    by_cat    = df.groupby("Category")["Amount_INR"].agg(
                    Total="sum", Count="count", Avg="mean"
                ).sort_values("Total", ascending=False)
    total_sp  = df["Amount_INR"].sum()
    overdue   = df[df["Status"]=="Overdue"]["Amount_INR"].sum()
    it_share  = by_cat.loc["IT Hardware","Total"] / total_sp * 100

    # ── KPIs ─────────────────────────────────────────────────────────────────
    section_banner("Procurement Snapshot", "100 Transactions · 6 Properties")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Procurement Spend",  inr(total_sp))
    k2.metric("IT Hardware Share",        f"{it_share:.1f}%",   "Infrastructure-first")
    k3.metric("Overdue AP Exposure",      inr(overdue),          "⚠ Escalation needed")
    k4.metric("Avg Invoice Value",        inr(df["Amount_INR"].mean()))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROI Slider ───────────────────────────────────────────────────────────
    section_banner("Dynamic ROI Calculator", "Centralised Bulk Discount Negotiation")
    col_sl, col_roi = st.columns([2, 1])

    with col_sl:
        discount_pct = st.slider(
            "🔧 Centralised Bulk Discount Negotiated (%)",
            min_value=0, max_value=35, value=12, step=1,
            help="Simulates the % cost reduction IHCL achieves by centralising "
                 "vendor negotiations across all properties."
        )
        st.markdown(f"""
        <div style="background:rgba(184,150,46,0.08); border:1px solid {GOLD}44;
                    border-radius:8px; padding:14px 18px; margin-top:8px;">
            <table style="width:100%; border-collapse:collapse;">
                <tr>
                    <td style="color:{MID}; font-size:0.78rem; padding:4px 0;
                               text-transform:uppercase; letter-spacing:0.06em;">
                        Baseline Spend (6 props)
                    </td>
                    <td style="color:{CREAM}; font-size:0.9rem; text-align:right;
                               font-weight:500;">
                        {inr(total_sp)}
                    </td>
                </tr>
                <tr>
                    <td style="color:{MID}; font-size:0.78rem; padding:4px 0;
                               text-transform:uppercase; letter-spacing:0.06em;">
                        Discount Applied
                    </td>
                    <td style="color:{GOLD}; font-size:0.9rem; text-align:right;
                               font-weight:600;">
                        {discount_pct}%
                    </td>
                </tr>
                <tr>
                    <td style="color:{MID}; font-size:0.78rem; padding:4px 0;
                               text-transform:uppercase; letter-spacing:0.06em;">
                        Savings — Group Total
                    </td>
                    <td style="color:{GREEN}; font-size:1.0rem; text-align:right;
                               font-weight:700;">
                        {inr(total_sp * discount_pct/100)}
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_roi:
        per_prop = (total_sp * discount_pct / 100) / 6
        roi_card("Annual Saving Per Property", inr(per_prop),
                 f"At {discount_pct}% bulk discount rate")
        roi_card("Projected Group Saving (2030)",
                 inr(per_prop * 700),
                 "Assumes 700-property portfolio")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ───────────────────────────────────────────────────────────────
    ch1, ch2 = st.columns([3, 2])

    with ch1:
        section_banner("Spend by Vendor Category")
        colors = [GOLD if c == "IT Hardware" else
                  RUST if c == "Engineering & Maintenance" else
                  GREEN if c == "Spa & Wellness" else SILVER
                  for c in by_cat.index]

        # Apply discount to show savings per category
        savings = by_cat["Total"] * discount_pct / 100

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=by_cat.index, x=by_cat["Total"],
            orientation="h", name="Gross Spend",
            marker_color=colors, marker_line_width=0,
            text=[inr(v) for v in by_cat["Total"]],
            textposition="outside", textfont=dict(size=9, color=CREAM),
        ))
        fig_bar.add_trace(go.Bar(
            y=by_cat.index, x=-savings,
            orientation="h", name=f"Bulk Discount Saving ({discount_pct}%)",
            marker_color=GREEN+"99", marker_line_width=0, base=by_cat["Total"],
        ))
        plotly_layout(fig_bar,
            "Procurement Spend by Category + Bulk Discount Savings", height=380)
        fig_bar.update_layout(barmode="overlay", showlegend=True,
                               xaxis_tickprefix="₹", xaxis_tickformat=",.0s")
        st.plotly_chart(fig_bar, use_container_width=True)

    with ch2:
        section_banner("Payment Status Breakdown")
        status_grp = df.groupby("Status")["Amount_INR"].sum().reset_index()
        colors_pie = {
            "Paid": GREEN, "Approved": GOLD,
            "Pending": RUST, "Overdue": "#CC3333"
        }
        fig_pie = go.Figure(go.Pie(
            labels=status_grp["Status"],
            values=status_grp["Amount_INR"],
            hole=0.52,
            marker_colors=[colors_pie.get(s, SILVER)
                           for s in status_grp["Status"]],
            textinfo="label+percent",
            textfont=dict(size=10, color=CREAM),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
        ))
        plotly_layout(fig_pie, "Spend by Payment Status", height=380)
        fig_pie.update_layout(
            legend=dict(orientation="h", y=-0.1),
            annotations=[dict(text="AP<br>Status", x=0.5, y=0.5,
                              font=dict(size=11, color=GOLD), showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    insight(f"IT Hardware dominates spend at {it_share:.0f}% of total procurement — "
            f"this is a deliberate investment signal, not overhead. A centralised "
            f"{discount_pct}% bulk discount yields {inr(per_prop)} per property annually, "
            f"scaling to {inr(per_prop * 700)} group-wide at 700 properties. "
            f"Overdue payables of {inr(overdue)} require immediate AP escalation to "
            f"protect supplier SLAs during the expansion phase.")


# =============================================================================
#  PAGE 3 — CPMS MODULE
# =============================================================================

elif "CPMS" in page:

    st.markdown(f"""
    <h1>CPMS · Revenue & Profitability</h1>
    <p style="color:{MID}; font-size:0.85rem; margin-top:-10px;">
        Cloud Property Management System — Channel Mix, Room Revenue & OTA Commission ROI
    </p>
    """, unsafe_allow_html=True)

    df = gen_cpms_data()
    OTA_COMMISSION = 0.18   # hardcoded 18% OTA fee benchmark

    # ── Aggregations ─────────────────────────────────────────────────────────
    by_chan  = df.groupby("Channel")["Revenue_INR"].agg(
                   Revenue="sum", Bookings="count", Avg="mean")
    total_rev       = df["Revenue_INR"].sum()
    ota_revenue     = by_chan.loc["OTA","Revenue"] if "OTA" in by_chan.index else 0
    ota_commission  = ota_revenue * OTA_COMMISSION
    direct_share    = by_chan.loc["Direct","Revenue"] / total_rev * 100

    # ── KPIs ─────────────────────────────────────────────────────────────────
    section_banner("Revenue Snapshot", "200 Bookings · 8 Properties")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Booking Revenue",  inr(total_rev))
    k2.metric("Direct Revenue Share",   f"{direct_share:.1f}%", "Target: 65%+")
    k3.metric("OTA Commission Leakage", inr(ota_commission),     f"At {OTA_COMMISSION*100:.0f}% rate")
    k4.metric("Avg Revenue / Booking",  inr(df["Revenue_INR"].mean()))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROI Slider ───────────────────────────────────────────────────────────
    section_banner("Dynamic ROI Calculator", "OTA → Direct Channel Shift")
    col_sl, col_roi = st.columns([2, 1])

    with col_sl:
        shift_pct = st.slider(
            "📈 Shift OTA Bookings to Direct Channel (%)",
            min_value=0, max_value=100, value=25, step=5,
            help="What % of current OTA bookings are converted to direct (brand.com / loyalty). "
                 "Commission saved = shifted revenue × 18% OTA rate."
        )

        shifted_rev       = ota_revenue * (shift_pct / 100)
        commission_saved  = shifted_rev * OTA_COMMISSION
        new_direct_share  = ((by_chan.loc["Direct","Revenue"] + shifted_rev)
                             / total_rev * 100)

        st.markdown(f"""
        <div style="background:rgba(184,150,46,0.08); border:1px solid {GOLD}44;
                    border-radius:8px; padding:14px 18px; margin-top:8px;">
            <table style="width:100%; border-collapse:collapse;">
                {"".join([
                    f"<tr><td style='color:{MID};font-size:0.78rem;padding:5px 0;"
                    f"text-transform:uppercase;letter-spacing:0.06em;'>{lbl}</td>"
                    f"<td style='color:{val_color};font-size:0.9rem;text-align:right;"
                    f"font-weight:600;'>{val}</td></tr>"
                    for lbl, val, val_color in [
                        ("OTA Revenue Baseline",    inr(ota_revenue),         CREAM),
                        ("OTA Bookings Shifted",    f"{shift_pct}%",           GOLD),
                        ("Revenue Moved to Direct", inr(shifted_rev),         GOLD),
                        ("Commission Saved (18%)",  inr(commission_saved),    GREEN),
                        ("New Direct Revenue Share",f"{new_direct_share:.1f}%",GREEN),
                    ]
                ])}
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_roi:
        roi_card("Commission Saved Per Property", inr(commission_saved / 6),
                 f"{shift_pct}% OTA → Direct shift")
        roi_card("Annual Bottom-Line Gain (Group)",
                 inr(commission_saved / 6 * 700),
                 "At 700-property scale")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ───────────────────────────────────────────────────────────────
    ch1, ch2 = st.columns([3, 2])

    with ch1:
        section_banner("Revenue by Channel & Room Type")
        pivot = (df.groupby(["Channel","Room_Type"])["Revenue_INR"]
                   .sum().reset_index())
        fig_grp = go.Figure()
        room_colors = {"Deluxe": NAVY, "Taj Club": GOLD, "Suite": RUST}
        for room in ["Deluxe","Taj Club","Suite"]:
            sub = pivot[pivot["Room_Type"]==room]
            fig_grp.add_trace(go.Bar(
                name=room, x=sub["Channel"], y=sub["Revenue_INR"],
                marker_color=room_colors[room],
                marker_line_color=GOLD+"44", marker_line_width=0.8,
                text=[inr(v) for v in sub["Revenue_INR"]],
                textposition="inside", textfont=dict(size=8.5, color=CREAM),
            ))
        plotly_layout(fig_grp, "Revenue by Booking Channel & Room Type", height=380)
        fig_grp.update_layout(barmode="group",
                               yaxis_tickprefix="₹", yaxis_tickformat=",.0s",
                               bargap=0.25, bargroupgap=0.06)
        st.plotly_chart(fig_grp, use_container_width=True)

    with ch2:
        section_banner("Channel Revenue Distribution")
        fig_donut = go.Figure(go.Pie(
            labels=by_chan.index,
            values=by_chan["Revenue"],
            hole=0.55,
            marker_colors=[GREEN if c=="Direct" else
                           RUST if c=="OTA" else GOLD
                           for c in by_chan.index],
            textinfo="label+percent",
            textfont=dict(size=10, color=CREAM),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
        ))
        plotly_layout(fig_donut, "Revenue Split by Channel", height=380)
        fig_donut.update_layout(
            annotations=[dict(text="Channel<br>Mix", x=0.5, y=0.5,
                              font=dict(size=11, color=GOLD), showarrow=False)],
            legend=dict(orientation="h", y=-0.1),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    insight(f"OTA commission leakage stands at {inr(ota_commission)} on the current "
            f"booking mix. A {shift_pct}% channel conversion to Direct saves "
            f"{inr(commission_saved)} group-wide — pure bottom-line margin recovery. "
            f"Suites generate the highest avg revenue per booking, validating IHCL's "
            f"premium-room push. Investing in the IHCL One loyalty app and brand.com "
            f"merchandising is the single highest-ROI IS lever in the CPMS stack.")


# =============================================================================
#  PAGE 4 — CRM MODULE
# =============================================================================

elif "CRM" in page:

    st.markdown(f"""
    <h1>CRM · Hyper-Personalisation</h1>
    <p style="color:{MID}; font-size:0.85rem; margin-top:-10px;">
        IHCL One Loyalty Engine — Tier Upgrade ROI, NPS Correlation & LTV Modelling
    </p>
    """, unsafe_allow_html=True)

    df = gen_crm_data()
    EPICURE_LTV_UPLIFT = 45_000   # ₹45,000 extra ancillary spend per Epicure guest

    # ── Aggregations ─────────────────────────────────────────────────────────
    by_tier = (df.groupby("Tier")
                 .agg(Avg_NPS=("NPS","mean"), Count=("Guest_ID","count"),
                      Avg_Stays=("Stays","mean"))
                 .reindex(["Silver","Gold","Platinum","Epicure"]))
    silver_count  = int(by_tier.loc["Silver","Count"])
    epicure_count = int(by_tier.loc["Epicure","Count"])
    overall_nps   = df["NPS"].mean()

    # ── KPIs ─────────────────────────────────────────────────────────────────
    section_banner("Guest Loyalty Snapshot", "200 Profiles · IHCL One CRM")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Overall Avg NPS",         f"{overall_nps:.2f} / 10")
    k2.metric("Epicure Avg NPS",
              f"{by_tier.loc['Epicure','Avg_NPS']:.2f}",
              f"vs Silver {by_tier.loc['Silver','Avg_NPS']:.2f}")
    k3.metric("Silver Tier Guests",      f"{silver_count}",
              "Upgrade pipeline")
    k4.metric("Epicure LTV Premium",     inr(EPICURE_LTV_UPLIFT),
              "Extra ancillary per guest")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROI Slider ───────────────────────────────────────────────────────────
    section_banner("Dynamic ROI Calculator", "Silver → Epicure Tier Upgrade Conversion")
    col_sl, col_roi = st.columns([2, 1])

    with col_sl:
        upgrade_pct = st.slider(
            "💎 Silver → Epicure Upgrade Conversion Rate (%)",
            min_value=0, max_value=50, value=15, step=1,
            help="% of Silver-tier guests successfully upgraded to Epicure "
                 "via personalised CRM journeys, F&B offers and exclusive events."
        )

        upgraded_guests   = int(silver_count * upgrade_pct / 100)
        ltv_uplift_total  = upgraded_guests * EPICURE_LTV_UPLIFT
        nps_bump          = ((by_tier.loc["Epicure","Avg_NPS"] -
                              by_tier.loc["Silver","Avg_NPS"])
                             * upgrade_pct / 100)
        new_avg_nps       = overall_nps + nps_bump * 0.3

        st.markdown(f"""
        <div style="background:rgba(184,150,46,0.08); border:1px solid {GOLD}44;
                    border-radius:8px; padding:14px 18px; margin-top:8px;">
            <table style="width:100%; border-collapse:collapse;">
                {"".join([
                    f"<tr><td style='color:{MID};font-size:0.78rem;padding:5px 0;"
                    f"text-transform:uppercase;letter-spacing:0.06em;'>{lbl}</td>"
                    f"<td style='color:{vc};font-size:0.9rem;text-align:right;"
                    f"font-weight:600;'>{val}</td></tr>"
                    for lbl, val, vc in [
                        ("Silver Guests in Pipeline",     str(silver_count),         CREAM),
                        ("Upgrade Rate Applied",           f"{upgrade_pct}%",         GOLD),
                        ("Guests Upgraded to Epicure",     str(upgraded_guests),      GOLD),
                        ("LTV Uplift @ ₹45K Each",        inr(ltv_uplift_total),     GREEN),
                        ("Projected New Avg NPS",          f"{new_avg_nps:.2f} / 10", GREEN),
                    ]
                ])}
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_roi:
        roi_card("Ancillary Revenue Uplift", inr(ltv_uplift_total),
                 f"{upgraded_guests} guests × ₹45K LTV delta")
        roi_card("Group-Wide LTV Opportunity",
                 inr(ltv_uplift_total * (700 / 6)),
                 "Scaled to 700 properties")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ───────────────────────────────────────────────────────────────
    ch1, ch2 = st.columns([3, 2])

    with ch1:
        section_banner("NPS Score Distribution by Loyalty Tier")
        tier_colors = {
            "Silver": SILVER, "Gold": GOLD,
            "Platinum": "#C0C0C0", "Epicure": RUST
        }
        fig_box = go.Figure()
        for tier in ["Silver","Gold","Platinum","Epicure"]:
            sub = df[df["Tier"]==tier]["NPS"]
            fig_box.add_trace(go.Box(
                y=sub, name=tier,
                marker_color=tier_colors[tier],
                line_color=tier_colors[tier],
                fillcolor=tier_colors[tier]+"33",
                boxmean="sd",
                hovertemplate=f"<b>{tier}</b><br>NPS: %{{y}}<extra></extra>",
            ))
        plotly_layout(fig_box, "NPS Distribution by IHCL One Loyalty Tier", height=400)
        fig_box.update_layout(
            yaxis=dict(range=[4, 11], title="NPS Score"),
            xaxis_title="Loyalty Tier",
        )
        # Benchmark line at 9
        fig_box.add_hline(y=9.0, line_dash="dot", line_color=GREEN,
                          annotation_text="  Target NPS: 9.0",
                          annotation_font=dict(color=GREEN, size=9))
        st.plotly_chart(fig_box, use_container_width=True)

    with ch2:
        section_banner("Lifetime Stays & Avg NPS by Tier")
        fig_sc = go.Figure()
        for tier in ["Silver","Gold","Platinum","Epicure"]:
            sub = df[df["Tier"]==tier]
            fig_sc.add_trace(go.Scatter(
                x=sub["Stays"], y=sub["NPS"],
                mode="markers", name=tier,
                marker=dict(color=tier_colors[tier], size=6,
                            opacity=0.65,
                            line=dict(width=0.5, color=CREAM+"44")),
                hovertemplate=(f"<b>{tier}</b><br>Stays: %{{x}}"
                               f"<br>NPS: %{{y}}<extra></extra>"),
            ))
        plotly_layout(fig_sc, "NPS vs. Lifetime Stays", height=400)
        fig_sc.update_layout(
            xaxis_title="Lifetime Stays",
            yaxis_title="NPS Score",
            yaxis=dict(range=[4, 11]),
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    insight(f"NPS rises in a statistically consistent staircase: Silver ({by_tier.loc['Silver','Avg_NPS']:.1f}) "
            f"→ Gold ({by_tier.loc['Gold','Avg_NPS']:.1f}) → Platinum ({by_tier.loc['Platinum','Avg_NPS']:.1f}) "
            f"→ Epicure ({by_tier.loc['Epicure','Avg_NPS']:.1f}). "
            f"A {upgrade_pct}% Silver upgrade conversion unlocks {inr(ltv_uplift_total)} in "
            f"ancillary LTV. CRM-driven hyper-personalisation — pre-arrival F&B configuration, "
            f"room preference auto-loading, and butler journey orchestration — is the primary "
            f"lever to accelerate tier migration and protect NPS at scale.")


# =============================================================================
#  PAGE 5 — IoT EMS MODULE
# =============================================================================

elif "IoT EMS" in page:

    st.markdown(f"""
    <h1>IoT EMS · Eco-Efficiency</h1>
    <p style="color:{MID}; font-size:0.85rem; margin-top:-10px;">
        Building Management System — 24hr Energy Intelligence, Eco-Mode Savings & Carbon ROI
    </p>
    """, unsafe_allow_html=True)

    df = gen_ems_data()
    COST_PER_KWH   = 10.0    # ₹10/kWh commercial electricity tariff (hardcoded)
    ROOMS_PER_PROP = 200     # average property size
    DAYS_PER_YEAR  = 365

    # ── Aggregations ─────────────────────────────────────────────────────────
    floor_total_occ     = df["Occupied"].sum()
    floor_total_no_iot  = df["Vacant_No_IoT"].sum()
    floor_total_iot     = df["Vacant_IoT"].sum()
    daily_saving_10rm   = floor_total_no_iot - floor_total_iot
    occupancy_rate      = 0.72   # benchmark 72% average

    # Annual savings per property (scale from 10 rooms to full property)
    vacant_hours        = 24 * DAYS_PER_YEAR * ROOMS_PER_PROP * (1 - occupancy_rate)
    no_iot_annual_kwh   = (floor_total_no_iot / 10) * vacant_hours
    iot_annual_kwh      = (floor_total_iot    / 10) * vacant_hours
    kwh_saved           = no_iot_annual_kwh - iot_annual_kwh
    annual_saving_inr   = kwh_saved * COST_PER_KWH

    # ── KPIs ─────────────────────────────────────────────────────────────────
    section_banner("Energy Snapshot", "24hr Time-Series · Floor 7 · 10 Rooms")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Occupied Avg Load",     f"{df['Occupied'].mean():.2f} kWh/hr")
    k2.metric("Vacant (No IoT) Load",  f"{df['Vacant_No_IoT'].mean():.2f} kWh/hr")
    k3.metric("Vacant (IoT Eco) Load", f"{df['Vacant_IoT'].mean():.2f} kWh/hr",
              f"↓{(1 - df['Vacant_IoT'].mean()/df['Vacant_No_IoT'].mean())*100:.0f}% reduction")
    k4.metric("Est. Annual OpEx Saved", inr(annual_saving_inr),
              "Per property · ₹10/kWh")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROI Slider ───────────────────────────────────────────────────────────
    section_banner("Dynamic ROI Calculator", "IoT Efficiency Rate & Annual Savings")
    col_sl, col_roi = st.columns([2, 1])

    with col_sl:
        eff_rate = st.slider(
            "🌿 IoT Efficiency Rate (% of Vacant kWh Eliminated)",
            min_value=50, max_value=95, value=82, step=1,
            help="How effectively the BMS/IoT system eliminates wasted energy "
                 "in vacant rooms. 82% = industry-leading best practice."
        )

        # Recalculate with new efficiency
        adjusted_iot_kwh     = df["Vacant_No_IoT"] * (1 - eff_rate/100)
        adj_daily_saving     = (df["Vacant_No_IoT"] - adjusted_iot_kwh).sum()
        adj_annual_kwh_saved = (floor_total_no_iot/10 - adjusted_iot_kwh.mean()) * vacant_hours
        adj_annual_inr       = adj_annual_kwh_saved * COST_PER_KWH
        carbon_saved_tonnes  = adj_annual_kwh_saved * 0.82 / 1000  # 0.82 kg CO2/kWh India grid

        st.markdown(f"""
        <div style="background:rgba(46,125,90,0.10); border:1px solid {GREEN}55;
                    border-radius:8px; padding:14px 18px; margin-top:8px;">
            <table style="width:100%; border-collapse:collapse;">
                {"".join([
                    f"<tr><td style='color:{MID};font-size:0.78rem;padding:5px 0;"
                    f"text-transform:uppercase;letter-spacing:0.06em;'>{lbl}</td>"
                    f"<td style='color:{vc};font-size:0.9rem;text-align:right;"
                    f"font-weight:600;'>{val}</td></tr>"
                    for lbl, val, vc in [
                        ("Electricity Rate (Hardcoded)",   "₹10 / kWh",               CREAM),
                        ("IoT Efficiency Rate Applied",    f"{eff_rate}%",             GOLD),
                        ("Annual kWh Saved (Per Property)",f"{adj_annual_kwh_saved:,.0f} kWh",GREEN),
                        ("Annual ₹ OpEx Reduction",        inr(adj_annual_inr),        GREEN),
                        ("Carbon Avoided (tCO₂e / year)",  f"{carbon_saved_tonnes:,.0f} tonnes",GREEN),
                    ]
                ])}
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col_roi:
        roi_card("Annual OpEx Saving", inr(adj_annual_inr),
                 f"Per property · {eff_rate}% IoT efficiency")
        roi_card("Group Carbon Avoided",
                 f"{carbon_saved_tonnes * 700:,.0f} tCO₂e",
                 "700 properties × annual avoided")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Main Area Chart ───────────────────────────────────────────────────────
    section_banner("24-Hour Power Consumption Profile",
                   "Occupied vs. Vacant (No IoT) vs. Vacant (IoT Eco-Mode)")

    fig_area = go.Figure()

    # Savings zone fill
    fig_area.add_trace(go.Scatter(
        x=df["Hour"], y=df["Vacant_No_IoT"],
        fill=None, mode="lines",
        line=dict(width=0, color="transparent"),
        showlegend=False, hoverinfo="skip",
    ))
    fig_area.add_trace(go.Scatter(
        x=df["Hour"], y=adjusted_iot_kwh,
        fill="tonexty", mode="none",
        fillcolor=GREEN+"28",
        name="IoT Savings Zone",
        hoverinfo="skip",
    ))

    # Occupied
    fig_area.add_trace(go.Scatter(
        x=df["Hour"], y=df["Occupied"],
        mode="lines+markers", name="Occupied Load",
        line=dict(color=RUST, width=2.5),
        marker=dict(size=5, color=RUST, symbol="circle",
                    line=dict(width=1.5, color=CREAM+"66")),
        hovertemplate="Hour %{x}:00 | Occupied: %{y:.2f} kWh<extra></extra>",
    ))

    # Vacant No IoT
    fig_area.add_trace(go.Scatter(
        x=df["Hour"], y=df["Vacant_No_IoT"],
        mode="lines+markers", name="Vacant (No IoT)",
        line=dict(color=MID, width=1.8, dash="dot"),
        marker=dict(size=4, color=MID),
        hovertemplate="Hour %{x}:00 | Vacant No IoT: %{y:.2f} kWh<extra></extra>",
    ))

    # Vacant IoT Eco (adjusted)
    fig_area.add_trace(go.Scatter(
        x=df["Hour"], y=adjusted_iot_kwh,
        mode="lines+markers", name="Vacant (IoT Eco-Mode)",
        line=dict(color=GREEN, width=2.2),
        marker=dict(size=5, color=GREEN,
                    line=dict(width=1.5, color=CREAM+"66")),
        hovertemplate="Hour %{x}:00 | IoT Eco: %{y:.2f} kWh<extra></extra>",
    ))

    plotly_layout(fig_area,
        "Average Hourly Power Draw: Occupied vs. Vacant Scenarios (kWh)", height=420)
    fig_area.update_layout(
        xaxis=dict(title="Hour of Day", tickmode="linear",
                   tick0=0, dtick=2,
                   ticktext=[f"{h:02d}:00" for h in range(0,24,2)],
                   tickvals=list(range(0,24,2))),
        yaxis=dict(title="Avg Power (kWh / Room)"),
        hovermode="x unified",
    )
    # Checkout trough annotation
    fig_area.add_vrect(x0=9, x1=14, fillcolor=GOLD+"0D",
                       line_width=0,
                       annotation_text="  Checkout Trough", annotation_position="top left",
                       annotation_font=dict(color=GOLD, size=9))
    # Peak annotation
    fig_area.add_vrect(x0=18, x1=21, fillcolor=RUST+"14",
                       line_width=0,
                       annotation_text="  Evening Peak  ", annotation_position="top right",
                       annotation_font=dict(color=RUST, size=9))

    st.plotly_chart(fig_area, use_container_width=True)

    # ── Hourly savings bar ────────────────────────────────────────────────────
    section_banner("Hourly kWh Saved by IoT Eco-Mode vs. Non-IoT Baseline")
    hourly_savings = df["Vacant_No_IoT"] - adjusted_iot_kwh
    fig_sav = go.Figure(go.Bar(
        x=df["Hour"], y=hourly_savings,
        marker_color=[GREEN if v > hourly_savings.mean() else GREEN+"88"
                      for v in hourly_savings],
        marker_line_width=0,
        hovertemplate="Hour %{x}:00<br>Saving: %{y:.3f} kWh<extra></extra>",
    ))
    plotly_layout(fig_sav, "kWh Saved Per Hour (IoT Eco-Mode vs. No IoT Baseline)", height=280)
    fig_sav.add_hline(y=hourly_savings.mean(), line_dash="dot",
                      line_color=GOLD, line_width=1.5,
                      annotation_text=f"  Avg saving: {hourly_savings.mean():.3f} kWh",
                      annotation_font=dict(color=GOLD, size=9))
    fig_sav.update_layout(yaxis_title="kWh Saved", xaxis_title="Hour of Day",
                           showlegend=False)
    st.plotly_chart(fig_sav, use_container_width=True)

    insight(f"At a {eff_rate}% IoT efficiency rate, the BMS eliminates "
            f"{adj_annual_kwh_saved:,.0f} kWh per property annually — "
            f"translating to {inr(adj_annual_inr)} in OpEx savings at the "
            f"₹10/kWh commercial tariff. Across 700 properties, this avoids "
            f"{carbon_saved_tonnes * 700:,.0f} tCO₂e per year, directly "
            f"supporting IHCL's FY2030 46% carbon intensity reduction target "
            f"and its commitment to 100% renewable energy. The checkout trough "
            f"(09:00–14:00) is the peak BMS savings window — automated Eco-Mode "
            f"and pre-arrival pre-cooling cycles must be orchestrated here.")
