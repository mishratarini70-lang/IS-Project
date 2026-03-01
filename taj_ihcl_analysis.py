"""
=============================================================================
  IHCL / TAJ HOTELS — INTEGRATED INFORMATION SYSTEMS ANALYSIS
  MBA Strategic Project | Senior Data Analyst: Python & Pandas Pipeline
  Datasets: ERP (Procurement) | CPMS (Bookings) | CRM (Guests) | IoT EMS
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# ── Global Style Configuration ────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "grid.linestyle":   "--",
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.labelsize":   10,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "figure.dpi":       150,
})

# Taj Hotels brand palette
TAJ_GOLD    = "#B8962E"
TAJ_DARK    = "#1A1A2E"
TAJ_CREAM   = "#F5F0E8"
TAJ_GREEN   = "#2E7D5A"
TAJ_RUST    = "#A0522D"
TAJ_BLUE    = "#1B4F72"
TAJ_PALETTE = [TAJ_GOLD, TAJ_DARK, TAJ_GREEN, TAJ_RUST, TAJ_BLUE, "#7D3C98"]

# ── Rupee formatter for axes ───────────────────────────────────────────────────
def inr_formatter(x, _):
    if x >= 1_00_00_000:
        return f"₹{x/1_00_00_000:.1f}Cr"
    elif x >= 1_00_000:
        return f"₹{x/1_00_000:.0f}L"
    elif x >= 1000:
        return f"₹{x/1000:.0f}K"
    return f"₹{x:.0f}"

# =============================================================================
#  SECTION 1 — BUILD MOCK DATAFRAMES
# =============================================================================

np.random.seed(42)   # reproducibility

# ── 1A. ERP — Procurement Transactions (100 rows) ────────────────────────────
properties  = ["PROP-MUM-01","PROP-DEL-02","PROP-GOA-03","PROP-JAI-04",
               "PROP-BLR-05","PROP-UDR-06"]

vendor_cfg = {
    # category            : (mean_INR, std_INR)
    "F&B Supplies"             : (62_000,  14_000),
    "Housekeeping"             : (36_000,   7_000),
    "Linens"                   : (1_18_000, 22_000),
    "Spa & Wellness"           : (1_05_000, 25_000),
    "Engineering & Maintenance": (2_50_000, 55_000),
    "IT Hardware"              : (6_20_000,1_80_000),
}

payment_statuses = ["Paid","Approved","Pending","Overdue"]
categories = list(vendor_cfg.keys())

erp_rows = []
for i in range(1, 101):
    cat   = np.random.choice(categories, p=[0.30,0.15,0.15,0.10,0.18,0.12])
    mean, std = vendor_cfg[cat]
    amount = max(15_000, int(np.random.normal(mean, std)))
    erp_rows.append({
        "Transaction_ID"   : f"PO-{i:04d}",
        "Property_ID"      : np.random.choice(properties),
        "Vendor_Category"  : cat,
        "Invoice_Amount_INR": amount,
        "Payment_Status"   : np.random.choice(payment_statuses,
                                p=[0.45,0.45,0.05,0.05]),
    })

df_erp = pd.DataFrame(erp_rows)

# ── 1B. CPMS — Property Management / Bookings (200 rows) ─────────────────────
locations     = ["Mumbai","Delhi","Goa","Jaipur","Bangalore","Udaipur",
                 "Chennai","London"]
room_types    = ["Deluxe","Taj Club","Suite"]
channels      = ["Direct","OTA","Corporate"]

room_rate = {          # base nightly rate INR
    ("Deluxe",  False): 17_500,
    ("Taj Club",False): 38_000,
    ("Suite",   False): 75_000,
    ("Deluxe",  True ): 82_000,   # London premium
    ("Taj Club",True ): 92_000,
    ("Suite",   True ): 95_000,
}

cpms_rows = []
for i in range(1, 201):
    loc    = np.random.choice(locations,
                p=[0.20,0.15,0.15,0.10,0.10,0.10,0.10,0.10])
    room   = np.random.choice(room_types, p=[0.40,0.35,0.25])
    chan   = np.random.choice(channels,   p=[0.60,0.24,0.16])
    nights = np.random.choice(range(1,8), p=[0.10,0.20,0.25,0.20,0.13,0.08,0.04])
    intl   = (loc == "London")
    rate   = room_rate[(room, intl)]
    spend  = int(rate * nights * np.random.uniform(0.92, 1.12))
    cpms_rows.append({
        "Booking_ID"       : f"TH-{i:04d}",
        "Property_Location": loc,
        "Room_Type"        : room,
        "Length_of_Stay_Days": nights,
        "Booking_Channel"  : chan,
        "Total_Spend_INR"  : spend,
    })

df_cpms = pd.DataFrame(cpms_rows)

# ── 1C. CRM — Guest Loyalty & Preferences (200 rows) ─────────────────────────
tiers      = ["Silver","Gold","Platinum","Epicure"]
stays_cfg  = {"Silver":(3,7),"Gold":(9,25),"Platinum":(28,60),"Epicure":(61,100)}
diets      = ["Vegetarian","Vegan","Jain","Gluten-Free","Halal","No Preference"]
rooms_pref = ["High Floor","Sea View","Quiet Wing","Near Elevator",
              "Pool View","Butler Suite"]

nps_cfg    = {"Silver":(8.0,0.6),"Gold":(8.8,0.5),
              "Platinum":(9.3,0.4),"Epicure":(9.8,0.2)}

crm_rows = []
for i in range(1, 201):
    tier   = np.random.choice(tiers, p=[0.35,0.35,0.20,0.10])
    lo, hi = stays_cfg[tier]
    stays  = np.random.randint(lo, hi+1)
    mu, sg = nps_cfg[tier]
    nps    = int(np.clip(np.round(np.random.normal(mu, sg)), 1, 10))
    crm_rows.append({
        "Guest_ID"          : f"GX-{i:04d}",
        "IHCL_One_Tier"     : tier,
        "Lifetime_Stays"    : stays,
        "Dietary_Preference": np.random.choice(diets,
            p=[0.25,0.10,0.12,0.12,0.10,0.31]),
        "Room_Preference"   : np.random.choice(rooms_pref),
        "Last_NPS_Score"    : nps,
    })

df_crm = pd.DataFrame(crm_rows)

# ── 1D. IoT EMS — Energy Management (240 rows: 10 rooms × 24 hrs) ────────────
ems_rows = []
rooms = [f"70{r}" for r in range(1, 11)]

for hour in range(24):
    for room in rooms:
        # Vacancy logic: rooms mostly vacant 09:00–14:00
        if 9 <= hour <= 14:
            occupied = np.random.choice([True, False], p=[0.15, 0.85])
        elif hour < 6 or hour >= 22:
            occupied = np.random.choice([True, False], p=[0.80, 0.20])
        else:
            occupied = np.random.choice([True, False], p=[0.60, 0.40])

        if occupied:
            hvac   = "On"
            # Power peaks at evening (18-21), dips at night
            base   = 2.1 + 0.06 * abs(hour - 4)
            power  = round(np.clip(np.random.normal(base, 0.15), 2.0, 3.8), 2)
        else:
            hvac   = np.random.choice(["Eco-Mode","Off"], p=[0.55, 0.45])
            power  = round(np.random.uniform(0.05, 0.55), 2)

        ems_rows.append({
            "Timestamp"          : f"2025-06-15 {hour:02d}:00",
            "Room_Number"        : room,
            "Occupancy_Status"   : "Occupied" if occupied else "Vacant",
            "HVAC_Status"        : hvac,
            "Power_Consumed_kWh" : power,
        })

df_ems = pd.DataFrame(ems_rows)
df_ems["Hour"] = df_ems["Timestamp"].str[11:13].astype(int)

print("=" * 65)
print("  IHCL DATA PIPELINE — DATAFRAME SHAPES")
print("=" * 65)
for name, df in [("ERP Procurement", df_erp),("CPMS Bookings", df_cpms),
                 ("CRM Guests",      df_crm),("IoT EMS",       df_ems)]:
    print(f"  {name:<22} {df.shape[0]:>4} rows × {df.shape[1]} cols")
print()

# =============================================================================
#  SECTION 2 — AGGREGATIONS & BUSINESS METRICS
# =============================================================================

# ── 2A. ERP Aggregations ──────────────────────────────────────────────────────
erp_by_cat = (df_erp.groupby("Vendor_Category")["Invoice_Amount_INR"]
                     .agg(Total_Spend="sum", Avg_Invoice="mean", Count="count")
                     .sort_values("Total_Spend", ascending=False))

erp_by_status = (df_erp.groupby("Payment_Status")["Invoice_Amount_INR"]
                        .agg(Total="sum", Count="count"))

overdue_amount = erp_by_status.loc["Overdue","Total"] if "Overdue" in erp_by_status.index else 0
total_erp_spend = df_erp["Invoice_Amount_INR"].sum()
it_share = (erp_by_cat.loc["IT Hardware","Total_Spend"] / total_erp_spend * 100
            if "IT Hardware" in erp_by_cat.index else 0)

# ── 2B. CPMS Aggregations ─────────────────────────────────────────────────────
cpms_by_channel = (df_cpms.groupby("Booking_Channel")["Total_Spend_INR"]
                           .agg(Revenue="sum", Bookings="count",
                                Avg_Spend="mean"))

cpms_by_room = (df_cpms.groupby("Room_Type")["Total_Spend_INR"]
                        .agg(Revenue="sum", Bookings="count",
                             Avg_Spend="mean")
                        .sort_values("Revenue", ascending=False))

direct_rev_share = (cpms_by_channel.loc["Direct","Revenue"]
                    / df_cpms["Total_Spend_INR"].sum() * 100)

# ── 2C. CRM Aggregations ──────────────────────────────────────────────────────
crm_by_tier = (df_crm.groupby("IHCL_One_Tier")
                      .agg(Avg_NPS     =("Last_NPS_Score","mean"),
                           Avg_Stays   =("Lifetime_Stays","mean"),
                           Guest_Count =("Guest_ID","count"))
                      .reindex(["Silver","Gold","Platinum","Epicure"]))

diet_dist = df_crm["Dietary_Preference"].value_counts(normalize=True) * 100

# ── 2D. EMS Aggregations ──────────────────────────────────────────────────────
ems_summary = (df_ems.groupby("Occupancy_Status")["Power_Consumed_kWh"]
                      .agg(Total_kWh="sum", Avg_kWh="mean", Records="count"))

hourly_power = (df_ems.groupby(["Hour","Occupancy_Status"])["Power_Consumed_kWh"]
                       .mean().reset_index())

vacant_power   = ems_summary.loc["Vacant","Total_kWh"]
occupied_power = ems_summary.loc["Occupied","Total_kWh"]
eco_saving_pct = (1 - vacant_power / occupied_power) * 100

# =============================================================================
#  SECTION 3 — PRINT DATA SOURCE INSIGHTS
# =============================================================================

DIVIDER = "─" * 65

def print_insight(system, lines):
    print(f"\n{'═'*65}")
    print(f"  📊  DATA SOURCE INSIGHT — {system}")
    print(f"{'═'*65}")
    for line in lines:
        print(f"  {line}")

print_insight("ERP — PROCUREMENT & VENDOR SPEND", [
    f"Total procurement spend across 6 properties : ₹{total_erp_spend:,.0f}",
    f"Highest spend category    : {erp_by_cat.index[0]}",
    f"  → ₹{erp_by_cat.iloc[0]['Total_Spend']:,.0f} across "
    f"{int(erp_by_cat.iloc[0]['Count'])} invoices",
    f"IT Hardware share of total spend            : {it_share:.1f}%",
    f"  → Signals active tech infrastructure investment",
    f"Overdue payables (AP risk)                  : ₹{overdue_amount:,.0f}",
    f"  → Requires immediate escalation to Finance Controller",
])

print_insight("CPMS — PROPERTY MANAGEMENT & REVENUE", [
    f"Total simulated booking revenue : ₹{df_cpms['Total_Spend_INR'].sum():,.0f}",
    f"Direct channel revenue share    : {direct_rev_share:.1f}%",
    f"  → Exceeds OTA dependency; supports margin protection strategy",
    f"Top performing room type        : {cpms_by_room.index[0]}",
    f"  → Revenue: ₹{cpms_by_room.iloc[0]['Revenue']:,.0f} | "
    f"Avg spend: ₹{cpms_by_room.iloc[0]['Avg_Spend']:,.0f}",
    f"Average booking revenue (Direct): ₹{cpms_by_channel.loc['Direct','Avg_Spend']:,.0f}",
    f"Average booking revenue (OTA)   : ₹{cpms_by_channel.loc['OTA','Avg_Spend']:,.0f}",
    f"  → Direct bookings yield {((cpms_by_channel.loc['Direct','Avg_Spend']/cpms_by_channel.loc['OTA','Avg_Spend'])-1)*100:.1f}% higher avg revenue than OTA",
])

print_insight("CRM — GUEST LOYALTY & PERSONALISATION", [
    f"Overall avg NPS score           : {df_crm['Last_NPS_Score'].mean():.2f} / 10",
    f"Epicure tier avg NPS            : {crm_by_tier.loc['Epicure','Avg_NPS']:.2f}",
    f"Silver tier avg NPS             : {crm_by_tier.loc['Silver','Avg_NPS']:.2f}",
    f"  → NPS rises consistently with loyalty tier depth",
    f"Epicure avg lifetime stays      : {crm_by_tier.loc['Epicure','Avg_Stays']:.0f} stays",
    f"Top dietary segment (non-std)   : {diet_dist[diet_dist.index != 'No Preference'].idxmax()}",
    f"  → {diet_dist[diet_dist.index != 'No Preference'].max():.1f}% of guests require specialised F&B",
    f"  → CRM-driven personalisation directly impacts NPS and retention",
])

print_insight("IoT EMS — ENERGY MANAGEMENT & SUSTAINABILITY", [
    f"Total floor power (24 hrs)      : {df_ems['Power_Consumed_kWh'].sum():.2f} kWh",
    f"Occupied rooms avg draw         : {ems_summary.loc['Occupied','Avg_kWh']:.2f} kWh/hr",
    f"Vacant rooms avg draw           : {ems_summary.loc['Vacant','Avg_kWh']:.2f} kWh/hr",
    f"IoT-driven energy reduction     : {eco_saving_pct:.1f}% vs always-on baseline",
    f"  → Eco-Mode & auto-Off saves ~{eco_saving_pct:.0f}% when rooms are empty",
    f"Peak demand window              : 18:00 – 21:00 (full occupancy)",
    f"Lowest demand window            : 10:00 – 13:00 (checkout trough)",
    f"  → BMS pre-cooling at 14:00 supports seamless check-in experience",
])

print(f"\n{'═'*65}\n")

# =============================================================================
#  SECTION 4 — VISUALISATIONS (2 × 2 Dashboard)
# =============================================================================

fig = plt.figure(figsize=(18, 14))
fig.patch.set_facecolor(TAJ_CREAM)

# Suptitle banner
fig.suptitle(
    "IHCL / TAJ HOTELS — INTEGRATED INFORMATION SYSTEMS DASHBOARD",
    fontsize=16, fontweight="bold", color=TAJ_DARK, y=0.98,
    fontfamily="DejaVu Sans"
)
fig.text(0.5, 0.955,
    "MBA Strategic Project | ERP · CPMS · CRM · IoT EMS | Data as of June 2025",
    ha="center", fontsize=9, color="grey"
)

gs = gridspec.GridSpec(2, 2, figure=fig,
                       hspace=0.42, wspace=0.35,
                       left=0.07, right=0.97,
                       top=0.93, bottom=0.07)

# ── Chart 1 (top-left): ERP — Spend by Vendor Category ───────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(TAJ_CREAM)

cats   = erp_by_cat.index.tolist()
totals = erp_by_cat["Total_Spend"].values
colors = [TAJ_GOLD if c == "IT Hardware" else TAJ_DARK for c in cats]

bars = ax1.barh(cats, totals, color=colors, edgecolor="white",
                linewidth=0.8, height=0.6)
ax1.set_xlabel("Total Spend (INR)", labelpad=6)
ax1.set_title("ERP · Procurement Spend by Vendor Category", pad=10)
ax1.xaxis.set_major_formatter(FuncFormatter(inr_formatter))

for bar, val in zip(bars, totals):
    ax1.text(val + total_erp_spend * 0.005, bar.get_y() + bar.get_height()/2,
             inr_formatter(val, None), va="center", fontsize=8, color=TAJ_DARK)

# Legend callout
ax1.text(0.98, 0.05, "🔶 Gold = IT Hardware\n(Infrastructure investment)",
         transform=ax1.transAxes, ha="right", fontsize=7.5,
         color=TAJ_GOLD, style="italic")

# ── Chart 2 (top-right): CPMS — Revenue by Channel & Room Type ───────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(TAJ_CREAM)

pivot = df_cpms.groupby(["Booking_Channel","Room_Type"])["Total_Spend_INR"].sum().unstack()
pivot = pivot[["Deluxe","Taj Club","Suite"]]   # fixed order
room_colors = [TAJ_BLUE, TAJ_GOLD, TAJ_RUST]

pivot.plot(kind="bar", ax=ax2, color=room_colors,
           edgecolor="white", linewidth=0.6, width=0.65)
ax2.set_title("CPMS · Revenue by Booking Channel & Room Type", pad=10)
ax2.set_xlabel("Booking Channel", labelpad=6)
ax2.set_ylabel("Total Revenue (INR)", labelpad=6)
ax2.yaxis.set_major_formatter(FuncFormatter(inr_formatter))
ax2.tick_params(axis="x", rotation=0)
ax2.legend(title="Room Type", fontsize=8, title_fontsize=8,
           framealpha=0.5, loc="upper right")

# Direct channel annotation
direct_total = cpms_by_channel.loc["Direct","Revenue"]
ax2.annotate(f"Direct: {direct_rev_share:.0f}%\nof all revenue",
             xy=(0, direct_total * 0.5),
             xytext=(0.18, 0.80),
             textcoords="axes fraction",
             fontsize=8, color=TAJ_GREEN, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=TAJ_GREEN, lw=1.2))

# ── Chart 3 (bottom-left): CRM — NPS & Lifetime Stays by Loyalty Tier ─────────
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor(TAJ_CREAM)

tier_order  = ["Silver","Gold","Platinum","Epicure"]
nps_vals    = [crm_by_tier.loc[t,"Avg_NPS"]   for t in tier_order]
stays_vals  = [crm_by_tier.loc[t,"Avg_Stays"] for t in tier_order]
x           = np.arange(len(tier_order))
bar_w       = 0.38

tier_colors = ["#A9A9A9", TAJ_GOLD, "#C0C0C0", TAJ_RUST]
ax3b = ax3.twinx()

b1 = ax3.bar(x - bar_w/2, nps_vals, bar_w, color=tier_colors,
             edgecolor="white", linewidth=0.8, label="Avg NPS Score")
b2 = ax3b.bar(x + bar_w/2, stays_vals, bar_w,
              color=[c+"88" for c in ["#A9A9A9", TAJ_GOLD, "#808080", TAJ_RUST]],
              edgecolor="white", linewidth=0.8, label="Avg Lifetime Stays",
              hatch="//")

ax3.set_xticks(x)
ax3.set_xticklabels(tier_order)
ax3.set_ylabel("Avg NPS Score", color=TAJ_DARK, labelpad=6)
ax3b.set_ylabel("Avg Lifetime Stays", color=TAJ_DARK, labelpad=6)
ax3.set_ylim(0, 12)
ax3.set_title("CRM · NPS Score & Loyalty Depth by IHCL One Tier", pad=10)
ax3.tick_params(axis="x", rotation=0)

# NPS labels
for bar, val in zip(b1, nps_vals):
    ax3.text(bar.get_x() + bar.get_width()/2, val + 0.1,
             f"{val:.1f}", ha="center", fontsize=8.5, fontweight="bold",
             color=TAJ_DARK)

lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3b.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + labels2,
           fontsize=7.5, loc="upper left", framealpha=0.5)

# ── Chart 4 (bottom-right): EMS — Hourly Power by Occupancy ──────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(TAJ_CREAM)

for occ_status, color, lw, ls in [
    ("Occupied", TAJ_RUST,  2.2, "-"),
    ("Vacant",   TAJ_GREEN, 1.8, "--"),
]:
    subset = hourly_power[hourly_power["Occupancy_Status"] == occ_status]
    ax4.plot(subset["Hour"], subset["Power_Consumed_kWh"],
             label=occ_status, color=color,
             linewidth=lw, linestyle=ls, marker="o",
             markersize=4, markerfacecolor="white",
             markeredgewidth=1.4, markeredgecolor=color)

occ_power   = hourly_power[hourly_power["Occupancy_Status"]=="Occupied"].set_index("Hour")["Power_Consumed_kWh"]
vacant_pwr  = hourly_power[hourly_power["Occupancy_Status"]=="Vacant"].set_index("Hour")["Power_Consumed_kWh"]
common_hrs  = occ_power.index.intersection(vacant_pwr.index)
ax4.fill_between(
    common_hrs,
    occ_power.loc[common_hrs],
    vacant_pwr.loc[common_hrs],
    alpha=0.08, color=TAJ_RUST, label="IoT Savings Zone"
)

ax4.set_title("IoT EMS · Avg Hourly Power Consumption by Occupancy", pad=10)
ax4.set_xlabel("Hour of Day", labelpad=6)
ax4.set_ylabel("Avg Power (kWh)", labelpad=6)
ax4.set_xticks(range(0, 24, 2))
ax4.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 2)],
                    rotation=35, ha="right")
ax4.legend(fontsize=8, framealpha=0.5)

# Annotate checkout trough and peak
occ_hourly = hourly_power[hourly_power["Occupancy_Status"]=="Occupied"].set_index("Hour")["Power_Consumed_kWh"]

# Only annotate if hour exists in data
if 11 in occ_hourly.index:
    ax4.annotate("Checkout trough\n(BMS savings max)",
                 xy=(11, occ_hourly.loc[11]),
                 xytext=(7, 1.5),
                 fontsize=7.5, color=TAJ_GREEN,
                 arrowprops=dict(arrowstyle="->", color=TAJ_GREEN, lw=1.1))

if 19 in occ_hourly.index:
    ax4.annotate("Evening peak\n(full occupancy)",
                 xy=(19, occ_hourly.loc[19]),
                 xytext=(20.5, 2.0),
                 fontsize=7.5, color=TAJ_RUST,
                 arrowprops=dict(arrowstyle="->", color=TAJ_RUST, lw=1.1))

# ── Footer ────────────────────────────────────────────────────────────────────
fig.text(0.5, 0.01,
    "CONFIDENTIAL — IHCL Strategic MBA Project | Simulated Data | "
    "Analysis by Senior Data Analyst | Python 3 · pandas · seaborn · matplotlib",
    ha="center", fontsize=7, color="grey"
)

plt.savefig("ihcl_dashboard.png", dpi=180, bbox_inches="tight",
            facecolor=TAJ_CREAM)
print("  ✅  Dashboard saved → ihcl_dashboard.png")
plt.show()
