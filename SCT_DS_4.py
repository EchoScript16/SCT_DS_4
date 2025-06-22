import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap

# 1. Load CSV (no weather merge)
df = pd.read_csv(r"C:\Users\Bhakti\Downloads\accidents\NYC_Accidents.csv", low_memory=False)
df["CRASH DATE"] = pd.to_datetime(df["CRASH DATE"], errors="coerce")

# 2. Preprocessing
df = df.dropna(subset=["CRASH DATE", "LATITUDE", "LONGITUDE"])
df["hour"] = df["CRASH DATE"].dt.hour
df["weekday"] = df["CRASH DATE"].dt.day_name()
df["month"] = df["CRASH DATE"].dt.to_period("M")

# 3. Visualizations
sns.countplot(x="hour", data=df)
plt.title("Crashes by Hour"); plt.tight_layout(); plt.savefig("crash_hour.png"); plt.close()

sns.countplot(x="weekday", data=df, order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
plt.title("Crashes by Weekday"); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig("crash_weekday.png"); plt.close()

df["CONTRIBUTING FACTOR VEHICLE 1"].value_counts().nlargest(10).plot(kind="barh", color="orange")
plt.title("Top 10 Contributing Factors"); plt.tight_layout(); plt.savefig("top_factors.png"); plt.close()

df.groupby("month").size().plot()
plt.title("Monthly Accident Trend"); plt.ylabel("Count"); plt.xticks(rotation=45); plt.tight_layout(); plt.savefig("monthly_trend.png"); plt.close()

# 4. Heatmap
m = folium.Map(location=[df.LATITUDE.mean(), df.LONGITUDE.mean()], zoom_start=10)
HeatMap(df[["LATITUDE", "LONGITUDE"]].dropna().sample(10000), radius=6).add_to(m)
m.save("nyc_accident_hotspots.html")
print("✅ Map saved: nyc_accident_hotspots.html")

# 5. Export to Excel
df.to_csv("nyc_accidents_cleaned.csv", index=False)
print("✅ CSV exported: nyc_accidents_cleaned.csv")