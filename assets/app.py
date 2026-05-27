import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="ShopMax Returns Analytics",
    page_icon="🛍️",
    layout="wide"
)

st_autorefresh(interval=10000, key="autorefresh")
st.cache_data.clear()
# ─────────────────────────────────────────
# Connect to MySQL
# ─────────────────────────────────────────
@st.cache_data(ttl=10)
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",  # your MySQL password
        database="shopmax_v2"
    )
    df          = pd.read_sql("SELECT * FROM vw_returns_analysis", conn)
    df_monthly  = pd.read_sql("SELECT * FROM vw_monthly_loss_trend", conn)
    df_seller   = pd.read_sql("SELECT * FROM vw_seller_scorecard", conn)
    df_category = pd.read_sql("SELECT * FROM vw_refund_rate_by_category", conn)
    df_fraud    = pd.read_sql("SELECT * FROM vw_fraud_customers", conn)
    conn.close()
    return df, df_monthly, df_seller, df_category, df_fraud

df, df_monthly, df_seller, df_category, df_fraud = load_data()

# ─────────────────────────────────────────
# Header
# ─────────────────────────────────────────
st.title("🛍️ ShopMax — Returns & Refund Loss Recovery")
st.markdown("**Real-time Refund Analytics Dashboard | Operations Team**")
st.divider()

# ─────────────────────────────────────────
# Sidebar Filters
# ─────────────────────────────────────────
st.sidebar.header("🔍 Filters")
regions   = ["All"] + sorted(df['region'].unique().tolist())
sellers   = ["All"] + sorted(df['seller_name'].unique().tolist())
reasons   = ["All"] + sorted(df['return_reason'].unique().tolist())
statuses  = ["All"] + sorted(df['refund_status'].unique().tolist())

sel_region  = st.sidebar.selectbox("Region",        regions)
sel_seller  = st.sidebar.selectbox("Seller",        sellers)
sel_reason  = st.sidebar.selectbox("Return Reason", reasons)
sel_status  = st.sidebar.selectbox("Refund Status", statuses)

# Apply filters
filtered = df.copy()
if sel_region != "All":
    filtered = filtered[filtered['region'] == sel_region]
if sel_seller != "All":
    filtered = filtered[filtered['seller_name'] == sel_seller]
if sel_reason != "All":
    filtered = filtered[filtered['return_reason'] == sel_reason]
if sel_status != "All":
    filtered = filtered[filtered['refund_status'] == sel_status]

# ─────────────────────────────────────────
# KPI Cards
# ─────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Total Refund Loss",
          f"₹{filtered['refund_amount'].sum():,.0f}")
k2.metric("📦 Total Returns",
          f"{len(filtered):,}")
k3.metric("⏳ Pending Refunds",
          f"{len(filtered[filtered['refund_status']=='Pending']):,}")
k4.metric("🚨 Fraud Flags",
          f"{filtered['fraud_flag'].sum():,}")
k5.metric("⭐ Avg Rating",
          f"{filtered['customer_rating'].mean():.1f} / 5")

st.divider()

# ─────────────────────────────────────────
# Row 1: Monthly Trend + Return Reasons
# ─────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Refund Loss Trend")
    df_monthly['period'] = df_monthly['month_name'] + " " + df_monthly['return_year'].astype(str)
    fig = px.line(df_monthly, x='period', y='total_refund_loss',
                  markers=True, color_discrete_sequence=['crimson'])
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🥧 Returns by Reason")
    reason_counts = filtered['return_reason'].value_counts().reset_index()
    reason_counts.columns = ['return_reason', 'count']
    fig = px.pie(reason_counts, names='return_reason', values='count',
                 color_discrete_sequence=px.colors.sequential.Reds_r)
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────
# Row 2: Refund by Region + Seller Scorecard
# ─────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("🗺️ Refund Loss by Region")
    region_data = filtered.groupby('region')['refund_amount'].sum().reset_index()
    fig = px.bar(region_data, x='refund_amount', y='region',
                 orientation='h', color='refund_amount',
                 color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("🏪 Seller Risk Scorecard")
    fig = px.bar(df_seller, x='seller_name', y='return_rate_pct',
                 color='seller_risk_tier',
                 color_discrete_map={
                     'Critical':'crimson',
                     'Watch':'orange',
                     'Healthy':'green'
                 })
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────
# Row 3: Category Analysis + Delay vs Refund
# ─────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader("📦 Refund Rate by Category")
    fig = px.bar(df_category, x='refund_rate_pct', y='product_category',
                 orientation='h', color='refund_rate_pct',
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("🚚 Shipping Delay vs Avg Refund")
    delay_data = filtered.groupby('shipping_delay_days')['refund_amount'].mean().reset_index()
    fig = px.scatter(delay_data, x='shipping_delay_days', y='refund_amount',
                     size='refund_amount', color='refund_amount',
                     color_continuous_scale='Oranges')
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────
# Row 4: Fraud Analysis
# ─────────────────────────────────────────
st.subheader("🚨 Fraud Detection — High Risk Customers")
fraud_display = df_fraud[df_fraud['fraud_risk_level'] == 'High Risk'][
    ['customer_name','city','total_returns',
     'fraud_count','total_refund_claimed','payment_method','fraud_risk_level']
].head(20)
st.dataframe(fraud_display, use_container_width=True)

# ─────────────────────────────────────────
# Row 5: Raw Data Table
# ─────────────────────────────────────────
st.divider()
st.subheader("📋 Filtered Returns Data")
display_df = filtered[['return_date','customer_name','city','product_name',
              'product_category','seller_name','return_reason',
              'refund_amount','refund_status','fraud_flag',
              'customer_rating','region','shipping_delay_days'
              ]].sort_values('refund_amount', ascending=False).reset_index(drop=True)
display_df.index += 1  # start from 1 instead of 0
st.dataframe(display_df, use_container_width=True)

st.caption("ShopMax Returns Analytics | Built with MySQL + Python + Streamlit")