"""
Biyepati SCM Project — Modules #3, #15, #28: Vendor Ranking + Cost-to-Serve +
                        Order Fulfillment Process Optimization
Author: Fahim | Founder & CEO, Biyepati (biyepati.com)
Tool: Python (pandas, matplotlib, numpy)
Description: Generates vendor radar chart, cost-to-serve breakdown,
             order fulfillment cycle time analysis, and all Tableau CSVs.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd
import os

OUTPUT_DIR  = os.path.dirname(os.path.abspath(__file__))
TABLEAU_DIR = os.path.join(OUTPUT_DIR, "..", "tableau_data")
os.makedirs(TABLEAU_DIR, exist_ok=True)

NAVY   = "#1B4F8A"
LBLUE  = "#D6E4F7"
GREEN  = "#27AE60"
RED    = "#E74C3C"
AMBER  = "#E67E22"
GRAY   = "#95A5A6"

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE #3 — Vendor Evaluation Radar Chart
# ═══════════════════════════════════════════════════════════════════════════════
vendors = {
    "Dream Décor BD":       [8, 7, 9, 8, 7, 9],
    "Royal Frames Studio":  [9, 6, 8, 9, 8, 7],
    "Garden Palace Venue":  [7, 8, 8, 7, 6, 8],
    "Spice Route Catering": [8, 9, 7, 8, 9, 9],
}
criteria    = ["Quality\n(25%)", "Pricing\n(20%)", "Reliability\n(20%)",
               "Comm.\n(15%)", "Availability\n(12%)", "Compliance\n(8%)"]
weights     = [0.25, 0.20, 0.20, 0.15, 0.12, 0.08]
num_vars    = len(criteria)
angles      = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles     += angles[:1]
colors      = [NAVY, GREEN, AMBER, RED]

fig, axes = plt.subplots(1, 2, figsize=(16, 7), subplot_kw=dict(polar=True))
fig.patch.set_facecolor("#F8F9FA")
fig.suptitle("Biyepati — Vendor Evaluation & Ranking | Module #3\n"
             "Weighted Scoring Radar Chart | Source: Assumed performance data",
             fontsize=13, fontweight="bold", color=NAVY, y=1.01)

# Left radar: all vendors overlaid
ax = axes[0]
ax.set_facecolor("#F5F8FF")
for (vname, scores), color in zip(vendors.items(), colors):
    vals = scores + scores[:1]
    ax.plot(angles, vals, color=color, linewidth=2, linestyle="solid", label=vname)
    ax.fill(angles, vals, color=color, alpha=0.08)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(criteria, fontsize=9, fontweight="bold")
ax.set_ylim(0, 10)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(["2","4","6","8","10"], fontsize=7, color="gray")
ax.set_title("All Vendors — Performance Comparison", fontsize=11,
             fontweight="bold", color=NAVY, pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.4, 1.1), fontsize=8)
ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)

# Right: Weighted scores horizontal bar
ax2 = axes[1]
ax2.remove()
ax2 = fig.add_axes([0.55, 0.12, 0.42, 0.72])
ax2.set_facecolor("#F8F9FA")

all_vendors_ext = {
    "Dream Décor BD":       [8,7,9,8,7,9],
    "Royal Frames Studio":  [9,6,8,9,8,7],
    "Garden Palace Venue":  [7,8,8,7,6,8],
    "Spice Route Catering": [8,9,7,8,9,9],
    "Elegance Events":      [6,8,6,7,8,7],
    "Moments Photography":  [7,7,8,8,7,6],
    "Pearl Banquet Hall":   [9,5,9,8,7,8],
    "Flavors of Dhaka":     [7,9,8,7,9,8],
}
weighted_scores = {v: round(sum(s*w for s,w in zip(scores, weights)), 2)
                   for v, scores in all_vendors_ext.items()}
ws_df = pd.DataFrame(list(weighted_scores.items()), columns=["Vendor","Score"])
ws_df = ws_df.sort_values("Score", ascending=True)

bar_colors = [GREEN if s >= 7.5 else AMBER if s >= 6.5 else RED for s in ws_df["Score"]]
bars = ax2.barh(ws_df["Vendor"], ws_df["Score"], color=bar_colors,
                edgecolor="white", linewidth=0.8, height=0.55)
for bar, score in zip(bars, ws_df["Score"]):
    ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
             f"{score:.2f}", va="center", fontsize=9, fontweight="bold")
ax2.axvline(7.5, color=GREEN, linewidth=1.5, linestyle="--", label="✔ Approved (≥7.5)")
ax2.axvline(6.5, color=AMBER, linewidth=1.5, linestyle="--", label="⚠ Review (≥6.5)")
ax2.set_xlim(0, 10.5)
ax2.set_xlabel("Weighted Score (0–10)", fontsize=10, fontweight="bold")
ax2.set_title("All Vendors — Weighted Score Ranking", fontsize=11,
              fontweight="bold", color=NAVY)
ax2.legend(fontsize=8, loc="lower right")
ax2.grid(axis="x", alpha=0.3, linestyle="--")
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

plt.savefig(os.path.join(OUTPUT_DIR, "vendor_ranking.png"), dpi=180, bbox_inches="tight")
plt.close()
print("✔ vendor_ranking.png saved")

# Tableau CSV for vendor scores
df_vendors = pd.DataFrame([
    {"Vendor": v, "Category": cat, "Weighted_Score": ws,
     "Status": "Approved" if ws >= 7.5 else "Review" if ws >= 6.5 else "Rejected",
     "Quality": sc[0], "Pricing": sc[1], "Reliability": sc[2],
     "Communication": sc[3], "Availability": sc[4], "Compliance": sc[5]}
    for (v, sc), ws, cat in zip(
        all_vendors_ext.items(),
        weighted_scores.values(),
        ["Vendor/Decor","Photography","Venue","Catering",
         "Vendor/Decor","Photography","Venue","Catering"])
])
df_vendors.to_csv(os.path.join(TABLEAU_DIR, "vendor_scores.csv"), index=False)
print("✔ tableau_data/vendor_scores.csv exported")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE #15 — Cost-to-Serve Analysis
# ═══════════════════════════════════════════════════════════════════════════════
cost_cats   = ["Platform\nCommission", "Vendor\nPayout", "Payment\nFees",
               "Customer\nAcquisition", "Coordination\nLabour",
               "Platform\nMaint.", "Comm. &\nFollow-up", "Contingency\nBuffer"]
venue_costs   = [5000, 45000, 800, 1500, 2000, 500, 300, 1575]
vendor_costs  = [8000, 70000, 1200, 1500, 2500, 500, 300, 2520]
photo_costs   = [4000, 35000, 600, 1500, 1500, 500, 300, 1260]
cater_costs   = [6000, 54000, 900, 1500, 2000, 500, 300, 1896]

prices        = [55000, 90000, 45000, 70000]
total_costs   = [sum(venue_costs), sum(vendor_costs), sum(photo_costs), sum(cater_costs)]
profits       = [p - c for p, c in zip(prices, total_costs)]
margins       = [pr/p*100 for pr, p in zip(profits, prices)]
svc_labels    = ["Venue Booking", "Vendor/Decoration", "Photography", "Catering"]

fig2 = plt.figure(figsize=(18, 12))
fig2.patch.set_facecolor("#F8F9FA")
gs = GridSpec(2, 2, figure=fig2, hspace=0.45, wspace=0.35)

# Stacked bar — cost breakdown per service
ax1 = fig2.add_subplot(gs[0, :])
ax1.set_facecolor("#F8F9FA")
x = np.arange(4)
stack_data = [venue_costs, vendor_costs, photo_costs, cater_costs]
stack_arr  = np.array(stack_data).T
stack_colors = ["#1B4F8A","#2980B9","#27AE60","#E67E22",
                "#8E44AD","#16A085","#F39C12","#E74C3C"]
bottoms = np.zeros(4)
for i, (row, color, label) in enumerate(zip(stack_arr, stack_colors, cost_cats)):
    bars = ax1.bar(x, row, bottom=bottoms, color=color, label=label.replace("\n"," "),
                   edgecolor="white", linewidth=0.8)
    for j, (bar, val) in enumerate(zip(bars, row)):
        if val > 800:
            ax1.text(bar.get_x() + bar.get_width()/2,
                     bottoms[j] + val/2, f"{val:,}",
                     ha="center", va="center", fontsize=7.5,
                     color="white", fontweight="bold")
    bottoms += row

# Price line
ax1.plot(x, prices, color="#E74C3C", linewidth=2.5, marker="D",
         markersize=9, label="Price Charged (BDT)", zorder=5)
for i, (xi, pr) in enumerate(zip(x, prices)):
    ax1.annotate(f"Price:\n{pr:,}", (xi, pr), textcoords="offset points",
                 xytext=(0, 14), ha="center", fontsize=8.5,
                 color="#E74C3C", fontweight="bold")

ax1.set_xticks(x); ax1.set_xticklabels(svc_labels, fontsize=11, fontweight="bold")
ax1.set_ylabel("Cost / Price (BDT)", fontsize=11, fontweight="bold")
ax1.set_title("Biyepati — Cost-to-Serve Breakdown vs Price per Service Category\n"
              "Module #15 | Source: Assumed Dhaka market rates 2026",
              fontsize=13, fontweight="bold", color=NAVY)
ax1.legend(ncol=5, fontsize=7.5, loc="upper left", framealpha=0.9)
ax1.grid(axis="y", alpha=0.3, linestyle="--")
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

# Gross margin bar
ax2 = fig2.add_subplot(gs[1, 0])
ax2.set_facecolor("#F8F9FA")
margin_colors = [GREEN if m > 15 else AMBER for m in margins]
bars = ax2.bar(svc_labels, margins, color=margin_colors, edgecolor="white",
               linewidth=0.8, width=0.5)
for bar, m in zip(bars, margins):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
             f"{m:.1f}%", ha="center", fontsize=11, fontweight="bold",
             color=NAVY)
ax2.axhline(15, color=RED, linewidth=1.5, linestyle="--", label="Target margin (15%)")
ax2.set_ylabel("Gross Margin (%)", fontsize=10, fontweight="bold")
ax2.set_title("Gross Margin by Service", fontsize=11, fontweight="bold", color=NAVY)
ax2.legend(fontsize=9)
ax2.grid(axis="y", alpha=0.3, linestyle="--")
ax2.tick_params(axis="x", rotation=15)
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

# Profit waterfall
ax3 = fig2.add_subplot(gs[1, 1])
ax3.set_facecolor("#F8F9FA")
full_price  = 250000
full_cost   = sum([sum(venue_costs), sum(vendor_costs), sum(photo_costs), sum(cater_costs)])
full_profit = full_price - full_cost
waterfall_labels = ["Full Package\nPrice", "Vendor Payouts", "Platform Ops\nCosts",
                    "Acquisition\nCosts", "Net Profit"]
running_vals = [full_price,
                -sum(v[1] for v in [venue_costs, vendor_costs, photo_costs, cater_costs]),
                -(full_cost - sum(v[1] for v in [venue_costs, vendor_costs, photo_costs, cater_costs]) - 4*1500),
                -4*1500,
                full_profit]
running_sum = 0
bottoms_wf  = []
for v in running_vals[:-1]:
    bottoms_wf.append(running_sum if v < 0 else running_sum)
    running_sum += v
bottoms_wf.append(0)

wf_colors = [NAVY, RED, RED, RED, GREEN]
for i, (label, val, bot, color) in enumerate(zip(
        waterfall_labels, running_vals, bottoms_wf, wf_colors)):
    ax3.bar(i, abs(val), bottom=bot if val > 0 else running_sum + val + abs(val),
            color=color, alpha=0.85, edgecolor="white", linewidth=0.8, width=0.55)
    ax3.text(i, (bot if val > 0 else running_sum + val + abs(val)) + abs(val)/2,
             f"{abs(val):,}", ha="center", va="center",
             fontsize=8, fontweight="bold", color="white")

ax3.set_xticks(range(len(waterfall_labels)))
ax3.set_xticklabels(waterfall_labels, fontsize=8.5, fontweight="bold")
ax3.set_ylabel("BDT", fontsize=10, fontweight="bold")
ax3.set_title("Full Package Profit Waterfall\n(250,000 BDT event)", fontsize=11,
              fontweight="bold", color=NAVY)
ax3.grid(axis="y", alpha=0.3, linestyle="--")
ax3.spines["top"].set_visible(False); ax3.spines["right"].set_visible(False)

plt.savefig(os.path.join(OUTPUT_DIR, "cost_to_serve.png"), dpi=180, bbox_inches="tight")
plt.close()
print("✔ cost_to_serve.png saved")

# Tableau CSV for cost-to-serve
rows = []
for svc, costs in zip(svc_labels, [venue_costs, vendor_costs, photo_costs, cater_costs]):
    for cat, cost in zip([c.replace("\n"," ") for c in cost_cats], costs):
        rows.append({"Service": svc, "Cost_Category": cat, "Cost_BDT": cost})
df_cost = pd.DataFrame(rows)
df_cost.to_csv(os.path.join(TABLEAU_DIR, "cost_to_serve.csv"), index=False)
print("✔ tableau_data/cost_to_serve.csv exported")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE #28 — Order Fulfillment Cycle Time
# ═══════════════════════════════════════════════════════════════════════════════
stages = ["Customer\nDiscovery", "Service\nBrowsing", "Consultation\n& Pricing",
          "Advance\nPayment", "Pre-Event\nPrep", "Event Day\nDelivery",
          "Post-Event\nClose"]
current_days  = [3, 2, 5, 1, 21, 1, 2]
optimized_days = [1, 1, 2, 0.5, 14, 1, 1]
bottlenecks   = [False, False, True, False, True, True, False]

fig3, axes3 = plt.subplots(1, 2, figsize=(16, 6))
fig3.patch.set_facecolor("#F8F9FA")
fig3.suptitle("Biyepati — Order Fulfillment Process Optimization | Module #28\n"
              "Cycle Time Analysis: Current vs Optimized State",
              fontsize=13, fontweight="bold", color=NAVY, y=1.02)

# Grouped bar chart
ax = axes3[0]
ax.set_facecolor("#F8F9FA")
x  = np.arange(len(stages))
w  = 0.35
b1 = ax.bar(x - w/2, current_days,   w, label="Current State",   color=RED,  alpha=0.85, edgecolor="white")
b2 = ax.bar(x + w/2, optimized_days, w, label="Optimized State", color=GREEN, alpha=0.85, edgecolor="white")
for bar, val in zip(b1, current_days):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
            f"{val}d", ha="center", fontsize=8.5, fontweight="bold", color=RED)
for bar, val in zip(b2, optimized_days):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
            f"{val}d", ha="center", fontsize=8.5, fontweight="bold", color=GREEN)
for i, is_bn in enumerate(bottlenecks):
    if is_bn:
        ax.annotate("⚠", (x[i], max(current_days[i], optimized_days[i]) + 0.8),
                    ha="center", fontsize=14, color=AMBER)
ax.set_xticks(x); ax.set_xticklabels(stages, fontsize=8.5, fontweight="bold")
ax.set_ylabel("Cycle Time (Days)", fontsize=10, fontweight="bold")
ax.set_title("Cycle Time per Fulfillment Stage", fontsize=11, fontweight="bold", color=NAVY)
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# Cumulative time chart
ax2 = axes3[1]
ax2.set_facecolor("#F8F9FA")
cum_current   = np.cumsum(current_days)
cum_optimized = np.cumsum(optimized_days)
x_pts = range(len(stages))
ax2.fill_between(x_pts, cum_current, cum_optimized, alpha=0.2, color=GREEN,
                 label=f"Time saved: {sum(current_days)-sum(optimized_days):.1f} days")
ax2.plot(x_pts, cum_current,   color=RED,  linewidth=2.5, marker="o", markersize=7,
         label=f"Current ({sum(current_days)} days total)")
ax2.plot(x_pts, cum_optimized, color=GREEN, linewidth=2.5, marker="s", markersize=7,
         label=f"Optimized ({sum(optimized_days)} days total)")
for xi, (yc, yo) in enumerate(zip(cum_current, cum_optimized)):
    ax2.annotate(f"{yc}d", (xi, yc), textcoords="offset points",
                 xytext=(0, 8), fontsize=7.5, color=RED, ha="center")
    ax2.annotate(f"{yo}d", (xi, yo), textcoords="offset points",
                 xytext=(0, -15), fontsize=7.5, color=GREEN, ha="center")
ax2.set_xticks(x_pts); ax2.set_xticklabels(stages, fontsize=8.5, fontweight="bold")
ax2.set_ylabel("Cumulative Days", fontsize=10, fontweight="bold")
ax2.set_title("Cumulative Fulfillment Timeline", fontsize=11, fontweight="bold", color=NAVY)
ax2.legend(fontsize=8.5, loc="upper left")
ax2.grid(alpha=0.3, linestyle="--")
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "fulfillment_cycle_time.png"), dpi=180, bbox_inches="tight")
plt.close()
print("✔ fulfillment_cycle_time.png saved")

# Final Tableau CSVs
df_fulfill = pd.DataFrame({
    "Stage": stages, "Current_Days": current_days,
    "Optimized_Days": optimized_days,
    "Days_Saved": [c - o for c, o in zip(current_days, optimized_days)],
    "Bottleneck": bottlenecks
})
df_fulfill["Stage"] = df_fulfill["Stage"].str.replace("\n"," ")
df_fulfill.to_csv(os.path.join(TABLEAU_DIR, "fulfillment_cycle.csv"), index=False)

df_risk = pd.DataFrame([
    {"ID":"R-01","Category":"Vendor Reliability","P":4,"I":5,"Score":20,"Level":"Critical"},
    {"ID":"R-02","Category":"Demand Volatility","P":3,"I":4,"Score":12,"Level":"High"},
    {"ID":"R-03","Category":"Payment Default","P":2,"I":5,"Score":10,"Level":"High"},
    {"ID":"R-04","Category":"Platform Downtime","P":2,"I":4,"Score":8,"Level":"Medium"},
    {"ID":"R-05","Category":"Pricing Dispute","P":3,"I":3,"Score":9,"Level":"High"},
    {"ID":"R-06","Category":"Transport Delay","P":3,"I":5,"Score":15,"Level":"Critical"},
    {"ID":"R-07","Category":"Competitor Entry","P":2,"I":3,"Score":6,"Level":"Medium"},
    {"ID":"R-08","Category":"Quality Drop","P":2,"I":4,"Score":8,"Level":"Medium"},
    {"ID":"R-09","Category":"Regulatory Change","P":1,"I":5,"Score":5,"Level":"Medium"},
    {"ID":"R-10","Category":"Cost Fluctuation","P":1,"I":3,"Score":3,"Level":"Low"},
    {"ID":"R-11","Category":"Data Breach","P":1,"I":5,"Score":5,"Level":"Medium"},
    {"ID":"R-12","Category":"Reputation Risk","P":2,"I":4,"Score":8,"Level":"Medium"},
])
df_risk.to_csv(os.path.join(TABLEAU_DIR, "risk_data.csv"), index=False)

df_kpi = pd.DataFrame([
    {"KPI":"Vendor Onboard Rate","Target":15,"Current":5,"Unit":"partners"},
    {"KPI":"Booking Confirmation Time","Target":24,"Current":48,"Unit":"hours"},
    {"KPI":"On-Time Vendor Arrival","Target":95,"Current":80,"Unit":"%"},
    {"KPI":"Customer Satisfaction","Target":4.5,"Current":4.6,"Unit":"/5"},
    {"KPI":"Advance Payment Rate","Target":100,"Current":100,"Unit":"%"},
    {"KPI":"Dispute Rate","Target":5,"Current":2,"Unit":"%"},
    {"KPI":"Gross Margin (Full Pkg)","Target":15,"Current":1.8,"Unit":"%"},
    {"KPI":"Annual Bookings Forecast","Target":100,"Current":10,"Unit":"events"},
])
df_kpi.to_csv(os.path.join(TABLEAU_DIR, "kpi_dashboard.csv"), index=False)
print("✔ All Tableau CSVs exported")

print("\n✅ Modules #3, #15, #28 complete.")
