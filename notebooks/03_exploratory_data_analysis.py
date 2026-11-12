
import pandas as pd
from pathlib import Path

# =====================================================
# 1. PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "global_superstore_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "reports" / "eda"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# 2. LOAD DATA
# =====================================================

df = pd.read_csv(INPUT_FILE)

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Fix floating-point discount inconsistencies
df["Discount"] = df["Discount"].round(2)

print("\n========================================")
print("GLOBAL SUPERSTORE BUSINESS ANALYSIS")
print("========================================")

print("\nDataset rows:", len(df))
print("Dataset columns:", len(df.columns))

# =====================================================
# 3. OVERALL BUSINESS PERFORMANCE
# =====================================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()
total_products = df["Product ID"].nunique()

profit_margin = (total_profit / total_sales) * 100

order_values = df.groupby("Order ID")["Sales"].sum()
average_order_value = order_values.mean()

print("\n========== BUSINESS PERFORMANCE ==========")
print(f"Total Sales: {total_sales:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Unique Products: {total_products:,}")
print(f"Average Order Value: {average_order_value:,.2f}")

# =====================================================
# 4. CATEGORY PERFORMANCE
# =====================================================

category_analysis = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum")
).reset_index()

category_analysis["Profit_Margin"] = (
    category_analysis["Total_Profit"] /
    category_analysis["Total_Sales"] * 100
)

print("\n========== CATEGORY PERFORMANCE ==========")
print(category_analysis.round(2).to_string(index=False))

# =====================================================
# 5. SUBCATEGORY PERFORMANCE
# =====================================================

subcategory_analysis = df.groupby("Sub-Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum")
).reset_index()

subcategory_analysis["Profit_Margin"] = (
    subcategory_analysis["Total_Profit"] /
    subcategory_analysis["Total_Sales"] * 100
)

top_subcategories = subcategory_analysis.sort_values(
    "Total_Profit", ascending=False
).head(10)

bottom_subcategories = subcategory_analysis.sort_values(
    "Total_Profit", ascending=True
).head(10)

print("\n========== TOP 10 SUBCATEGORIES BY PROFIT ==========")
print(top_subcategories.round(2).to_string(index=False))

print("\n========== BOTTOM 10 SUBCATEGORIES BY PROFIT ==========")
print(bottom_subcategories.round(2).to_string(index=False))

# =====================================================
# 6. REGIONAL PERFORMANCE
# =====================================================

region_analysis = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
    Customers=("Customer ID", "nunique")
).reset_index()

region_analysis["Profit_Margin"] = (
    region_analysis["Total_Profit"] /
    region_analysis["Total_Sales"] * 100
)

region_analysis = region_analysis.sort_values(
    "Total_Profit", ascending=False
)

print("\n========== REGIONAL PERFORMANCE ==========")
print(region_analysis.round(2).to_string(index=False))

# =====================================================
# 7. CUSTOMER SEGMENT PERFORMANCE
# =====================================================

segment_analysis = df.groupby("Segment").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
    Customers=("Customer ID", "nunique")
).reset_index()

segment_analysis["Profit_Margin"] = (
    segment_analysis["Total_Profit"] /
    segment_analysis["Total_Sales"] * 100
)

print("\n========== CUSTOMER SEGMENT PERFORMANCE ==========")
print(segment_analysis.round(2).to_string(index=False))

# Check orders assigned to multiple segments
segment_check = df.groupby("Order ID")["Segment"].nunique()

print("\n========== ORDER SEGMENT VALIDATION ==========")
print(
    "Orders appearing in multiple segments:",
    (segment_check > 1).sum()
)

print("Unique orders in dataset:", df["Order ID"].nunique())
print(
    "Sum of segment order counts:",
    segment_analysis["Orders"].sum()
)

# =====================================================
# 8. DISCOUNT ANALYSIS
# =====================================================

discount_analysis = df.groupby("Discount").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Transactions=("Order ID", "count")
).reset_index()

discount_analysis["Profit_Margin"] = (
    discount_analysis["Total_Profit"] /
    discount_analysis["Total_Sales"] * 100
)

discount_analysis = discount_analysis.sort_values("Discount")

print("\n========== DISCOUNT ANALYSIS ==========")
print(discount_analysis.round(2).to_string(index=False))

# =====================================================
# 9. ANNUAL PERFORMANCE
# =====================================================

df["Order Year"] = df["Order Date"].dt.year

year_analysis = df.groupby("Order Year").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique")
).reset_index()

year_analysis["Profit_Margin"] = (
    year_analysis["Total_Profit"] /
    year_analysis["Total_Sales"] * 100
)

print("\n========== ANNUAL PERFORMANCE ==========")
print(year_analysis.round(2).to_string(index=False))

# =====================================================
# 10. MONTHLY PERFORMANCE
# =====================================================

df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)

monthly_analysis = df.groupby("Order Month").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique")
).reset_index()

print("\n========== MONTHLY PERFORMANCE ==========")
print(monthly_analysis.round(2).to_string(index=False))

# =====================================================
# 11. PRODUCT PROFITABILITY
# =====================================================

product_analysis = df.groupby(
    ["Product ID", "Product Name"]
).agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Quantity_Sold=("Quantity", "sum")
).reset_index()

product_analysis["Profit_Margin"] = (
    product_analysis["Total_Profit"] /
    product_analysis["Total_Sales"] * 100
)

loss_products = product_analysis[
    product_analysis["Total_Profit"] < 0
].sort_values("Total_Profit").head(10)

print("\n========== 10 MOST LOSS-MAKING PRODUCTS ==========")
print(loss_products.round(2).to_string(index=False))

# =====================================================
# 12. SHIPPING PERFORMANCE
# =====================================================

df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

shipping_analysis = df.groupby("Ship Mode").agg(
    Average_Shipping_Days=("Shipping Days", "mean"),
    Average_Shipping_Cost=("Shipping Cost", "mean"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique")
).reset_index()

print("\n========== SHIPPING PERFORMANCE ==========")
print(shipping_analysis.round(2).to_string(index=False))

# =====================================================
# 13. SAVE ALL ANALYSIS RESULTS
# =====================================================

results = {
    "category_performance": category_analysis,
    "subcategory_performance": subcategory_analysis,
    "top_subcategories": top_subcategories,
    "bottom_subcategories": bottom_subcategories,
    "regional_performance": region_analysis,
    "customer_segment_performance": segment_analysis,
    "discount_analysis": discount_analysis,
    "annual_performance": year_analysis,
    "monthly_performance": monthly_analysis,
    "product_profitability": product_analysis,
    "loss_making_products": loss_products,
    "shipping_performance": shipping_analysis
}

for filename, table in results.items():
    table.to_csv(
        OUTPUT_DIR / f"{filename}.csv",
        index=False
    )

# =====================================================
# 14. FINAL SUMMARY
# =====================================================

print("\n========================================")
print("EDA COMPLETED SUCCESSFULLY")
print("========================================")

print("Analysis files generated:", len(results))
print("Output directory:", OUTPUT_DIR)
print("Original records preserved:", len(df))
