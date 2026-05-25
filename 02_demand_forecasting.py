"""
Biyepati SCM Project — Module #5: Demand Forecasting Dashboard
Author: Fahim | Founder & CEO, Biyepati (biyepati.com)
Tool: Python (pandas, matplotlib, numpy)
Description: Seasonal demand forecasting for Dhaka wedding market.
             Generates trend analysis, seasonal decomposition, and
             12-month 2026 forecast with confidence bands.
Data Source: Assumed from Bangladesh wedding industry benchmarks 2025.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Data ───────────────────────────────────────────────────────────────────────
months     = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
actual_25  = [85, 110, 70, 95, 120, 45, 30, 35, 50, 75, 140, 155]
actual_24  = [75,  97, 60, 84, 105, 38, 25, 30, 44, 66, 124, 137]
growth_rate = 0.12
forecast_26 = [int(v * (1 + growth_rate)) for v in actual_25]
upper_26    = [int(v * 1.15) for v in forecast_26]
lower_26    = [int(v * 0.85) for v in forecast_26]
seasonal_idx = [v / np.mean(actual_25) for v in actual_25]

# ── FIGURE 1: Full Forecasting Dashboard ──────────────────────────────────────
fig = plt.figure(figsize=(18, 13))
fig.patch.set_facecolor("#F8F9FA")
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.32)

NAVY = "#1B4F8A"
x = np.arange(len(months))

# ── Panel A: Actual vs Forecast with confidence band ──────────────────────────
ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor("#F8F9FA")
ax1.fill_between(x, lower_26, upper_26, alpha=0.2, color="#3498DB", label="Forecast band (±15%)")
ax1.plot(x, actual_24,  color="#95A5A6", linewidth=2, linestyle="--", marker="o", markersize=5, label="2024 Actual")
ax1.plot(x, actual_25,  color=NAVY,      linewidth=2.5, marker="o",  markersize=7, label="2025 Actual")
ax1.plot(x, forecast_26,color="#E74C3C", linewidth=2.5, marker="s",  markersize=7, label="2026 Forecast (+12% growth)")
for i, (y25, y26) in enumerate(zip(actual_25, forecast_26)):
    ax1.annotate(str(y25), (x[i], y25), textcoords="offset points", xytext=(0, 8),
                 fontsize=7.5, color=NAVY, ha="center")
    ax1.annotate(str(y26), (x[i], y26), textcoords="offset points", xytext=(0, -14),
                 fontsize=7.5, color="#E74C3C", ha="center")
ax1.set_xticks(x); ax1.set_xticklabels(months, fontsize=10)
ax1.set_ylabel("Wedding Bookings", fontsize=11, fontweight="bold")
ax1.set_title("Wedding Demand Forecast — Dhaka Metro Market (2024–2026)\nBiyepati SCM Module #5 | Source: Assumed industry data",
              fontsize=13, fontweight="bold", color=NAVY)
ax1.legend(fontsize=9, loc="upper left", framealpha=0.9)
ax1.grid(axis="y", alpha=0.3, linestyle="--")
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

# ── Panel B: Seasonal Index Bar Chart ─────────────────────────────────────────
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_facecolor("#F8F9FA")
bar_colors = ["#E74C3C" if si >= 1.2 else "#F39C12" if si >= 0.8 else "#3498DB"
              for si in seasonal_idx]
bars = ax2.bar(months, seasonal_idx, color=bar_colors, edgecolor="white", linewidth=0.8)
ax2.axhline(1.0, color=NAVY, linewidth=1.5, linestyle="--", label="Baseline = 1.0")
ax2.axhline(1.2, color="#E74C3C", linewidth=1, linestyle=":", alpha=0.7, label="Peak threshold")
ax2.axhline(0.8, color="#3498DB", linewidth=1, linestyle=":", alpha=0.7, label="Low threshold")
for bar, si in zip(bars, seasonal_idx):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
             f"{si:.2f}", ha="center", fontsize=8, fontweight="bold")
ax2.set_title("Seasonal Demand Index by Month", fontsize=11, fontweight="bold", color=NAVY)
ax2.set_ylabel("Seasonal Index", fontsize=10)
ax2.legend(fontsize=8, loc="upper left")
ax2.set_ylim(0, 2.0)
ax2.tick_params(axis="x", rotation=45)
ax2.grid(axis="y", alpha=0.3, linestyle="--")
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

# ── Panel C: Service Category Demand Split ────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 1])
ax3.set_facecolor("#F8F9FA")
categories    = ["Venue\nBooking", "Vendor/\nDecoration", "Photography", "Catering"]
demand_share  = [0.30, 0.35, 0.20, 0.15]
annual_total  = sum(forecast_26)
cat_demand    = [annual_total * s for s in demand_share]
cat_colors    = ["#1B4F8A","#2980B9","#27AE60","#E67E22"]
wedges, texts, autotexts = ax3.pie(
    cat_demand, labels=categories, colors=cat_colors,
    autopct="%1.0f%%", startangle=140,
    wedgeprops=dict(edgecolor="white", linewidth=2),
    pctdistance=0.7)
for t in texts:     t.set_fontsize(9);  t.set_fontweight("bold")
for t in autotexts: t.set_fontsize(9);  t.set_color("white"); t.set_fontweight("bold")
ax3.set_title(f"2026 Demand Split by Service\n(Total Forecast: {annual_total:,} events)",
              fontsize=11, fontweight="bold", color=NAVY)

plt.savefig(os.path.join(OUTPUT_DIR, "demand_forecast_dashboard.png"), dpi=180, bbox_inches="tight")
plt.close()
print("✔ demand_forecast_dashboard.png saved")

# ── FIGURE 2: Monthly Capacity Planning ───────────────────────────────────────
fig2, ax = plt.subplots(figsize=(14, 6))
fig2.patch.set_facecolor("#F8F9FA")
ax.set_facecolor("#F8F9FA")

vendors_available = [3, 3, 3, 3, 3, 2, 2, 2, 3, 3, 5, 5]
capacity_max      = [v * 4 for v in vendors_available]   # 4 events per vendor/month

width = 0.35
bars1 = ax.bar(x - width/2, forecast_26, width, label="2026 Forecasted Demand",
               color="#1B4F8A", alpha=0.85, edgecolor="white")
bars2 = ax.bar(x + width/2, capacity_max, width, label="Vendor Capacity (available)",
               color="#27AE60", alpha=0.85, edgecolor="white")

for bar in bars1:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 1, str(int(h)),
            ha="center", va="bottom", fontsize=8, color="#1B4F8A", fontweight="bold")
for bar in bars2:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 1, str(int(h)),
            ha="center", va="bottom", fontsize=8, color="#27AE60", fontweight="bold")

# Highlight capacity gaps
for i, (d, c) in enumerate(zip(forecast_26, capacity_max)):
    if d > c:
        ax.annotate("⚠ Gap", (x[i], max(d,c) + 8), ha="center",
                    fontsize=8, color="#E74C3C", fontweight="bold")

ax.set_xticks(x); ax.set_xticklabels(months, fontsize=10)
ax.set_ylabel("Number of Events / Capacity", fontsize=11, fontweight="bold")
ax.set_title("Biyepati — Demand vs Vendor Capacity Planning 2026\nModule #5 | Source: Assumed | Dhaka market",
             fontsize=13, fontweight="bold", color=NAVY)
ax.legend(fontsize=10)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "demand_vs_capacity.png"), dpi=180, bbox_inches="tight")
plt.close()
print("✔ demand_vs_capacity.png saved")

# ── Export CSVs for Tableau ────────────────────────────────────────────────────
tableau_dir = os.path.join(OUTPUT_DIR, "..", "tableau_data")
os.makedirs(tableau_dir, exist_ok=True)

df_demand = pd.DataFrame({
    "Month": months,
    "Month_Num": range(1, 13),
    "Actual_2024": actual_24,
    "Actual_2025": actual_25,
    "Forecast_2026": forecast_26,
    "Upper_Bound_2026": upper_26,
    "Lower_Bound_2026": lower_26,
    "Seasonal_Index": [round(s, 3) for s in seasonal_idx],
    "Vendor_Capacity": capacity_max,
    "Peak_Flag": ["Peak" if v >= 100 else "Off-Peak" for v in actual_25],
    "Growth_Rate_Pct": [growth_rate * 100] * 12
})
df_demand.to_csv(os.path.join(tableau_dir, "demand_forecast.csv"), index=False)
print("✔ tableau_data/demand_forecast.csv exported")

print("\n✅ Demand forecasting module complete.")
