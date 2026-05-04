import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings

warnings.filterwarnings("ignore")
sns.set_theme(style="darkgrid", palette="deep")
plt.rcParams.update({"figure.dpi": 130, "font.size": 10})

FILE = r"C:\Users\asif6\Downloads\AQI_Air_Quality_Dataset.csv"   # change path if needed


# ─────────────────────────────────────────────────────────────
# 1 ─ Load & Inspect Data
# ─────────────────────────────────────────────────────────────
df = pd.read_csv(FILE)
df.columns = df.columns.str.strip().str.replace(" ", "_")
df.rename(columns={"PM2.5": "PM25", "Wind_Speed": "Wind_Speed"}, inplace=True)
df["Date"] = pd.to_datetime(df["Date"])

print("=" * 60)
print("1.  DATASET OVERVIEW")
print("=" * 60)
print(f"Shape             : {df.shape}")
print(f"Date Range        : {df['Date'].min().date()}  →  {df['Date'].max().date()}")
print(f"Cities            : {sorted(df['City'].unique())}")
print(f"Countries         : {df['Country'].unique()}")
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())


# ─────────────────────────────────────────────────────────────
# 2 ─ AQI Category (US-EPA PM2.5 Breakpoints)
# ─────────────────────────────────────────────────────────────
def aqi_category(pm25):
    if   pm25 < 12.0:  return "Good"
    elif pm25 < 35.4:  return "Moderate"
    elif pm25 < 55.4:  return "Unhealthy (Sensitive)"
    elif pm25 < 150.4: return "Unhealthy"
    elif pm25 < 250.4: return "Very Unhealthy"
    else:              return "Hazardous"

df["AQI_Category"] = df["PM25"].apply(aqi_category)
df["Month"]        = df["Date"].dt.strftime("%b")
df["Month_Num"]    = df["Date"].dt.month

print("\n\n" + "=" * 60)
print("2.  AQI CATEGORY DISTRIBUTION")
print("=" * 60)
cat_counts = df["AQI_Category"].value_counts()
print(cat_counts)
print(f"\nPercentages:\n{(cat_counts / len(df) * 100).round(1)}")


# ─────────────────────────────────────────────────────────────
# 3 ─ Descriptive Statistics
# ─────────────────────────────────────────────────────────────
pollutants  = ["PM25", "PM10", "NO2", "SO2", "CO", "O3"]
weather     = ["Temperature", "Humidity", "Wind_Speed"]
all_numeric = pollutants + weather

print("\n\n" + "=" * 60)
print("3.  DESCRIPTIVE STATISTICS — ALL NUMERIC COLUMNS")
print("=" * 60)
print(df[all_numeric].describe().round(2).to_string())


# ─────────────────────────────────────────────────────────────
# 4 ─ Per-City Averages
# ─────────────────────────────────────────────────────────────
city_avg = df.groupby("City")[all_numeric].mean().round(2)
print("\n\n" + "=" * 60)
print("4.  CITY-WISE AVERAGE POLLUTANT LEVELS")
print("=" * 60)
print(city_avg.to_string())


# ─────────────────────────────────────────────────────────────
# 5 ─ Monthly Trends
# ─────────────────────────────────────────────────────────────
month_order = ["Jan", "Feb", "Mar", "Apr", "May"]
monthly_avg = (df.groupby(["Month", "Month_Num"])[pollutants]
               .mean()
               .reset_index()
               .sort_values("Month_Num"))

print("\n\n" + "=" * 60)
print("5.  MONTHLY AVERAGE POLLUTANT LEVELS")
print("=" * 60)
print(monthly_avg.drop("Month_Num", axis=1).to_string(index=False))


# ─────────────────────────────────────────────────────────────
# 6 ─ Correlation Analysis
# ─────────────────────────────────────────────────────────────
print("\n\n" + "=" * 60)
print("6.  PEARSON CORRELATION MATRIX")
print("=" * 60)
corr_matrix = df[all_numeric].corr().round(3)
print(corr_matrix.to_string())


# ─────────────────────────────────────────────────────────────
# 7 ─ Anomaly / Extreme Pollution Days
# ─────────────────────────────────────────────────────────────
q99 = df["PM25"].quantile(0.99)
extreme = df[df["PM25"] >= q99][["City", "Date", "PM25", "PM10", "AQI_Category"]]

print("\n\n" + "=" * 60)
print("7.  EXTREME PM2.5 DAYS (≥ 99th percentile)")
print("=" * 60)
print(extreme.sort_values("PM25", ascending=False).to_string(index=False))


# ─────────────────────────────────────────────────────────────
# 8 ─ Wind Speed vs PM2.5 Pearson Test
# ─────────────────────────────────────────────────────────────
r, p = stats.pearsonr(df["Wind_Speed"], df["PM25"])
print("\n\n" + "=" * 60)
print("8.  WIND SPEED vs PM2.5 — PEARSON CORRELATION TEST")
print("=" * 60)
print(f"r = {r:.4f}   p-value = {p:.4f}")
if p < 0.05:
    direction = "negative" if r < 0 else "positive"
    print(f"→ Statistically significant {direction} correlation (α = 0.05)")
