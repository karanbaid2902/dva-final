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

# Professional Corporate Header (No mention of project)
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .company-sub { font-size: 16px; color: #4B5563; margin-bottom: 25px; border-bottom: 2px solid #E5E7EB; padding-bottom: 10px; }
    </style>
    <div class="main-title">Apex Global Analytics Portal</div>
    <div class="company-sub">Enterprise Sales & Operations Dashboard | Internal Corporate Access</div>
    """, unsafe_allow_html=True)

# --- THE "NUCLEAR" DATA ENGINE ---
def get_data():
    file_path = 'ecommerce_data.csv'
    # List of columns we absolutely need
    required_cols = ['Order_ID', 'Date', 'Category', 'Product', 'Price', 'Quantity', 'Revenue', 'Region', 'Channel', 'Payment', 'Customer_Age', 'Rating', 'Delivery_Days']
    
    # Check if we need to regenerate
    regenerate = False
    if not os.path.exists(file_path):
        regenerate = True
    else:
        # Check if the existing file is missing any columns
        existing_df = pd.read_csv(file_path, nrows=1)
        if not all(col in existing_df.columns for col in required_cols):
            regenerate = True
            os.remove(file_path) # Delete the "bad" file

    if regenerate:
        categories = ['Electronics', 'Home & Kitchen', 'Fashion', 'Beauty', 'Sports']
        regions = ['North', 'South', 'East', 'West', 'Central']
        channels = ['Direct', 'Social Media', 'Email', 'Affiliate']
        
        data = []
        for i in range(2000):
            cat = random.choice(categories)
            price = random.uniform(200, 1200) if cat == 'Electronics' else random.uniform(20, 400)
            qty = random.randint(1, 5)
            data.append({
                'Order_ID': f"ORD-{5000+i}",
                'Date': datetime(2023, 1, 1) + timedelta(days=random.randint(0, 364)),
                'Category': cat,
                'Product': f"{cat} SKU-{random.randint(100, 999)}",
                'Price': round(price, 2),
                'Quantity': qty,
                'Revenue': round(price * qty, 2),
                'Region': random.choice(regions),
                'Channel': random.choice(channels),
                'Payment': random.choice(['Credit Card', 'PayPal', 'Crypto', 'Debit Card']),
                'Customer_Age': random.randint(18, 72),
                'Rating': random.randint(1, 5),
                'Delivery_Days': random.randint(1, 8)
            })
        df_new = pd.DataFrame(data)
        df_new.to_csv(file_path, index=False)
    
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = get_data()

# --- NAVIGATION ---
st.sidebar.title("Management Hub")
page = st.sidebar.radio("Navigation", ["Executive Overview", "Sales Trends", "Customer Behavior", "Product Analysis", "Regional Insights"])

# --- 1. EXECUTIVE OVERVIEW ---
if page == "Executive Overview":
    st.subheader("Key Performance Indicators")
    cols = st.columns(4)
    cols[0].metric("Total Revenue", f"${df['Revenue'].sum():,.0f}")
    cols[1].metric("Total Units", f"{df['Quantity'].sum():,}")
    cols[2].metric("Avg Order Value", f"${df['Revenue'].mean():,.2f}")
    cols[3].metric("Avg Rating", f"{df['Rating'].mean():.1f} / 5")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(df, values='Revenue', names='Category', hole=0.5, title="Revenue Share by Category"), use_container_width=True)
    with c2:
        rev_trend = df.groupby('Date')['Revenue'].sum().reset_index()
        st.plotly_chart(px.line(rev_trend, x='Date', y='Revenue', title="Daily Revenue Stream"), use_container_width=True)

# --- 2. SALES TRENDS ---
elif page == "Sales Trends":
    st.subheader("Market Dynamics")
    df_monthly = df.set_index('Date').resample('M')['Revenue'].sum().reset_index()
    st.plotly_chart(px.area(df_monthly, x='Date', y='Revenue', title="Monthly Revenue Growth"), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        df['Day'] = df['Date'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_sales = df.groupby('Day')['Revenue'].sum().reindex(day_order).reset_index()
        st.plotly_chart(px.bar(day_sales, x='Day', y='Revenue', title="Weekly Purchase Patterns"), use_container_width=True)
    with c2:
        st.plotly_chart(px.pie(df, names="Channel", values="Revenue", title="Channel Contribution"), use_container_width=True)
    
    st.plotly_chart(px.box(df, x="Payment", y="Revenue", color="Payment", title="Transaction Value by Payment Type"), use_container_width=True)

# --- 3. CUSTOMER BEHAVIOR ---
elif page == "Customer Behavior":
    st.subheader("Demographics & Sentiment")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.histogram(df, x="Customer_Age", nbins=20, title="Customer Age Distribution", color_discrete_sequence=['#3B82F6']), use_container_width=True)
    with c2:
        st.plotly_chart(px.violin(df, y="Rating", x="Category", box=True, title="Customer Satisfaction by Category"), use_container_width=True)
    
    st.plotly_chart(px.scatter(df, x="Customer_Age", y="Revenue", color="Category", title="Age vs. Spending Correlation"), use_container_width=True)

# --- 4. PRODUCT ANALYSIS ---
elif page == "Product Analysis":
    st.subheader("Inventory & SKU Intelligence")
    top_10 = df.groupby('Product')['Revenue'].sum().nlargest(10).reset_index()
    st.plotly_chart(px.bar(top_10, x='Revenue', y='Product', orientation='h', title="Top 10 High-Performing SKUs", color='Revenue'), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.density_heatmap(df, x="Price", y="Quantity", title="Price Point Demand Heatmap"), use_container_width=True)
    with c2:
        st.plotly_chart(px.histogram(df, x="Delivery_Days", title="Logistics Performance (Delivery Days)"), use_container_width=True)

# --- 5. REGIONAL INSIGHTS ---
elif page == "Regional Insights":
    st.subheader("Geographic Market Distribution")
    st.plotly_chart(px.sunburst(df, path=['Region', 'Category'], values='Revenue', title="Regional Revenue Hierarchies"), use_container_width=True)
    
    reg_summary = df.groupby('Region').agg({'Revenue':'sum', 'Quantity':'sum'}).reset_index()
    st.plotly_chart(px.bar(reg_summary, x='Region', y='Revenue', color='Quantity', title="Regional Revenue vs. Volume"), use_container_width=True)
    
    st.plotly_chart(px.scatter(df.groupby(['Region', 'Channel'])['Revenue'].sum().reset_index(), 
                               x="Region", y="Revenue", color="Channel", title="Channel Performance by Region"), use_container_width=True)