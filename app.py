import plotly.express as px
import plotly.graph_objects as go
import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- AUTOMATIC DATA GENERATOR ---
def create_data_if_missing():
    if not os.path.exists('ecommerce_data.csv'):
        # Generate 1,000 rows of synthetic data if the file is missing
        categories = ['Electronics', 'Home & Kitchen', 'Fashion', 'Beauty', 'Sports']
        data = []
        for i in range(1000):
            cat = random.choice(categories)
            price = random.uniform(10, 500) if cat != 'Electronics' else random.uniform(100, 1500)
            data.append({
                'Order_ID': f"ORD-{1000+i}",
                'Date': datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)),
                'Category': cat,
                'Revenue': price * random.randint(1, 5),
                'Region': random.choice(['North', 'South', 'East', 'West', 'Central']),
                'Channel': random.choice(['Direct', 'Social', 'Email']),
                'Payment': random.choice(['Credit Card', 'PayPal', 'Crypto']),
                'Customer_Age': random.randint(18, 70),
                'Rating': random.randint(1, 5),
                'Delivery_Days': random.randint(1, 10)
            })
        df_new = pd.DataFrame(data)
        df_new.to_csv('ecommerce_data.csv', index=False)

# Call the generator before loading
create_data_if_missing()

@st.cache_data
def load_data():
    df = pd.read_csv('ecommerce_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()
# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Executive Overview", "Sales Trends", "Customer Behavior", "Product Analysis", "Regional Insights"])

# --- SECTION 1: EXECUTIVE OVERVIEW ---
if page == "Executive Overview":
    st.title("🚀 Executive Overview")
    
    # KPIs (4 Charts/Metrics)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Revenue", f"${df['Revenue'].sum():,.0f}")
    m2.metric("Total Orders", f"{df['Order_ID'].nunique():,}")
    m3.metric("Avg Order Value", f"${df['Revenue'].mean():,.2f}")
    m4.metric("Avg Rating", f"{df['Rating'].mean():.1f} ⭐")

    col1, col2 = st.columns(2)
    with col1:
        # Chart 5: Revenue Contribution by Category
        fig5 = px.pie(df, values='Revenue', names='Category', hole=0.4, title="Revenue by Category")
        st.plotly_chart(fig5, use_container_width=True)
    with col2:
        # Chart 6: Cumulative Revenue
        df_cum = df.groupby('Date')['Revenue'].sum().cumsum().reset_index()
        fig6 = px.area(df_cum, x='Date', y='Revenue', title="Cumulative Revenue Growth")
        st.plotly_chart(fig6, use_container_width=True)

# --- SECTION 2: SALES TRENDS ---
elif page == "Sales Trends":
    st.title("📈 Sales & Growth Analysis")
    
    # Chart 7: Monthly Sales
    df_monthly = df.set_index('Date').resample('M')['Revenue'].sum().reset_index()
    fig7 = px.line(df_monthly, x='Date', y='Revenue', title="Monthly Sales Trend", markers=True)
    st.plotly_chart(fig7, use_container_width=True)

    c1, c2 = st.columns(2)
    # Chart 8: Sales by Day of Week
    df['Day'] = df['Date'].dt.day_name()
    fig8 = px.bar(df.groupby('Day')['Revenue'].sum().reset_index(), x='Day', y='Revenue', title="Sales by Day of Week")
    c1.plotly_chart(fig8)
    
    # Chart 9: Payment Method Distribution
    fig9 = px.histogram(df, x="Payment", title="Payment Method Preference", color="Payment")
    c2.plotly_chart(fig9)

    # Chart 10: Sales Channel ROI
    fig10 = px.box(df, x="Channel", y="Revenue", title="Revenue Distribution by Channel", color="Channel")
    st.plotly_chart(fig10, use_container_width=True)

# --- SECTION 3: CUSTOMER BEHAVIOR ---
elif page == "Customer Behavior":
    st.title("👥 Customer Intelligence")
    
    c1, c2 = st.columns(2)
    # Chart 11: Age vs Revenue Scatter
    fig11 = px.scatter(df, x="Customer_Age", y="Revenue", color="Category", title="Age vs. Spending Correlation")
    c1.plotly_chart(fig11)
    
    # Chart 12: Rating Distribution
    fig12 = px.violin(df, y="Rating", x="Category", box=True, title="Customer Ratings by Category")
    c2.plotly_chart(fig12)

    # Chart 13: Conversion Funnel (Mockup data for Master's logic)
    funnel_data = dict(number=[10000, 4500, 2200, 1100], stage=["Visited", "Added to Cart", "Checkout", "Purchased"])
    fig13 = px.funnel(funnel_data, x='number', y='stage', title="Customer Purchase Funnel")
    st.plotly_chart(fig13, use_container_width=True)

# --- SECTION 4: PRODUCT ANALYSIS ---
elif page == "Product Analysis":
    st.title("📦 Product & Inventory Performance")
    
    # Chart 14: Top 10 Products
    top_prods = df.groupby('Product')['Revenue'].sum().nlargest(10).reset_index()
    fig14 = px.bar(top_prods, x='Revenue', y='Product', orientation='h', title="Top 10 Products by Revenue")
    st.plotly_chart(fig14, use_container_width=True)

    c1, c2 = st.columns(2)
    # Chart 15: Price vs Quantity Correlation
    fig15 = px.density_heatmap(df, x="Price", y="Quantity", title="Price-Quantity Heatmap")
    c1.plotly_chart(fig15)
    
    # Chart 16: Delivery Performance
    fig16 = px.histogram(df, x="Delivery_Days", title="Delivery Time Distribution (Days)")
    c2.plotly_chart(fig16)

# --- SECTION 5: REGIONAL INSIGHTS ---
elif page == "Regional Insights":
    st.title("🌍 Geospatial & Regional Analysis")
    
    # Chart 17: Regional Revenue Breakdown
    fig17 = px.sunburst(df, path=['Region', 'Category'], values='Revenue', title="Regional Category Composition")
    st.plotly_chart(fig17, use_container_width=True)
    
    # Chart 18: Map (Since data is generic, we use a Bubble chart for Regions)
    reg_data = df.groupby('Region').agg({'Revenue':'sum', 'Quantity':'count'}).reset_index()
    fig18 = px.scatter(reg_data, x="Region", y="Revenue", size="Quantity", color="Region", title="Regional Revenue Scale")
    st.plotly_chart(fig18, use_container_width=True)