else:
    print("→ Not statistically significant at α = 0.05")


# ─────────────────────────────────────────────────────────────
# 9 ─ Composite Pollution Index (CPI)
# ─────────────────────────────────────────────────────────────
maxvals = {"PM25": 179.95, "PM10": 219.63, "NO2": 70, "SO2": 60, "CO": 2.0, "O3": 100}
for col, mx in maxvals.items():
    df[f"norm_{col}"] = df[col] / mx

df["CPI"] = df[[f"norm_{c}" for c in maxvals]].mean(axis=1).round(4)
cpi_city  = df.groupby("City")["CPI"].mean().sort_values(ascending=False).round(4)

print("\n\n" + "=" * 60)
print("9.  COMPOSITE POLLUTION INDEX (CPI) BY CITY")
print("=" * 60)
print(cpi_city.to_string())
print("(Higher = more polluted, scale 0–1)")


# ─────────────────────────────────────────────────────────────
# 10 ─ VISUALISATIONS
# ─────────────────────────────────────────────────────────────
CITY_COLORS = {
    "Bangalore": "#e74c3c", "Chennai": "#e67e22", "Delhi": "#9b59b6",
    "Hyderabad": "#2980b9",  "Kolkata": "#27ae60", "Mumbai": "#f39c12",
    "Pune":      "#1abc9c"
}
cat_palette = {
    "Good": "#2ecc71", "Moderate": "#f1c40f",
    "Unhealthy (Sensitive)": "#e67e22",
    "Unhealthy": "#e74c3c", "Very Unhealthy": "#8e44ad", "Hazardous": "#2c3e50"
}


# ── 10.1  Bar Chart: Avg PM2.5 by City ───────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
data_sorted = city_avg["PM25"].sort_values(ascending=False)
bars = ax.bar(data_sorted.index, data_sorted.values,
              color=[CITY_COLORS[c] for c in data_sorted.index], edgecolor="white", linewidth=0.8)
ax.axhline(data_sorted.mean(), color="black", linestyle="--", linewidth=1.2, label=f"Mean: {data_sorted.mean():.1f}")
for bar, val in zip(bars, data_sorted.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5, f"{val:.1f}",
            ha="center", va="bottom", fontsize=9, fontweight="bold")
ax.set(title="Average PM2.5 Concentration by City (Jan–May 2024)",
       xlabel="City", ylabel="PM2.5 (µg/m³)")
ax.legend()
plt.tight_layout()
plt.savefig("plot_01_avg_pm25_by_city.png")
plt.show()


# ── 10.2  Grouped Bar: All Pollutants by City ─────────────────
fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(len(city_avg.index))
width = 0.13
for i, pol in enumerate(pollutants[:5]):   # exclude O3 for scale
    ax.bar(x + i*width, city_avg[pol], width, label=pol)
ax.set_xticks(x + width * 2)
ax.set_xticklabels(city_avg.index, rotation=30)
ax.set(title="Pollutant Comparison Across Cities",
       xlabel="City", ylabel="Concentration")
ax.legend()
plt.tight_layout()
plt.savefig("plot_02_pollutant_grouped_bar.png")
plt.show()


# ── 10.3  Line Chart: Monthly PM2.5 Trend ─────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
for city, grp in df.groupby("City"):
    monthly = grp.groupby(["Month_Num", "Month"])["PM25"].mean().reset_index().sort_values("Month_Num")
    ax.plot(monthly["Month"], monthly["PM25"], marker="o", label=city,
            color=CITY_COLORS[city], linewidth=2)
ax.set(title="Monthly PM2.5 Trend by City (2024)",
       xlabel="Month", ylabel="Avg PM2.5 (µg/m³)")
ax.legend(loc="upper right", fontsize=8)
plt.tight_layout()
plt.savefig("plot_03_monthly_trend.png")
plt.show()


# ── 10.4  Heatmap: Pollutant Correlation ─────────────────────
fig, ax = plt.subplots(figsize=(9, 7))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, vmin=-1, vmax=1, ax=ax, linewidths=0.5)
ax.set_title("Pearson Correlation Heatmap — All Variables")
plt.tight_layout()
plt.savefig("plot_04_correlation_heatmap.png")
plt.show()


# ── 10.5  Pie Chart: AQI Category Distribution ────────────────
fig, ax = plt.subplots(figsize=(7, 7))
labels = cat_counts.index
sizes  = cat_counts.values
colors = [cat_palette.get(l, "#95a5a6") for l in labels]
wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                   autopct="%1.1f%%", startangle=140,
                                   wedgeprops={"edgecolor": "white", "linewidth": 1.5})
for at in autotexts:
    at.set_fontsize(9)
ax.set_title("AQI Category Distribution (PM2.5 — US EPA)", fontsize=13, pad=20)
plt.tight_layout()
plt.savefig("plot_05_aqi_pie.png")
plt.show()


# ── 10.6  Box Plot: PM2.5 by City ─────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
city_order = df.groupby("City")["PM25"].median().sort_values(ascending=False).index
sns.boxplot(data=df, x="City", y="PM25", order=city_order,
            palette=CITY_COLORS, ax=ax, linewidth=1.2)
