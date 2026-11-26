from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "survey_data.csv"
OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)

def clean_data(df):
    df = df.copy()
    df = df.drop_duplicates()
    df["Commute_Mode"] = df["Commute_Mode"].astype(str).str.strip().str.title()
    df["Distance_km"] = pd.to_numeric(df["Distance_km"], errors="coerce")
    df["Travel_Time_min"] = pd.to_numeric(df["Travel_Time_min"], errors="coerce")
    df["Daily_Cost_INR"] = pd.to_numeric(df["Daily_Cost_INR"], errors="coerce")
    for col in ["Distance_km", "Travel_Time_min", "Daily_Cost_INR"]:
        df[col] = df[col].fillna(df[col].median())
    df = df[(df["Distance_km"] >= 0) & (df["Travel_Time_min"] >= 0) & (df["Daily_Cost_INR"] >= 0)]
    return df

def main():
    raw = pd.read_csv(DATA)
    clean = clean_data(raw)
    clean.to_csv(ROOT / "data" / "cleaned_data.csv", index=False)
    mode_counts = clean["Commute_Mode"].value_counts()
    avg_mode_cost = clean.groupby("Commute_Mode")["Daily_Cost_INR"].mean().sort_values()
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(9,5)); mode_counts.plot(kind="bar"); plt.title("Students by Commute Mode"); plt.ylabel("Student Count"); plt.tight_layout(); plt.savefig(OUT/"commute_modes.png", dpi=160); plt.close()
    plt.figure(figsize=(7,7)); mode_counts.plot(kind="pie", autopct="%1.1f%%", startangle=90); plt.title("Commute Mode Share"); plt.ylabel(""); plt.tight_layout(); plt.savefig(OUT/"mode_share.png", dpi=160); plt.close()
    plt.figure(figsize=(8,5)); plt.hist(clean["Distance_km"], bins=12, edgecolor="black"); plt.title("Commute Distance Distribution"); plt.xlabel("Distance (km)"); plt.tight_layout(); plt.savefig(OUT/"distance_histogram.png", dpi=160); plt.close()
    plt.figure(figsize=(10,5)); sns.boxplot(data=clean, x="Commute_Mode", y="Travel_Time_min"); plt.title("Travel Time by Mode"); plt.xticks(rotation=25); plt.tight_layout(); plt.savefig(OUT/"travel_time_boxplot.png", dpi=160); plt.close()
    plt.figure(figsize=(8,5)); sns.scatterplot(data=clean, x="Distance_km", y="Travel_Time_min", hue="Commute_Mode"); plt.title("Distance vs Travel Time"); plt.tight_layout(); plt.savefig(OUT/"distance_time_scatter.png", dpi=160); plt.close()
    pivot = clean.pivot_table(index="Year", columns="Commute_Mode", values="Student_ID", aggfunc="count", fill_value=0)
    plt.figure(figsize=(10,5)); sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues"); plt.title("Year vs Commute Mode"); plt.tight_layout(); plt.savefig(OUT/"year_mode_heatmap.png", dpi=160); plt.close()
    plt.figure(figsize=(8,5)); avg_mode_cost.plot(kind="bar"); plt.title("Average Daily Commute Cost by Mode"); plt.ylabel("INR"); plt.tight_layout(); plt.savefig(OUT/"average_cost_by_mode.png", dpi=160); plt.close()
    year_mode = pd.crosstab(clean["Year"], clean["Commute_Mode"])
    year_mode.plot(kind="bar", stacked=True, figsize=(10,5)); plt.title("Year-wise Commute Mode"); plt.ylabel("Students"); plt.tight_layout(); plt.savefig(OUT/"year_stacked_modes.png", dpi=160); plt.close()
    # Illustrative emission factors (kg CO2 per passenger-km); not official campus-specific values.
    factors = {"Bus":0.08,"Car":0.18,"Carpool":0.09,"Motorbike":0.10,"Bicycle":0.0,"Walking":0.0,"Auto-Rickshaw":0.11}
    clean["Estimated_kg_CO2_oneway"] = clean.apply(lambda r: r["Distance_km"]*factors.get(r["Commute_Mode"],0.12), axis=1)
    clean["Commute_Burden_Score"] = (clean["Travel_Time_min"]/clean["Travel_Time_min"].max()*40 + clean["Distance_km"]/clean["Distance_km"].max()*35 + clean["Daily_Cost_INR"]/max(clean["Daily_Cost_INR"].max(),1)*25).round(1)
    clean.to_csv(ROOT/"data"/"cleaned_data.csv", index=False)
    print(f"Rows after cleaning: {len(clean)}")
    print(f"Average distance (km): {clean.Distance_km.mean():.2f}")
    print(f"Average one-way travel time (min): {clean.Travel_Time_min.mean():.1f}")
    print(f"Average daily cost (INR): {clean.Daily_Cost_INR.mean():.2f}")
    print(f"Most popular mode: {mode_counts.idxmax()} ({mode_counts.max()} students)")
    print("Generated 8 charts in images/")
if __name__ == "__main__":
    main()
