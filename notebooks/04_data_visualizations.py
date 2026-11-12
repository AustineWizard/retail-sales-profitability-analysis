
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


 
# 1. PROJECT PATHS
 

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "global_superstore_cleaned.csv"

OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


 
# 2. LOAD DATA
 

print("Loading cleaned dataset...")

df = pd.read_csv(DATA_FILE)

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df["Discount"] = df["Discount"].round(2)
df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print(f"Dataset loaded: {len(df):,} rows")


 
# 3. CHART STYLE
 

plt.rcParams.update({
    "figure.figsize": (12, 7),
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 15,
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.axisbelow": True
})


def save_chart(filename):
    """Save chart and close the figure."""
    path = OUTPUT_DIR / filename
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {filename}")


def format_axis(axis):
    axis.xaxis.set_major_formatter(
        ticker.StrMethodFormatter("{x:,.0f}")
    )


 
# 4. CATEGORY PERFORMANCE
 

category = (
    df.groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Sales", ascending=False)
)

fig, axes = plt.subplots(1, 2, figsize=(13, 6))

axes[0].bar(category.index, category["Sales"])
axes[0].set_title("Sales by Product Category")
axes[0].set_ylabel("Sales")
axes[0].tick_params(axis="x", rotation=20)
format_axis(axes[0])

axes[1].bar(category.index, category["Profit"])
axes[1].set_title("Profit by Product Category")
axes[1].set_ylabel("Profit")
axes[1].tick_params(axis="x", rotation=20)
format_axis(axes[1])

fig.suptitle(
    "Retail Sales and Profitability by Category",
    fontsize=17,
    fontweight="bold"
)

save_chart("01_category_performance.png")


 
# 5. REGIONAL PROFITABILITY
 

region = (
    df.groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Profit")
)

plt.figure(figsize=(12, 8))

plt.barh(region.index, region["Profit"])

plt.title(
    "Profitability by Region",
    fontweight="bold"
)
plt.xlabel("Total Profit")
plt.ylabel("Region")

plt.axvline(0, linewidth=1)

save_chart("02_regional_profitability.png")


 
# 6. MONTHLY SALES TREND
 

df["Order Month"] = df["Order Date"].dt.to_period("M")

monthly = (
    df.groupby("Order Month")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

monthly["Order Month"] = monthly["Order Month"].astype(str)

plt.figure(figsize=(15, 7))

plt.plot(
    monthly["Order Month"],
    monthly["Sales"],
    linewidth=2
)

plt.title(
    "Monthly Sales Trend (2011–2014)",
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(
    range(0, len(monthly), 3),
    monthly["Order Month"].iloc[::3],
    rotation=45
)

format_axis(plt.gca())

save_chart("03_monthly_sales_trend.png")


 
# 7. MONTHLY PROFIT TREND
 

plt.figure(figsize=(15, 7))

plt.plot(
    monthly["Order Month"],
    monthly["Profit"],
    linewidth=2
)

plt.axhline(0, linewidth=1)

plt.title(
    "Monthly Profit Trend (2011–2014)",
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Profit")

plt.xticks(
    range(0, len(monthly), 3),
    monthly["Order Month"].iloc[::3],
    rotation=45
)

format_axis(plt.gca())

save_chart("04_monthly_profit_trend.png")


 
# 8. DISCOUNT AND PROFITABILITY
 

discount = (
    df.groupby("Discount")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

discount["Profit Margin"] = (
    discount["Profit"] / discount["Sales"] * 100
)

plt.figure(figsize=(12, 7))

plt.plot(
    discount["Discount"] * 100,
    discount["Profit Margin"],
    marker="o",
    linewidth=2
)

plt.axhline(0, linewidth=1)

plt.title(
    "Relationship Between Discount and Profit Margin",
    fontweight="bold"
)

plt.xlabel("Discount (%)")
plt.ylabel("Profit Margin (%)")

save_chart("05_discount_profitability.png")


 
# 9. SUBCATEGORY PROFITABILITY
 

subcategory = (
    df.groupby("Sub-Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Profit")
)

fig, axes = plt.subplots(1, 2, figsize=(16, 9))

axes[0].barh(
    subcategory.index,
    subcategory["Profit"]
)

axes[0].set_title("Profit by Subcategory")
axes[0].set_xlabel("Profit")
axes[0].axvline(0, linewidth=1)

axes[1].barh(
    subcategory.index,
    subcategory["Sales"]
)

axes[1].set_title("Sales by Subcategory")
axes[1].set_xlabel("Sales")

format_axis(axes[0])
format_axis(axes[1])

fig.suptitle(
    "Product Subcategory Performance",
    fontsize=17,
    fontweight="bold"
)

save_chart("06_subcategory_performance.png")


 
# 10. CUSTOMER SEGMENT PERFORMANCE
 

segment = (
    df.groupby("Segment")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

fig, axes = plt.subplots(1, 2, figsize=(13, 6))

axes[0].bar(segment.index, segment["Sales"])
axes[0].set_title("Sales by Customer Segment")
axes[0].set_ylabel("Sales")
format_axis(axes[0])

axes[1].bar(segment.index, segment["Profit"])
axes[1].set_title("Profit by Customer Segment")
axes[1].set_ylabel("Profit")
format_axis(axes[1])

fig.suptitle(
    "Customer Segment Performance",
    fontsize=17,
    fontweight="bold"
)

save_chart("07_customer_segment_performance.png")


 
# 11. SHIPPING PERFORMANCE
 

shipping = (
    df.groupby("Ship Mode")
    .agg(
        Average_Shipping_Days=("Shipping Days", "mean"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Average_Shipping_Days")
)

plt.figure(figsize=(11, 6))

plt.bar(
    shipping.index,
    shipping["Average_Shipping_Days"]
)

plt.title(
    "Average Shipping Time by Shipping Mode",
    fontweight="bold"
)

plt.xlabel("Shipping Mode")
plt.ylabel("Average Shipping Days")

plt.xticks(rotation=15)

save_chart("08_shipping_performance.png")



# 12. COMPLETION SUMMARY

print("\n" + "=" * 55)
print("DATA VISUALIZATION COMPLETED SUCCESSFULLY")
print("=" * 55)

print(f"Total charts generated: 8")
print(f"Output folder: {OUTPUT_DIR}")

for file in sorted(OUTPUT_DIR.glob("*.png")):
    print(f" - {file.name}")

print("\nAll charts have been saved successfully.")
