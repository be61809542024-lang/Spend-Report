import streamlit as st
import pandas as pd
import plotly.express as px

file_path = os.path.join("data", "procurement.xlsx")

# =========================
# PAGE CONFIG (optional but professional)
# =========================
st.set_page_config(page_title="Procurement Spend Dashboard", layout="wide")

# =========================
# TITLE
# =========================
st.title("PROCUREMENT SPEND REPORT")


# =========================
# LOAD DATA
# =========================
df = pd.read_excel("data/procurement.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Remove unnecessary index column if it exists
if "#" in df.columns:
    df = df.drop(columns=["#"])

# Ensure numeric fields are correct
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")

# Ensure Date is datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# =========================
# SEARCH FUNCTION
# =========================
st.subheader("Search Procurement Records")

search_term = st.text_input("Search Supplier or Item Description")

search_df = df.copy()

if search_term:
    search_df = search_df[
        search_df["Supplier/Service provider"].str.contains(search_term, case=False, na=False) |
        search_df["Item Description"].str.contains(search_term, case=False, na=False)
    ]

st.dataframe(search_df, use_container_width=True)

# =========================
# DRILL-DOWN FILTER
# =========================
st.subheader("Drill-down Analysis")

selected_category = st.selectbox(
    "Select Classification to Drill Down",
    ["All"] + sorted(df["Classification"].dropna().unique().tolist())
)

drill_df = df.copy()

if selected_category != "All":
    drill_df = drill_df[drill_df["Classification"] == selected_category]

# =========================
# KPIs
# =========================
total_spend = drill_df["Total"].sum()
total_lpos = drill_df["Lpo No."].nunique()
avg_transaction = drill_df["Total"].mean()
total_qty = drill_df["Qty"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Spend", f"KES {total_spend:,.0f}")
col2.metric("Total LPOs", total_lpos)
col3.metric("Avg Transaction", f"KES {avg_transaction:,.0f}")
col4.metric("Total Quantity", f"{total_qty:,.0f}")

st.divider()

# =========================
# EXECUTIVE SUMMARY
# =========================
st.subheader("Executive Summary")

top_department = drill_df.groupby("Department")["Total"].sum().idxmax()
top_supplier = drill_df.groupby("Supplier/Service provider")["Total"].sum().idxmax()
top_category = drill_df.groupby("Classification")["Total"].sum().idxmax()

monthly_trend = drill_df.groupby(pd.Grouper(key="Date", freq="ME"))["Total"].sum()

trend_direction = "Increasing 📈" if monthly_trend.iloc[-1] > monthly_trend.iloc[0] else "Decreasing 📉"

st.markdown(f"""
- Highest spending department: **{top_department}**
- Most utilized supplier: **{top_supplier}**
- Dominant category: **{top_category}**
- Overall spending trend: **{trend_direction}**
""")

# =========================
# CHART 1: CLASSIFICATION
# =========================
st.subheader("Procurement Spend by Classification")

classification_df = drill_df.groupby("Classification")["Total"].sum().reset_index()

fig1 = px.bar(
    classification_df,
    x="Classification",
    y="Total",
    text_auto=True,
    title="Spend by Classification"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# CHART 2: MONTHLY TREND
# =========================
st.subheader("Monthly Procurement Trend")

monthly_df = drill_df.groupby(pd.Grouper(key="Date", freq="ME"))["Total"].sum().reset_index()

fig2 = px.line(
    monthly_df,
    x="Date",
    y="Total",
    markers=True,
    title="Monthly Procurement Spend Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# CHART 3: TOP SUPPLIERS
# =========================
st.subheader("Top Suppliers by Spend")

supplier_df = drill_df.groupby("Supplier/Service provider")["Total"].sum().nlargest(10).reset_index()

fig3 = px.bar(
    supplier_df,
    x="Supplier/Service provider",
    y="Total",
    text_auto=True,
    title="Top 10 Suppliers"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# CHART 4: DEPARTMENT ANALYSIS
# =========================
st.subheader("Spend by Department")

dept_df = drill_df.groupby("Department")["Total"].sum().reset_index()

fig4 = px.bar(
    dept_df,
    x="Department",
    y="Total",
    text_auto=True,
    title="Procurement Spend by Department"
)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# CHART 5: CAMPUS DISTRIBUTION
# =========================
st.subheader("Spend by Campus")

campus_df = drill_df.groupby("Campus")["Total"].sum().reset_index()

fig5 = px.pie(
    campus_df,
    names="Campus",
    values="Total",
    title="Campus Procurement Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# =========================
# DRILL-DOWN TABLE
# =========================
st.subheader("Detailed Procurement View")

detail_view = drill_df[[
    "Lpo No.",
    "Date",
    "Supplier/Service provider",
    "Department",
    "Campus",
    "Classification",
    "Specific Category",
    "Item Description",
    "Qty",
    "Total"
]].sort_values(by="Total", ascending=False)

st.dataframe(detail_view, use_container_width=True)
