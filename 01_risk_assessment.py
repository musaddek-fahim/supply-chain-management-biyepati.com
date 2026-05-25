"""
Biyepati SCM Project — Module #7: Supply Chain Risk Assessment
Author: Fahim | Founder & CEO, Biyepati (biyepati.com)
Tool: Python (matplotlib, numpy, pandas)
Description: Generates probability-impact heat map, risk distribution chart,
             and risk register summary for Biyepati's wedding supply chain.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Risk Data ──────────────────────────────────────────────────────────────────
risks = pd.DataFrame([
    {"ID":"R-01","Category":"Vendor Reliability",  "Description":"Vendor no-show on event day",                    "P":4,"I":5},
    {"ID":"R-02","Category":"Demand Volatility",   "Description":"Demand spike exceeding vendor capacity",          "P":3,"I":4},
    {"ID":"R-03","Category":"Payment Default",     "Description":"Customer fails to pay 80% balance on event day",  "P":2,"I":5},
    {"ID":"R-04","Category":"Platform Downtime",   "Description":"WordPress platform failure during peak booking",  "P":2,"I":4},
    {"ID":"R-05","Category":"Pricing Dispute",     "Description":"Customer disputes variable pricing post-booking", "P":3,"I":3},
    {"ID":"R-06","Category":"Transport Delay",     "Description":"Vendor late arrival on event day",                "P":3,"I":5},
    {"ID":"R-07","Category":"Competitor Entry",    "Description":"New platform enters Dhaka wedding market",        "P":2,"I":3},
    {"ID":"R-08","Category":"Quality Drop",        "Description":"Partner reduces service quality post-onboarding", "P":2,"I":4},
    {"ID":"R-09","Category":"Regulatory Change",   "Description":"Government restriction on event gatherings",      "P":1,"I":5},
    {"ID":"R-10","Category":"Cost Fluctuation",    "Description":"Import price rise for decoration materials",      "P":1,"I":3},
    {"ID":"R-11","Category":"Data Breach",         "Description":"Customer data compromised on platform",           "P":1,"I":5},
    {"ID":"R-12","Category":"Reputation Risk",     "Description":"Viral negative review damages platform brand",    "P":2,"I":4},
])
risks["Score"] = risks["P"] * risks["I"]

def risk_level(score):
    if score >= 15: return "Critical", "#E74C3C"
    elif score >= 9: return "High",   "#E67E22"
    elif score >= 4: return "Medium", "#F1C40F"
    else:            return "Low",    "#27AE60"

risks[["Level","Color"]] = risks["Score"].apply(
    lambda s: pd.Series(risk_level(s)))

# ── FIGURE 1: Probability–Impact Heat Map ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor("#F8F9FA")
ax.set_facecolor("#F8F9FA")

cmap = LinearSegmentedColormap.from_list(
    "risk", ["#27AE60","#F1C40F","#E67E22","#E74C3C"], N=25)

for p in range(1, 6):
    for i in range(1, 6):
        score = p * i
        normed = (score - 1) / 24
        color = cmap(normed)
        ax.add_patch(mpatches.FancyBboxPatch(
            (i-0.48, p-0.48), 0.96, 0.96,
            boxstyle="round,pad=0.05", color=color, alpha=0.85, zorder=1))
        ax.text(i, p, str(score), ha="center", va="center",
                fontsize=13, fontweight="bold", color="white", zorder=2)

# Plot risks as scatter
jitter = np.random.default_rng(42)
for _, row in risks.iterrows():
    jx = row["I"] + jitter.uniform(-0.18, 0.18)
    jy = row["P"] + jitter.uniform(-0.18, 0.18)
    ax.scatter(jx, jy, s=220, color=row["Color"], edgecolors="white",
               linewidths=1.5, zorder=4)
    ax.annotate(row["ID"], (jx, jy), textcoords="offset points",
                xytext=(8, 4), fontsize=7.5, fontweight="bold",
                color="#2C3E50", zorder=5)

ax.set_xlim(0.4, 5.6)
ax.set_ylim(0.4, 5.6)
ax.set_xticks(range(1, 6))
ax.set_yticks(range(1, 6))
ax.set_xticklabels([f"Impact {i}" for i in range(1, 6)], fontsize=10)
ax.set_yticklabels([f"Prob {p}" for p in range(1, 6)], fontsize=10)
ax.set_xlabel("Impact Severity →", fontsize=12, fontweight="bold", labelpad=10)
ax.set_ylabel("Probability →", fontsize=12, fontweight="bold", labelpad=10)
ax.set_title("Biyepati — Supply Chain Risk Assessment\nProbability–Impact Heat Map",
             fontsize=14, fontweight="bold", color="#1B4F8A", pad=15)
ax.grid(False)

legend_patches = [
    mpatches.Patch(color="#E74C3C", label="Critical (≥15)"),
    mpatches.Patch(color="#E67E22", label="High (9–14)"),
    mpatches.Patch(color="#F1C40F", label="Medium (4–8)"),
    mpatches.Patch(color="#27AE60", label="Low (<4)"),
]
ax.legend(handles=legend_patches, loc="lower right", fontsize=9,
          framealpha=0.9, title="Risk Level")
ax.annotate("Source: Assumed risk data | Biyepati Dhaka operations 2026",
            xy=(0.01, 0.01), xycoords="axes fraction", fontsize=7.5,
            color="gray", style="italic")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "risk_heatmap.png"), dpi=180, bbox_inches="tight")
plt.close()
print("✔ risk_heatmap.png saved")

# ── FIGURE 2: Risk Distribution Bar Chart ─────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#F8F9FA")

# Left: Risk scores by ID
ax1 = axes[0]
ax1.set_facecolor("#F8F9FA")
colors = risks["Color"].tolist()
bars = ax1.barh(risks["ID"][::-1], risks["Score"][::-1],
                color=colors[::-1], edgecolor="white", linewidth=0.8, height=0.6)
for bar, score in zip(bars, risks["Score"][::-1]):
    ax1.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
             f"{score}", va="center", fontsize=10, fontweight="bold")
ax1.axvline(15, color="#E74C3C", linewidth=1.5, linestyle="--", label="Critical threshold (15)")
ax1.axvline(9,  color="#E67E22", linewidth=1.5, linestyle="--", label="High threshold (9)")
ax1.axvline(4,  color="#F1C40F", linewidth=1.5, linestyle="--", label="Medium threshold (4)")
ax1.set_xlabel("Risk Score (P × I)", fontsize=11, fontweight="bold")
ax1.set_title("Risk Scores by Risk ID", fontsize=12, fontweight="bold", color="#1B4F8A")
ax1.legend(fontsize=8, loc="lower right")
ax1.set_xlim(0, 26)
ax1.grid(axis="x", alpha=0.3)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Right: Risk level distribution pie
ax2 = axes[1]
ax2.set_facecolor("#F8F9FA")
level_counts = risks["Level"].value_counts()
order = ["Critical","High","Medium","Low"]
level_counts = level_counts.reindex([l for l in order if l in level_counts.index])
pie_colors = {"Critical":"#E74C3C","High":"#E67E22","Medium":"#F1C40F","Low":"#27AE60"}
wedge_colors = [pie_colors[l] for l in level_counts.index]
wedges, texts, autotexts = ax2.pie(
    level_counts.values, labels=level_counts.index,
    colors=wedge_colors, autopct="%1.0f%%",
    startangle=140, pctdistance=0.7,
    wedgeprops=dict(edgecolor="white", linewidth=2))
for t in texts:     t.set_fontsize(11); t.set_fontweight("bold")
for t in autotexts: t.set_fontsize(10); t.set_color("white"); t.set_fontweight("bold")
ax2.set_title("Risk Level Distribution\n(12 Risks Identified)", fontsize=12,
              fontweight="bold", color="#1B4F8A")

fig.suptitle("Biyepati Supply Chain Risk Assessment — Module #7",
             fontsize=14, fontweight="bold", color="#1B4F8A", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "risk_distribution.png"), dpi=180, bbox_inches="tight")
plt.close()
print("✔ risk_distribution.png saved")

# ── FIGURE 3: Risk Register Table ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(16, 7))
fig.patch.set_facecolor("#F8F9FA")
ax.set_facecolor("#F8F9FA")
ax.axis("off")

table_data = risks[["ID","Category","P","I","Score","Level"]].values.tolist()
col_labels = ["Risk ID","Category","Prob (1–5)","Impact (1–5)","Score","Level"]
table = ax.table(cellText=table_data, colLabels=col_labels,
                 loc="center", cellLoc="center")
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.7)

# Style header
for j in range(len(col_labels)):
    table[0, j].set_facecolor("#1B4F8A")
    table[0, j].set_text_props(color="white", fontweight="bold", fontsize=10)

# Style data rows
for i, (_, row) in enumerate(risks.iterrows(), 1):
    bg = "#FFFFFF" if i % 2 == 0 else "#F0F4FA"
    for j in range(len(col_labels)):
        table[i, j].set_facecolor(bg)
    # Color the Level cell
    table[i, 5].set_facecolor(row["Color"])
    table[i, 5].set_text_props(color="white", fontweight="bold")

ax.set_title("Biyepati — Risk Register Summary | Module #7\nSource: Assumed operational risks | Dhaka wedding market 2026",
             fontsize=12, fontweight="bold", color="#1B4F8A", pad=12)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "risk_register_table.png"), dpi=180, bbox_inches="tight")
plt.close()
print("✔ risk_register_table.png saved")

print("\n✅ All risk assessment charts generated successfully.")
print(f"   Output: {OUTPUT_DIR}")
