import os
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG & BRANDING ---
st.set_page_config(page_title="Apex Global | Executive Dashboard", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main-title { font-size: 36px; font-weight: bold; color: #1E3A8A; }
    .company-name { font-size: 18px; color: #6B7280; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🚀 Sales Performance Control Tower</div>', unsafe_allow_html=True)
st.markdown('<div class="company-name">Apex Global Retail Solutions | Master\'s Project v1.2</div>', unsafe_allow_html=True)

# --- AUTOMATIC DATA GENERATOR (Robust Version) ---
def create_data_if_missing():
    if not os.path.exists('ecommerce_data.csv'):
        categories = ['Electronics', 'Home & Kitchen', 'Fashion', 'Beauty', 'Sports']
        regions = ['North', 'South', 'East', 'West', 'Central']
        channels = ['Direct', 'Social Media', 'Email', 'Affiliate']
        
        data = []
        for i in range(2000): # 2,000 rows for better visualization
            cat = random.choice(categories)
            # Electronics are more expensive
            price = random.uniform(200, 1200) if cat == 'Electronics' else random.uniform(10, 400)
            qty = random.randint(1, 5)
            
            data.append({
                'Order_ID': f"ORD-{1000+i}",
                'Customer_ID': f"CUST-{random.randint(1, 500)}",
                'Date': datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)),
                'Category': cat,
                'Product': f"{cat} Item {random.randint(1, 20)}", # Fixes Product KeyError
                'Price': round(price, 2),
                'Quantity': qty, # Fixes Quantity KeyError
                'Revenue': round(price * qty, 2),
                'Region': random.choice(regions),
                'Channel': random.choice(channels),
                'Payment': random.choice(['Credit Card', 'PayPal', 'Crypto', 'Debit Card']),
                'Customer_Age': random.randint(18, 75),
                'Rating': random.randint(1, 5),
                'Delivery_Days': random.randint(1, 10)
            })
        df_new = pd.DataFrame(data)
        df_new.to_csv('ecommerce_data.csv', index=False)

create_data_if_missing()

@st.cache_data
def load_data():
    df = pd.read_csv('ecommerce_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://via.placeholder.com/150x50?text=APEX+GLOBAL", use_container_width=True)
st.sidebar.title("Management Hub")
page = st.sidebar.radio("Analysis Module", ["Executive Overview", "Sales Trends", "Customer Behavior", "Product Analysis", "Regional Insights"])

# --- SECTION 1: EXECUTIVE OVERVIEW ---
if page == "Executive Overview":
    st.subheader("📊 High-Level Metrics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Revenue", f"${df['Revenue'].sum():,.0f}", "+12%")
    m2.metric("Total Orders", f"{df['Order_ID'].nunique():,}")
    m3.metric("Avg Order Value", f"${df['Revenue'].mean():,.2f}")
    m4.metric("Customer Sat", f"{df['Rating'].mean():.1f} / 5.0")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(df, values='Revenue', names='Category', hole=0.4, title="Revenue Share"), use_container_width=True)
    with c2:
        df_cum = df.groupby('Date')['Revenue'].sum().cumsum().reset_index()
        st.plotly_chart(px.area(df_cum, x='Date', y='Revenue', title="Year-to-Date Growth"), use_container_width=True)

# --- SECTION 2: SALES TRENDS ---
elif page == "Sales Trends":
    st.subheader("📈 Time-Series & Channel Analysis")
    df_monthly = df.set_index('Date').resample('M')['Revenue'].sum().reset_index()
    st.plotly_chart(px.line(df_monthly, x='Date', y='Revenue', title="Monthly Revenue Stream", markers=True), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        df['Day'] = df['Date'].dt.day_name()
        st.plotly_chart(px.bar(df.groupby('Day')['Revenue'].sum().reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']).reset_index(), 
                               x='Day', y='Revenue', title="Daily Performance"), use_container_width=True)
    with c2:
        st.plotly_chart(px.histogram(df, x="Payment", title="Payment Method Preference", color_discrete_sequence=['#22C55E']), use_container_width=True)

    st.plotly_chart(px.box(df, x="Channel", y="Revenue", color="Channel", title="Transaction Value by Acquisition Channel"), use_container_width=True)

# --- SECTION 3: CUSTOMER BEHAVIOR ---
elif page == "Customer Behavior":
    st.subheader("👥 CRM & Demographic Intelligence")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.scatter(df, x="Customer_Age", y="Revenue", color="Category", title="Age vs. Spending Profile"), use_container_width=True)
    with c2:
        st.plotly_chart(px.violin(df, y="Rating", x="Category", box=True, title="Sentiment Distribution"), use_container_width=True)

    funnel_data = dict(number=[5000, 2800, 1500, 800], stage=["Leads", "Cart Addition", "Checkout", "Conversion"])
    st.plotly_chart(px.funnel(funnel_data, x='number', y='stage', title="Sales Conversion Funnel (Global)"), use_container_width=True)

# --- SECTION 4: PRODUCT ANALYSIS ---
elif page == "Product Analysis":
    st.subheader("📦 SKU Performance Analysis")
    top_prods = df.groupby('Product')['Revenue'].sum().nlargest(10).reset_index()
    st.plotly_chart(px.bar(top_prods, x='Revenue', y='Product', orientation='h', title="Top 10 High-Revenue SKUs", color='Revenue'), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.density_heatmap(df, x="Price", y="Quantity", title="Price Elasticity Heatmap"), use_container_width=True)
    with c2:
        st.plotly_chart(px.histogram(df, x="Delivery_Days", title="Logistics Lead Time (Days)", nbins=10), use_container_width=True)

# --- SECTION 5: REGIONAL INSIGHTS ---
elif page == "Regional Insights":
    st.subheader("🌍 Geospatial Market Distribution")
    st.plotly_chart(px.sunburst(df, path=['Region', 'Category'], values='Revenue', title="Regional Category Composition"), use_container_width=True)
    
    reg_data = df.groupby('Region').agg({'Revenue':'sum', 'Quantity':'count'}).reset_index()
    st.plotly_chart(px.scatter(reg_data, x="Region", y="Revenue", size="Quantity", color="Revenue", title="Market Saturation vs Revenue"), use_container_width=True)