ax.axhline(df["PM25"].mean(), color="red", linestyle="--", linewidth=1, label="Overall Mean")
ax.set(title="PM2.5 Distribution by City (Box Plot)", xlabel="City", ylabel="PM2.5 (µg/m³)")
ax.legend()
plt.tight_layout()
plt.savefig("plot_06_boxplot_pm25.png")
plt.show()


# ── 10.7  Scatter: Wind Speed vs PM2.5 ────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
for city, grp in df.groupby("City"):
    ax.scatter(grp["Wind_Speed"], grp["PM25"], alpha=0.65, label=city,
               color=CITY_COLORS[city], edgecolors="white", linewidth=0.4, s=60)
m, b = np.polyfit(df["Wind_Speed"], df["PM25"], 1)
x_line = np.linspace(df["Wind_Speed"].min(), df["Wind_Speed"].max(), 100)
ax.plot(x_line, m*x_line + b, color="black", linestyle="--", linewidth=2, label=f"Trend (r={r:.2f})")
ax.set(title="Wind Speed vs PM2.5 (Dispersion Effect)",
       xlabel="Wind Speed (m/s)", ylabel="PM2.5 (µg/m³)")
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig("plot_07_windspeed_pm25.png")
plt.show()


# ── 10.8  Stacked Bar: AQI Category Count Per City ────────────
cat_city = df.groupby(["City", "AQI_Category"]).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(11, 6))
cat_order = ["Good", "Moderate", "Unhealthy (Sensitive)", "Unhealthy", "Very Unhealthy", "Hazardous"]
cat_order = [c for c in cat_order if c in cat_city.columns]
cat_city[cat_order].plot(kind="bar", stacked=True, ax=ax,
                          color=[cat_palette[c] for c in cat_order], edgecolor="white", linewidth=0.5)
ax.set(title="AQI Category Frequency Per City", xlabel="City", ylabel="Number of Days")
ax.legend(title="AQI Category", fontsize=8, loc="upper right")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
plt.tight_layout()
plt.savefig("plot_08_stacked_aqi_city.png")
plt.show()


# ── 10.9  Histogram: PM2.5 Distribution ──────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df["PM25"], bins=25, color="#3498db", edgecolor="white", linewidth=0.6, alpha=0.85)
ax.axvline(df["PM25"].mean(),   color="red",    linestyle="--", linewidth=1.5, label=f"Mean {df['PM25'].mean():.1f}")
ax.axvline(df["PM25"].median(), color="orange", linestyle="-",  linewidth=1.5, label=f"Median {df['PM25'].median():.1f}")
ax.set(title="PM2.5 Frequency Distribution", xlabel="PM2.5 (µg/m³)", ylabel="Count")
ax.legend()
plt.tight_layout()
plt.savefig("plot_09_pm25_histogram.png")
plt.show()


# ── 10.10  Pair Plot: PM25, NO2, O3, Temp ─────────────────────
pair_cols = ["PM25", "PM10", "NO2", "O3", "Temperature"]
g = sns.pairplot(df[pair_cols + ["City"]], hue="City", palette=CITY_COLORS,
                 plot_kws={"alpha": 0.5, "s": 25}, diag_kind="kde")
g.figure.suptitle("Pair Plot — Key Pollutants & Temperature", y=1.01, fontsize=13)
plt.tight_layout()
plt.savefig("plot_10_pairplot.png")
plt.show()


# ─────────────────────────────────────────────────────────────
# 11 ─ Summary Report Print
# ─────────────────────────────────────────────────────────────
print("\n\n" + "=" * 60)
print("10.  SUMMARY REPORT")
print("=" * 60)
print(f"  • Total records analysed   : {len(df)}")
print(f"  • Cities covered           : {', '.join(sorted(df['City'].unique()))}")
print(f"  • Most polluted city (PM2.5): {city_avg['PM25'].idxmax()} ({city_avg['PM25'].max():.2f} µg/m³)")
print(f"  • Cleanest city   (PM2.5)  : {city_avg['PM25'].idxmin()} ({city_avg['PM25'].min():.2f} µg/m³)")
print(f"  • Overall avg PM2.5        : {df['PM25'].mean():.2f} µg/m³")
print(f"  • Peak PM2.5 recorded      : {df['PM25'].max():.2f} µg/m³  ({df.loc[df['PM25'].idxmax(), 'City']})")
print(f"  • % Unhealthy days         : {(df['AQI_Category'].isin(['Unhealthy','Very Unhealthy','Hazardous']).sum()/len(df)*100):.1f}%")
print(f"  • Wind–PM2.5 correlation   : r = {r:.3f}  (p = {p:.4f})")
print(f"  • Highest CPI city         : {cpi_city.idxmax()} ({cpi_city.max():.4f})")
print(f"  • Lowest  CPI city         : {cpi_city.idxmin()} ({cpi_city.min():.4f})")
print("\n10 plots saved as plot_01 … plot_10 PNG files.")
print("=" * 60)
