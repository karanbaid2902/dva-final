import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# --- BRANDING & CONFIG ---
st.set_page_config(page_title="Apex Global | Sales Intelligence", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .company-sub { font-size: 16px; color: #4B5563; margin-bottom: 25px; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; }
    </style>
    <div class="main-title">Apex Global Analytics Portal</div>
    <div class="company-sub">Enterprise Sales & Operations Dashboard | Internal Corporate Access</div>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def get_data():
    file_path = 'ecommerce_data.csv'
    if not os.path.exists(file_path):
        categories = ['Electronics', 'Home & Kitchen', 'Fashion', 'Beauty', 'Sports']
        regions = ['North', 'South', 'East', 'West', 'Central']
        data = []
        for i in range(2500):
            cat = random.choice(categories)
            price = random.uniform(200, 1200) if cat == 'Electronics' else random.uniform(20, 400)
            data.append({
                'Order_ID': f"ORD-{7000+i}",
                'Date': datetime(2023, 1, 1) + timedelta(days=random.randint(0, 364)),
                'Category': cat,
                'Product': f"{cat} SKU-{random.randint(100, 999)}",
                'Price': round(price, 2),
                'Quantity': random.randint(1, 5),
                'Revenue': 0, 
                'Region': random.choice(regions),
                'Channel': random.choice(['Direct', 'Social Media', 'Email', 'Affiliate']),
                'Payment': random.choice(['Credit Card', 'PayPal', 'Crypto', 'Debit Card']),
                'Customer_Age': random.randint(18, 72),
                'Rating': random.randint(1, 5),
                'Delivery_Days': random.randint(1, 8)
            })
        df_new = pd.DataFrame(data)
        df_new['Revenue'] = df_new['Price'] * df_new['Quantity']
        df_new.to_csv(file_path, index=False)
    
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

raw_df = get_data()

# --- SIDEBAR FILTERS ---
st.sidebar.title("Global Filters")

# 1. Date Range Filter
min_date = raw_df['Date'].min().to_pydatetime()
max_date = raw_df['Date'].max().to_pydatetime()
date_range = st.sidebar.date_input("Filter by Date Range", [min_date, max_date])

# 2. Region Multi-select
all_regions = sorted(raw_df['Region'].unique())
selected_regions = st.sidebar.multiselect("Filter by Regions", all_regions, default=all_regions)

# 3. Category Multi-select
all_cats = sorted(raw_df['Category'].unique())
selected_cats = st.sidebar.multiselect("Filter by Categories", all_cats, default=all_cats)

# --- APPLY FILTERS ---
# Handle date_range being a single value during selection
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

mask = (
    (raw_df['Date'].dt.date >= start_date) & 
    (raw_df['Date'].dt.date <= end_date) &
    (raw_df['Region'].isin(selected_regions)) &
    (raw_df['Category'].isin(selected_cats))
)
df = raw_df.loc[mask]

# --- NAVIGATION ---
st.sidebar.markdown("---")
page = st.sidebar.radio("Analysis Module", ["Executive Overview", "Sales Trends", "Customer Behavior", "Product Analysis", "Regional Insights"])

# --- RESET & DOWNLOAD ---
st.sidebar.markdown("---")
if st.sidebar.button("Reset All Filters"):
    st.rerun()

@st.cache_data
def convert_df(df_to_download):
    return df_to_download.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    label="Export Filtered Data (CSV)",
    data=convert_df(df),
    file_name='apex_filtered_report.csv',
    mime='text/csv'
)

# --- 1. EXECUTIVE OVERVIEW ---
if page == "Executive Overview":
    st.subheader("Key Performance Indicators")
    cols = st.columns(4)
    cols[0].metric("Total Revenue", f"${df['Revenue'].sum():,.0f}")
    cols[1].metric("Filtered Orders", f"{len(df):,}")
    cols[2].metric("Avg Unit Price", f"${df['Price'].mean():,.2f}")
    cols[3].metric("Avg Delivery Time", f"{df['Delivery_Days'].mean():.1f} Days")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(df, values='Revenue', names='Category', hole=0.5, title="Revenue Share"), use_container_width=True)
    with c2:
        rev_trend = df.groupby('Date')['Revenue'].sum().reset_index()
        st.plotly_chart(px.line(rev_trend, x='Date', y='Revenue', title="Filtered Revenue Over Time"), use_container_width=True)

# --- 2. SALES TRENDS ---
elif page == "Sales Trends":
    st.subheader("Market Dynamics")
    df_monthly = df.set_index('Date').resample('ME')['Revenue'].sum().reset_index()
    st.plotly_chart(px.area(df_monthly, x='Date', y='Revenue', title="Monthly Revenue Stream"), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        df_day = df.copy()
        df_day['Day'] = df_day['Date'].dt.day_name()
        day_sales = df_day.groupby('Day')['Revenue'].sum().reset_index()
        st.plotly_chart(px.bar(day_sales, x='Day', y='Revenue', title="Weekly Purchase Patterns"), use_container_width=True)
    with c2:
        st.plotly_chart(px.pie(df, names="Channel", values="Revenue", title="Channel Contribution"), use_container_width=True)

# --- 3. CUSTOMER BEHAVIOR ---
elif page == "Customer Behavior":
    st.subheader("Demographics & Sentiment")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.histogram(df, x="Customer_Age", title="Filtered Age Distribution"), use_container_width=True)
    with c2:
        st.plotly_chart(px.box(df, x="Category", y="Rating", title="Satisfaction Scores by Category"), use_container_width=True)
    
    st.plotly_chart(px.scatter(df, x="Customer_Age", y="Revenue", color="Category", title="Spending Correlation"), use_container_width=True)

# --- 4. PRODUCT ANALYSIS ---
elif page == "Product Analysis":
    st.subheader("Inventory & SKU Intelligence")
    top_10 = df.groupby('Product')['Revenue'].sum().nlargest(10).reset_index()
    st.plotly_chart(px.bar(top_10, x='Revenue', y='Product', orientation='h', title="Top 10 Performers (Filtered)"), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.density_heatmap(df, x="Price", y="Quantity", title="Price-Demand Heatmap"), use_container_width=True)
    with c2:
        st.plotly_chart(px.histogram(df, x="Delivery_Days", title="Logistics Lead Times"), use_container_width=True)

# --- 5. REGIONAL INSIGHTS ---
elif page == "Regional Insights":
    st.subheader("Geographic Market Distribution")
    st.plotly_chart(px.sunburst(df, path=['Region', 'Category'], values='Revenue', title="Regional Revenue Hierarchies"), use_container_width=True)
    
    reg_summary = df.groupby('Region').agg({'Revenue':'sum', 'Quantity':'sum'}).reset_index()
    st.plotly_chart(px.bar(reg_summary, x='Region', y='Revenue', color='Quantity', title="Regional Revenue vs Volume"), use_container_width=True)