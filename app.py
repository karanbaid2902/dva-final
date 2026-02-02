"""
TitanForge Industries - Smart Manufacturing & IoT Analytics Dashboard
AI-Powered Predictive Analytics Platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from data_generator import SyntheticDataGenerator
from ml_models import PredictiveMaintenanceModel, AnomalyDetector, EnergyForecaster, QualityPredictor
from utils import format_metric, get_status_color, create_gauge_chart
from ai_chatbot import ManufacturingChatbot

# Page configuration
st.set_page_config(
    page_title="TitanForge Industries - Smart Manufacturing Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional software-like styling
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Professional App Header */
    .app-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 20px 30px;
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 1.5rem -1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: inline-block;
    }
    
    .app-subtitle {
        color: #8892b0;
        font-size: 0.95rem;
        margin-top: 5px;
    }
    
    .header-stats {
        display: flex;
        gap: 30px;
        margin-top: 15px;
    }
    
    .header-stat {
        text-align: center;
    }
    
    .header-stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #64ffda;
    }
    
    .header-stat-label {
        font-size: 0.75rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Navigation Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 8px 15px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        padding: 0 20px;
        font-weight: 600;
        border-radius: 10px;
        color: #8892b0;
        background: transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.2);
        color: #fff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    }
    
    /* Status Indicators */
    .status-online { color: #64ffda; font-weight: bold; }
    .status-warning { color: #ffd93d; font-weight: bold; }
    .status-critical { color: #ff6b6b; font-weight: bold; }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #4a5568;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #fff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 10px 15px;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Select Boxes */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Data Tables */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Charts Container */
    .plot-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Animations */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.6; }
        100% { opacity: 1; }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in {
        animation: slideIn 0.5s ease forwards;
    }
    
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #64ffda;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1.5s infinite;
        box-shadow: 0 0 10px #64ffda;
    }
    
    /* Badges */
    .badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-danger {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        color: #1a1a2e;
    }
    
    .badge-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Cards */
    .info-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        transform: translateY(-3px);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border: none;
        border-radius: 10px;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* Login Page Styles */
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 40px;
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .login-logo {
        font-size: 4rem;
        margin-bottom: 15px;
    }
    
    .login-title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .login-subtitle {
        color: #8892b0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# AUTHENTICATION SYSTEM
# ============================================

# Demo user credentials (in production, use proper authentication)
USERS = {
    "admin": {"password": "admin123", "name": "Administrator", "role": "Admin"},
    "operator": {"password": "op123", "name": "Plant Operator", "role": "Operator"},
    "manager": {"password": "mgr123", "name": "Production Manager", "role": "Manager"},
    "demo": {"password": "demo", "name": "Demo User", "role": "Viewer"}
}

# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def authenticate(username, password):
    """Verify user credentials"""
    if username in USERS and USERS[username]["password"] == password:
        return True, USERS[username]
    return False, None

def logout():
    """Log out the user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_info = None

def show_login_page():
    """Display the login page"""
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 60px 0 30px 0;">
            <div style="font-size: 5rem; margin-bottom: 20px;">🏭</div>
            <h1 style="font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;">TitanForge Industries</h1>
            <p style="color: #8892b0; font-size: 1rem;">Smart Manufacturing & IoT Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); padding: 40px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); margin-top: 20px;">
            <h3 style="color: #fff; text-align: center; margin-bottom: 5px;">Welcome Back</h3>
            <p style="color: #8892b0; text-align: center; margin-bottom: 25px; font-size: 0.9rem;">Sign in to access your dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            st.markdown("<br>", unsafe_allow_html=True)
            
            username = st.text_input(
                "👤 Username",
                placeholder="Enter your username",
                key="login_username"
            )
            
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                submit = st.form_submit_button("🚀 Sign In", use_container_width=True)
            
            if submit:
                if username and password:
                    success, user_info = authenticate(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.user_info = user_info
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 40px; padding: 20px;">
            <p style="color: #555; font-size: 0.8rem;">
                © 2026 TitanForge Industries | Enterprise IoT Platform v2.0
            </p>
        </div>
        """, unsafe_allow_html=True)

# Check if user is authenticated
if not st.session_state.authenticated:
    show_login_page()
    st.stop()

# ============================================
# MAIN DASHBOARD (Only shown when authenticated)
# ============================================

# Initialize session state
if 'data_generator' not in st.session_state:
    st.session_state.data_generator = SyntheticDataGenerator()
if 'pm_model' not in st.session_state:
    st.session_state.pm_model = PredictiveMaintenanceModel()
if 'anomaly_detector' not in st.session_state:
    st.session_state.anomaly_detector = AnomalyDetector()
if 'energy_forecaster' not in st.session_state:
    st.session_state.energy_forecaster = EnergyForecaster()
if 'quality_predictor' not in st.session_state:
    st.session_state.quality_predictor = QualityPredictor()
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = st.session_state.data_generator.generate_historical_data(days=30)
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ManufacturingChatbot()
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# Filter defaults
if 'filter_lines' not in st.session_state:
    st.session_state.filter_lines = ["Line A - Assembly", "Line B - Welding"]
if 'filter_machines' not in st.session_state:
    st.session_state.filter_machines = []
if 'filter_shift' not in st.session_state:
    st.session_state.filter_shift = "All Shifts"
if 'filter_severity' not in st.session_state:
    st.session_state.filter_severity = ["Critical", "Warning", "Info"]

# Professional App Header
current_time_display = datetime.now().strftime('%B %d, %Y | %H:%M:%S')
user_name = st.session_state.user_info["name"] if st.session_state.user_info else "User"
user_role = st.session_state.user_info["role"] if st.session_state.user_info else ""
st.markdown(f'''
<div class="app-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 class="app-title">🏭 TitanForge Industries</h1>
            <p class="app-subtitle">
                <span class="live-indicator"></span>
                Smart Manufacturing & IoT Analytics Platform
            </p>
        </div>
        <div style="text-align: right;">
            <div style="color: #fff; font-size: 1rem; font-weight: 600;">👤 {user_name}</div>
            <div style="color: #64ffda; font-size: 0.8rem;">{user_role}</div>
        </div>
    </div>
    <div style="display: flex; gap: 40px; margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
        <div class="header-stat">
            <div class="header-stat-value">●</div>
            <div class="header-stat-label" style="color: #64ffda;">System Online</div>
        </div>
        <div class="header-stat">
            <div class="header-stat-value">4</div>
            <div class="header-stat-label">AI Models Active</div>
        </div>
        <div class="header-stat">
            <div class="header-stat-value">52</div>
            <div class="header-stat-label">Sensors Connected</div>
        </div>
        <div class="header-stat">
            <div class="header-stat-value">{current_time_display.split(' | ')[1]}</div>
            <div class="header-stat-label">{current_time_display.split(' | ')[0]}</div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Alert Banner (if there are critical alerts)
if len([a for a in st.session_state.get('alerts', []) if a.get('severity') == 'Critical']) > 0:
    st.markdown('''
    <div style="background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%); padding: 12px 20px; border-radius: 10px; margin: 10px 0; display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 1.5rem;">⚠️</span>
        <div>
            <strong style="color: white;">CRITICAL ALERT</strong>
            <span style="color: rgba(255,255,255,0.9);"> — Immediate attention required. Check AI Insights tab for details.</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Function to reset all filters (using callback - runs BEFORE widget instantiation)
def reset_filters():
    st.session_state.filter_lines_widget = ["Line A - Assembly", "Line B - Welding"]
    st.session_state.filter_machines_widget = []
    st.session_state.filter_shift_widget = "All Shifts"
    st.session_state.filter_severity_widget = ["Critical", "Warning", "Info"]
    st.session_state.reset_triggered = True

# Check if reset was triggered
if 'reset_triggered' not in st.session_state:
    st.session_state.reset_triggered = False

# Sidebar
with st.sidebar:
    # User Profile Section
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%); padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid rgba(100,255,218,0.2);">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 45px; height: 45px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">
                👤
            </div>
            <div>
                <div style="color: #fff; font-weight: 600; font-size: 0.95rem;">{st.session_state.user_info["name"]}</div>
                <div style="color: #64ffda; font-size: 0.75rem;">{st.session_state.user_info["role"]}</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Logout button
    if st.button("🚪 Sign Out", use_container_width=True):
        logout()
        st.rerun()
    
    st.markdown("---")
    
    # Logo and branding
    st.markdown('''
    <div style="text-align: center; padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">🏭</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #64ffda;">TitanForge</div>
        <div style="font-size: 0.7rem; color: #8892b0; letter-spacing: 2px;">INDUSTRIES</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Control Center")
    
    # Auto-refresh toggle with better styling
    st.markdown('''
    <div style="background: rgba(100,255,218,0.1); padding: 10px; border-radius: 10px; margin-bottom: 15px;">
        <span style="color: #64ffda; font-weight: 600;">📡 Real-Time Mode</span>
    </div>
    ''', unsafe_allow_html=True)
    auto_refresh = st.toggle("🔄 Live Data Streaming", value=True)
    refresh_rate = st.slider("Refresh Interval", 1, 10, 3, help="Data refresh rate in seconds")
    
    st.markdown("---")
    
    # === FILTERS SECTION ===
    st.markdown("### 🔍 Filters")
    
    # Initialize widget keys if not present
    if "filter_lines_widget" not in st.session_state:
        st.session_state.filter_lines_widget = ["Line A - Assembly", "Line B - Welding"]
    if "filter_machines_widget" not in st.session_state:
        st.session_state.filter_machines_widget = []
    if "filter_shift_widget" not in st.session_state:
        st.session_state.filter_shift_widget = "All Shifts"
    if "filter_severity_widget" not in st.session_state:
        st.session_state.filter_severity_widget = ["Critical", "Warning", "Info"]
    
    # Reset Filters Button (BEFORE widgets, using on_click callback)
    st.button("🔄 Reset All Filters", use_container_width=True, on_click=reset_filters)
    
    # Production line selector
    selected_lines = st.multiselect(
        "🏭 Production Lines",
        ["Line A - Assembly", "Line B - Welding", "Line C - Painting", "Line D - Packaging"],
        key="filter_lines_widget"
    )
    
    # Machine selector
    all_machines = ["CNC Machine #1", "CNC Machine #2", "CNC Machine #3", 
                    "Robot Arm A", "Robot Arm B", "Conveyor System",
                    "Welding Station", "Press Machine", "Packaging Unit"]
    selected_machines = st.multiselect(
        "🔧 Machines",
        all_machines,
        key="filter_machines_widget"
    )
    
    # Shift selector
    shift_options = ["All Shifts", "Morning (6AM-2PM)", "Afternoon (2PM-10PM)", "Night (10PM-6AM)"]
    selected_shift = st.selectbox(
        "⏰ Shift",
        shift_options,
        key="filter_shift_widget"
    )
    
    # Alert severity filter
    selected_severity = st.multiselect(
        "⚠️ Alert Severity",
        ["Critical", "Warning", "Info"],
        key="filter_severity_widget"
    )
    
    st.markdown("---")
    
    # Date range for historical analysis
    st.markdown("### 📅 Analysis Period")
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime.now() - timedelta(days=7), datetime.now()),
        max_value=datetime.now()
    )
    
    st.markdown("---")
    
    # AI Model Settings
    st.markdown("### 🤖 AI Configuration")
    prediction_horizon = st.selectbox(
        "Prediction Horizon",
        ["Next 1 Hour", "Next 4 Hours", "Next 24 Hours", "Next 7 Days"]
    )
    
    sensitivity = st.slider("Anomaly Detection Sensitivity", 0.1, 1.0, 0.7)
    st.session_state.anomaly_detector.set_sensitivity(sensitivity)
    
    st.markdown("---")
    
    # === DATA EXPORT SECTION ===
    st.markdown("### 📥 Data Export")
    
    # Generate exportable data
    export_data = st.session_state.historical_data.copy()
    
    # CSV Download button
    csv_data = export_data.to_csv(index=False)
    st.download_button(
        label="📊 Download Historical Data (CSV)",
        data=csv_data,
        file_name=f"titanforge_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Generate current metrics for export
    current_metrics = pd.DataFrame([{
        'timestamp': datetime.now().isoformat(),
        'oee': np.random.uniform(78, 92),
        'production_rate': np.random.uniform(180, 220),
        'defect_rate': np.random.uniform(0.5, 1.5),
        'energy_consumption': np.random.uniform(1200, 1800),
        'uptime': np.random.uniform(94, 99.5)
    }])
    
    current_csv = current_metrics.to_csv(index=False)
    st.download_button(
        label="📈 Download Current Metrics (CSV)",
        data=current_csv,
        file_name=f"titanforge_current_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("##### 📊 System Status")
    st.markdown('''
    <div style="background: rgba(100,255,218,0.1); border-radius: 10px; padding: 12px; margin-bottom: 10px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #64ffda; font-size: 1.2rem;">●</span>
            <span style="color: #64ffda; font-weight: 600;">All Systems Operational</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.caption(f"🕐 Last sync: {datetime.now().strftime('%H:%M:%S')}")
    
    # Quick Performance Summary
    st.markdown("---")
    st.markdown("##### ⚡ Live Metrics")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(100,255,218,0.1) 0%, rgba(102,126,234,0.1) 100%); padding: 15px; border-radius: 12px; border: 1px solid rgba(100,255,218,0.2);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #8892b0;">OEE</span>
            <span style="color: #64ffda; font-weight: 700;">85.2%</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #8892b0;">Throughput</span>
            <span style="color: #fff; font-weight: 600;">198 u/hr</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #8892b0;">Quality</span>
            <span style="color: #64ffda; font-weight: 700;">99.2%</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #8892b0;">Energy</span>
            <span style="color: #ffd93d; font-weight: 600;">1,542 kWh</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Help section
    st.markdown("---")
    st.markdown("##### ❓ Help")
    with st.expander("📖 User Guide"):
        st.markdown("""
        **Navigation:**
        - Use tabs to switch between different analytics views
        - Real-time data updates automatically
        
        **Filters:**
        - Select production lines, machines, and shifts
        - Use Reset button to clear all filters
        
        **AI Assistant:**
        - Ask questions in natural language
        - Quick actions provide instant insights
        
        **Export:**
        - Download data as CSV files
        - Export chat history for records
        """)

# Generate current data (before status bar)
current_data = st.session_state.data_generator.generate_real_time_data()

# Quick Status Bar - Above tabs
st.markdown("---")
status_col1, status_col2, status_col3, status_col4, status_col5 = st.columns(5)

with status_col1:
    system_health = current_data.get('uptime', 95)
    color = "#64ffda" if system_health > 90 else "#ffd93d" if system_health > 75 else "#ff6b6b"
    st.markdown(f'''
    <div class="kpi-card" style="text-align: center;">
        <div style="color: #8892b0; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">System Health</div>
        <div style="color: {color}; font-size: 1.8rem; font-weight: 800;">{system_health:.1f}%</div>
        <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top: 8px;">
            <div style="width: {system_health}%; height: 100%; background: {color}; border-radius: 2px;"></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with status_col2:
    active_alerts = len([a for a in st.session_state.alerts if a.get('severity') == 'Critical'])
    alert_color = "#ff6b6b" if active_alerts > 0 else "#64ffda"
    st.markdown(f'''
    <div class="kpi-card" style="text-align: center;">
        <div style="color: #8892b0; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Active Alerts</div>
        <div style="color: {alert_color}; font-size: 1.8rem; font-weight: 800;">{active_alerts}</div>
        <div style="color: #8892b0; font-size: 0.75rem; margin-top: 5px;">{"⚠️ Attention needed" if active_alerts > 0 else "✓ All clear"}</div>
    </div>
    ''', unsafe_allow_html=True)

with status_col3:
    machines_online = np.random.randint(8, 10)
    st.markdown(f'''
    <div class="kpi-card" style="text-align: center;">
        <div style="color: #8892b0; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Machines Online</div>
        <div style="color: #64ffda; font-size: 1.8rem; font-weight: 800;">{machines_online}<span style="color: #8892b0; font-size: 1rem;">/10</span></div>
        <div style="display: flex; gap: 3px; justify-content: center; margin-top: 8px;">
            {"".join(['<div style="width: 8px; height: 8px; background: #64ffda; border-radius: 2px;"></div>' for _ in range(machines_online)])}
            {"".join(['<div style="width: 8px; height: 8px; background: rgba(255,255,255,0.1); border-radius: 2px;"></div>' for _ in range(10 - machines_online)])}
        </div>
    </div>
    ''', unsafe_allow_html=True)

with status_col4:
    st.markdown(f'''
    <div class="kpi-card" style="text-align: center;">
        <div style="color: #8892b0; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">AI Engine</div>
        <div style="color: #64ffda; font-size: 1.8rem; font-weight: 800;">✓</div>
        <div style="color: #64ffda; font-size: 0.75rem; margin-top: 5px;">4 Models Active</div>
    </div>
    ''', unsafe_allow_html=True)

with status_col5:
    data_streams = np.random.randint(45, 52)
    st.markdown(f'''
    <div class="kpi-card" style="text-align: center;">
        <div style="color: #8892b0; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Data Streams</div>
        <div style="color: #667eea; font-size: 1.8rem; font-weight: 800;">{data_streams}</div>
        <div style="color: #8892b0; font-size: 0.75rem; margin-top: 5px;"><span class="live-indicator" style="width: 6px; height: 6px;"></span> Live</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Dashboard Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Real-Time Monitoring",
    "🔧 Predictive Maintenance", 
    "⚡ Energy Analytics",
    "✅ Quality Control",
    "📈 Production Analytics",
    "🤖 AI Insights",
    "💬 AI Assistant"
])

# Tab 1: Real-Time Monitoring
with tab1:
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 12px; border-radius: 12px;">
            <span style="font-size: 1.5rem;">📡</span>
        </div>
        <div>
            <h3 style="margin: 0; color: #1a1a2e;">Live Sensor Dashboard</h3>
            <p style="margin: 0; color: #8892b0; font-size: 0.9rem;">Real-time monitoring of all production sensors</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Top KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        oee = current_data['oee']
        st.metric(
            label="🎯 Overall Equipment Effectiveness",
            value=f"{oee:.1f}%",
            delta=f"{np.random.uniform(-2, 3):.1f}%"
        )
    
    with col2:
        production_rate = current_data['production_rate']
        st.metric(
            label="⚙️ Production Rate",
            value=f"{production_rate:.0f} units/hr",
            delta=f"{np.random.randint(-5, 10)} units"
        )
    
    with col3:
        defect_rate = current_data['defect_rate']
        st.metric(
            label="❌ Defect Rate",
            value=f"{defect_rate:.2f}%",
            delta=f"{np.random.uniform(-0.1, 0.05):.2f}%",
            delta_color="inverse"
        )
    
    with col4:
        uptime = current_data['uptime']
        st.metric(
            label="⏱️ Uptime",
            value=f"{uptime:.1f}%",
            delta=f"{np.random.uniform(-0.5, 1):.1f}%"
        )
    
    with col5:
        energy = current_data['energy_consumption']
        st.metric(
            label="⚡ Energy (kWh)",
            value=f"{energy:.0f}",
            delta=f"{np.random.randint(-50, 30)} kWh",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Real-time sensor readings
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌡️ Temperature Sensors")
        
        # Generate temperature data for multiple sensors
        temp_data = current_data['temperatures']
        
        fig_temp = go.Figure()
        for i, (sensor, temp) in enumerate(temp_data.items()):
            color = '#00C851' if temp < 75 else '#ffbb33' if temp < 85 else '#ff4444'
            fig_temp.add_trace(go.Indicator(
                mode="gauge+number+delta",
                value=temp,
                title={'text': sensor, 'font': {'size': 12}},
                number={'font': {'size': 18}},
                delta={'reference': 70, 'relative': False, 'font': {'size': 12}},
                gauge={
                    'axis': {'range': [0, 120], 'tickwidth': 1, 'tickfont': {'size': 10}},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 60], 'color': '#e8f5e9'},
                        {'range': [60, 80], 'color': '#fff3e0'},
                        {'range': [80, 120], 'color': '#ffebee'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 85
                    }
                },
                domain={'row': i // 2, 'column': i % 2}
            ))
        
        fig_temp.update_layout(
            grid={'rows': 2, 'columns': 2, 'pattern': "independent"},
            height=420,
            margin=dict(l=40, r=40, t=50, b=30)
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Vibration Analysis")
        
        # Generate vibration time series
        vib_df = st.session_state.data_generator.generate_vibration_stream(n_points=100)
        
        fig_vib = px.line(vib_df, x='timestamp', y=['sensor_1', 'sensor_2', 'sensor_3'],
                         title="Real-Time Vibration (mm/s)")
        fig_vib.update_layout(
            height=350,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=30, r=30, t=50, b=30)
        )
        
        # Add threshold line
        fig_vib.add_hline(y=7.5, line_dash="dash", line_color="red",
                         annotation_text="Warning Threshold")
        
        st.plotly_chart(fig_vib, use_container_width=True)
    
    # Pressure and Flow Monitoring
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💨 Pressure Monitoring (PSI)")
        pressure_df = st.session_state.data_generator.generate_pressure_data()
        
        fig_pressure = go.Figure()
        for col_name in ['hydraulic', 'pneumatic', 'cooling']:
            fig_pressure.add_trace(go.Scatter(
                x=pressure_df['timestamp'],
                y=pressure_df[col_name],
                mode='lines+markers',
                name=col_name.capitalize(),
                fill='tozeroy',
                opacity=0.7
            ))
        
        fig_pressure.update_layout(height=300, margin=dict(l=30, r=30, t=30, b=30))
        st.plotly_chart(fig_pressure, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔄 Machine Status Overview")
        
        machine_status = current_data['machine_status']
        
        status_df = pd.DataFrame(machine_status)
        
        colors = {'Running': '#00C851', 'Idle': '#ffbb33', 'Maintenance': '#ff4444', 'Standby': '#33b5e5'}
        status_df['color'] = status_df['status'].map(colors)
        
        fig_status = px.bar(status_df, x='machine', y='efficiency', color='status',
                           color_discrete_map=colors,
                           title="Machine Efficiency by Status")
        fig_status.update_layout(height=300, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Alerts Section
    st.markdown("---")
    st.markdown("### ⚠️ Active Alerts & Notifications")
    
    alerts = st.session_state.data_generator.generate_alerts()
    
    if alerts:
        for alert in alerts[:5]:
            if alert['severity'] == 'critical':
                st.error(f"🔴 **CRITICAL** | {alert['timestamp']} | {alert['message']}")
            elif alert['severity'] == 'warning':
                st.warning(f"🟡 **WARNING** | {alert['timestamp']} | {alert['message']}")
            else:
                st.info(f"🔵 **INFO** | {alert['timestamp']} | {alert['message']}")
    else:
        st.success("✅ No active alerts - All systems operating normally")

# Tab 2: Predictive Maintenance
with tab2:
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 12px; border-radius: 12px;">
            <span style="font-size: 1.5rem;">🔧</span>
        </div>
        <div>
            <h3 style="margin: 0; color: #1a1a2e;">AI-Powered Predictive Maintenance</h3>
            <p style="margin: 0; color: #8892b0; font-size: 0.9rem;">Machine learning-driven equipment health monitoring</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Equipment health scores
        st.markdown("#### 🏥 Equipment Health Scores")
        
        equipment_health = st.session_state.pm_model.predict_health_scores(
            st.session_state.historical_data
        )
        
        fig_health = go.Figure()
        
        for eq in equipment_health:
            color = '#00C851' if eq['health_score'] > 80 else '#ffbb33' if eq['health_score'] > 50 else '#ff4444'
            fig_health.add_trace(go.Bar(
                x=[eq['equipment']],
                y=[eq['health_score']],
                name=eq['equipment'],
                marker_color=color,
                text=f"{eq['health_score']:.0f}%",
                textposition='outside'
            ))
        
        fig_health.add_hline(y=80, line_dash="dash", line_color="green", 
                            annotation_text="Healthy Threshold")
        fig_health.add_hline(y=50, line_dash="dash", line_color="red",
                            annotation_text="Critical Threshold")
        
        fig_health.update_layout(
            height=400,
            showlegend=False,
            yaxis_range=[0, 110],
            margin=dict(l=30, r=30, t=30, b=30)
        )
        st.plotly_chart(fig_health, use_container_width=True)
    
    with col2:
        st.markdown("#### ⏰ Maintenance Predictions")
        
        for eq in equipment_health:
            days_until = eq['days_until_maintenance']
            if days_until < 7:
                st.error(f"**{eq['equipment']}**: {days_until} days")
            elif days_until < 14:
                st.warning(f"**{eq['equipment']}**: {days_until} days")
            else:
                st.success(f"**{eq['equipment']}**: {days_until} days")
        
        st.markdown("---")
        st.markdown("#### 💰 Cost Savings")
        st.metric("Predicted Savings", "$127,500", "+15%")
        st.metric("Prevented Downtime", "156 hrs", "+23 hrs")
    
    st.markdown("---")
    
    # Remaining Useful Life (RUL) Prediction
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📉 Remaining Useful Life (RUL) Forecast")
        
        rul_data = st.session_state.pm_model.predict_rul()
        
        fig_rul = go.Figure()
        
        fig_rul.add_trace(go.Scatter(
            x=rul_data['date'],
            y=rul_data['rul_actual'],
            mode='lines',
            name='Actual Health',
            line=dict(color='#667eea', width=2)
        ))
        
        fig_rul.add_trace(go.Scatter(
            x=rul_data['date'],
            y=rul_data['rul_predicted'],
            mode='lines',
            name='AI Prediction',
            line=dict(color='#ff6b6b', width=2, dash='dash')
        ))
        
        fig_rul.add_trace(go.Scatter(
            x=rul_data['date'],
            y=rul_data['confidence_upper'],
            mode='lines',
            name='95% CI Upper',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig_rul.add_trace(go.Scatter(
            x=rul_data['date'],
            y=rul_data['confidence_lower'],
            mode='lines',
            name='95% CI Lower',
            fill='tonexty',
            fillcolor='rgba(255, 107, 107, 0.2)',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig_rul.update_layout(height=400, margin=dict(l=30, r=30, t=30, b=30))
        st.plotly_chart(fig_rul, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔍 Failure Mode Analysis")
        
        failure_modes = st.session_state.pm_model.analyze_failure_modes()
        
        fig_failure = px.treemap(
            failure_modes,
            path=['category', 'failure_mode'],
            values='probability',
            color='severity',
            color_continuous_scale='RdYlGn_r',
            title="Failure Mode Probability Tree"
        )
        fig_failure.update_layout(height=400, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig_failure, use_container_width=True)
    
    # Maintenance Schedule
    st.markdown("---")
    st.markdown("#### 📅 AI-Optimized Maintenance Schedule")
    
    schedule = st.session_state.pm_model.generate_maintenance_schedule()
    
    fig_schedule = px.timeline(
        schedule,
        x_start="start",
        x_end="end",
        y="equipment",
        color="priority",
        color_discrete_map={'High': '#ff4444', 'Medium': '#ffbb33', 'Low': '#00C851'},
        title="Upcoming Maintenance Windows"
    )
    fig_schedule.update_layout(height=350, margin=dict(l=30, r=30, t=50, b=30))
    st.plotly_chart(fig_schedule, use_container_width=True)

# Tab 3: Energy Analytics
with tab3:
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); padding: 12px; border-radius: 12px;">
            <span style="font-size: 1.5rem;">⚡</span>
        </div>
        <div>
            <h3 style="margin: 0; color: #1a1a2e;">Energy Consumption & Optimization</h3>
            <p style="margin: 0; color: #8892b0; font-size: 0.9rem;">Smart energy monitoring with AI-powered forecasting</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Energy KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    energy_data = st.session_state.data_generator.generate_energy_data()
    
    with col1:
        st.metric("Today's Consumption", f"{energy_data['today_kwh']:,.0f} kWh", 
                  f"{energy_data['today_delta']:+.1f}%", delta_color="inverse")
    with col2:
        st.metric("Peak Demand", f"{energy_data['peak_kw']:,.0f} kW",
                  f"{energy_data['peak_delta']:+.1f}%", delta_color="inverse")
    with col3:
        st.metric("Cost Today", f"${energy_data['cost_today']:,.2f}",
                  f"{energy_data['cost_delta']:+.1f}%", delta_color="inverse")
    with col4:
        st.metric("Carbon Footprint", f"{energy_data['carbon_kg']:.0f} kg CO₂",
                  f"{energy_data['carbon_delta']:+.1f}%", delta_color="inverse")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 24-Hour Energy Profile")
        
        hourly_energy = st.session_state.data_generator.generate_hourly_energy()
        
        fig_energy = go.Figure()
        
        fig_energy.add_trace(go.Bar(
            x=hourly_energy['hour'],
            y=hourly_energy['consumption'],
            name='Consumption',
            marker_color='#667eea'
        ))
        
        fig_energy.add_trace(go.Scatter(
            x=hourly_energy['hour'],
            y=hourly_energy['baseline'],
            mode='lines',
            name='Baseline',
            line=dict(color='#ff6b6b', dash='dash')
        ))
        
        fig_energy.update_layout(
            height=350,
            xaxis_title="Hour of Day",
            yaxis_title="Energy (kWh)",
            margin=dict(l=30, r=30, t=30, b=30)
        )
        st.plotly_chart(fig_energy, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏭 Energy by Production Line")
        
        line_energy = st.session_state.data_generator.generate_line_energy()
        
        fig_pie = px.pie(
            line_energy,
            values='consumption',
            names='line',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_layout(height=350, margin=dict(l=30, r=30, t=30, b=30))
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # AI Energy Forecast
    st.markdown("---")
    st.markdown("#### 🤖 AI Energy Consumption Forecast")
    
    forecast = st.session_state.energy_forecaster.predict_energy(days=7)
    
    fig_forecast = go.Figure()
    
    # Historical
    fig_forecast.add_trace(go.Scatter(
        x=forecast['date'][:24],
        y=forecast['actual'][:24],
        mode='lines',
        name='Historical',
        line=dict(color='#667eea', width=2)
    ))
    
    # Forecast
    fig_forecast.add_trace(go.Scatter(
        x=forecast['date'][24:],
        y=forecast['predicted'][24:],
        mode='lines',
        name='AI Forecast',
        line=dict(color='#00C851', width=2, dash='dash')
    ))
    
    # Confidence interval
    fig_forecast.add_trace(go.Scatter(
        x=list(forecast['date'][24:]) + list(forecast['date'][24:][::-1]),
        y=list(forecast['upper'][24:]) + list(forecast['lower'][24:][::-1]),
        fill='toself',
        fillcolor='rgba(0, 200, 81, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='95% Confidence'
    ))
    
    fig_forecast.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="Energy Consumption (kWh)",
        margin=dict(l=30, r=30, t=30, b=30)
    )
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Optimization Recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💡 AI Optimization Recommendations")
        
        recommendations = st.session_state.energy_forecaster.get_recommendations()
        
        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"#{i}: {rec['title']} | Potential Savings: {rec['savings']}"):
                st.write(rec['description'])
                st.progress(rec['confidence'])
                st.caption(f"Confidence: {rec['confidence']*100:.0f}%")
    
    with col2:
        st.markdown("#### 📈 Projected Savings")
        
        savings_data = st.session_state.energy_forecaster.calculate_savings()
        
        fig_savings = go.Figure(go.Waterfall(
            name="Savings Breakdown",
            orientation="v",
            x=savings_data['category'],
            y=savings_data['value'],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#00C851"}},
            decreasing={"marker": {"color": "#ff4444"}},
            totals={"marker": {"color": "#667eea"}}
        ))
        fig_savings.update_layout(height=350, margin=dict(l=30, r=30, t=30, b=30))
        st.plotly_chart(fig_savings, use_container_width=True)

# Tab 4: Quality Control
with tab4:
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 12px; border-radius: 12px;">
            <span style="font-size: 1.5rem;">✅</span>
        </div>
        <div>
            <h3 style="margin: 0; color: #1a1a2e;">AI-Powered Quality Control</h3>
            <p style="margin: 0; color: #8892b0; font-size: 0.9rem;">Intelligent inspection and defect detection system</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Quality KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    quality_data = current_data['quality_metrics']
    
    with col1:
        st.metric("First Pass Yield", f"{quality_data['fpy']:.1f}%", "+0.8%")
    with col2:
        st.metric("Defect Rate", f"{quality_data['defect_rate']:.2f}%", "-0.05%", delta_color="inverse")
    with col3:
        st.metric("Inspection Accuracy", f"{quality_data['inspection_accuracy']:.1f}%", "+1.2%")
    with col4:
        st.metric("Rework Rate", f"{quality_data['rework_rate']:.2f}%", "-0.12%", delta_color="inverse")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Statistical Process Control (SPC)")
        
        spc_data = st.session_state.data_generator.generate_spc_data()
        
        fig_spc = go.Figure()
        
        fig_spc.add_trace(go.Scatter(
            x=spc_data['sample'],
            y=spc_data['measurement'],
            mode='lines+markers',
            name='Measurements',
            line=dict(color='#667eea')
        ))
        
        # Control limits
        fig_spc.add_hline(y=spc_data['ucl'][0], line_dash="dash", line_color="red",
                         annotation_text="UCL")
        fig_spc.add_hline(y=spc_data['lcl'][0], line_dash="dash", line_color="red",
                         annotation_text="LCL")
        fig_spc.add_hline(y=spc_data['center'][0], line_dash="solid", line_color="green",
                         annotation_text="Center Line")
        
        fig_spc.update_layout(
            height=350,
            xaxis_title="Sample Number",
            yaxis_title="Measurement Value",
            margin=dict(l=30, r=30, t=30, b=30)
        )
        st.plotly_chart(fig_spc, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔍 Defect Distribution")
        
        defect_data = st.session_state.data_generator.generate_defect_data()
        
        fig_defect = px.bar(
            defect_data,
            x='defect_type',
            y='count',
            color='severity',
            color_discrete_map={'Critical': '#ff4444', 'Major': '#ffbb33', 'Minor': '#00C851'},
            title="Defects by Type and Severity"
        )
        fig_defect.update_layout(height=350, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_defect, use_container_width=True)
    
    # AI Quality Prediction
    st.markdown("---")
    st.markdown("#### 🤖 AI Quality Prediction Model")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("##### Input Parameters")
        temp_input = st.slider("Temperature (°C)", 20, 100, 65)
        pressure_input = st.slider("Pressure (PSI)", 50, 200, 120)
        speed_input = st.slider("Line Speed (m/min)", 10, 100, 55)
        humidity_input = st.slider("Humidity (%)", 20, 80, 45)
    
    with col2:
        # Get prediction
        prediction = st.session_state.quality_predictor.predict(
            temp_input, pressure_input, speed_input, humidity_input
        )
        
        st.markdown("##### Quality Prediction Results")
        
        # Gauge chart for quality score
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=prediction['quality_score'],
            delta={'reference': 85},
            title={'text': "Predicted Quality Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 50], 'color': "#ffebee"},
                    {'range': [50, 75], 'color': "#fff3e0"},
                    {'range': [75, 100], 'color': "#e8f5e9"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col3:
        st.markdown("##### Prediction Details")
        
        if prediction['quality_score'] >= 90:
            st.success(f"✅ Excellent Quality")
        elif prediction['quality_score'] >= 75:
            st.warning(f"⚠️ Acceptable Quality")
        else:
            st.error(f"❌ Quality Risk")
        
        st.metric("Pass Probability", f"{prediction['pass_probability']:.1f}%")
        st.metric("Defect Risk", f"{prediction['defect_risk']:.1f}%", delta_color="inverse")
        
        st.markdown("**Key Factors:**")
        for factor in prediction['key_factors']:
            st.write(f"• {factor}")

# Tab 5: Production Analytics
with tab5:
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%); padding: 12px; border-radius: 12px;">
            <span style="font-size: 1.5rem;">📈</span>
        </div>
        <div>
            <h3 style="margin: 0; color: #1a1a2e;">Production Performance Analytics</h3>
            <p style="margin: 0; color: #8892b0; font-size: 0.9rem;">Real-time production monitoring and OEE tracking</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Production KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    prod_data = st.session_state.data_generator.generate_production_data()
    
    with col1:
        st.metric("Units Produced", f"{prod_data['units_today']:,}", f"+{prod_data['units_delta']:,}")
    with col2:
        st.metric("Target Achievement", f"{prod_data['target_pct']:.1f}%", f"+{prod_data['target_delta']:.1f}%")
    with col3:
        st.metric("Cycle Time", f"{prod_data['cycle_time']:.1f}s", f"{prod_data['cycle_delta']:.1f}s", delta_color="inverse")
    with col4:
        st.metric("Throughput", f"{prod_data['throughput']:.0f}/hr", f"+{prod_data['throughput_delta']:.0f}")
    with col5:
        st.metric("Scrap Rate", f"{prod_data['scrap_rate']:.2f}%", f"{prod_data['scrap_delta']:.2f}%", delta_color="inverse")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Production Trend (Last 30 Days)")
        
        trend_data = st.session_state.historical_data
        
        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_trend.add_trace(
            go.Bar(x=trend_data['date'], y=trend_data['production'], name='Production',
                   marker_color='#667eea', opacity=0.7),
            secondary_y=False
        )
        
        fig_trend.add_trace(
            go.Scatter(x=trend_data['date'], y=trend_data['efficiency'], name='Efficiency %',
                      mode='lines+markers', line=dict(color='#ff6b6b', width=2)),
            secondary_y=True
        )
        
        fig_trend.update_layout(height=400, margin=dict(l=30, r=30, t=30, b=30))
        fig_trend.update_yaxes(title_text="Units Produced", secondary_y=False)
        fig_trend.update_yaxes(title_text="Efficiency %", secondary_y=True)
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏭 Production by Line")
        
        line_production = st.session_state.data_generator.generate_line_production()
        
        fig_line = px.bar(
            line_production,
            x='line',
            y=['actual', 'target'],
            barmode='group',
            color_discrete_map={'actual': '#667eea', 'target': '#e0e0e0'},
            title="Actual vs Target Production"
        )
        fig_line.update_layout(height=400, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_line, use_container_width=True)
    
    # OEE Breakdown
    st.markdown("---")
    st.markdown("#### 🎯 OEE (Overall Equipment Effectiveness) Breakdown")
    
    col1, col2, col3, col4 = st.columns(4)
    
    oee_data = st.session_state.data_generator.generate_oee_breakdown()
    
    with col1:
        fig_avail = create_gauge_chart(oee_data['availability'], "Availability", "#00C851")
        st.plotly_chart(fig_avail, use_container_width=True)
    
    with col2:
        fig_perf = create_gauge_chart(oee_data['performance'], "Performance", "#ffbb33")
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with col3:
        fig_qual = create_gauge_chart(oee_data['quality'], "Quality", "#667eea")
        st.plotly_chart(fig_qual, use_container_width=True)
    
    with col4:
        fig_oee = create_gauge_chart(oee_data['oee'], "OEE", "#764ba2")
        st.plotly_chart(fig_oee, use_container_width=True)
    
    # Downtime Analysis
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⏱️ Downtime Analysis")
        
        downtime_data = st.session_state.data_generator.generate_downtime_data()
        
        fig_downtime = px.sunburst(
            downtime_data,
            path=['category', 'reason'],
            values='duration',
            color='duration',
            color_continuous_scale='RdYlGn_r'
        )
        fig_downtime.update_layout(height=400, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_downtime, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 Shift Performance Comparison")
        
        shift_data = st.session_state.data_generator.generate_shift_data()
        
        # Create radar chart using graph_objects (Scatterpolar)
        fig_shift = go.Figure()
        
        shifts = shift_data['shift'].unique()
        colors = ['#667eea', '#00C851', '#ffbb33']
        
        for i, shift in enumerate(shifts):
            shift_subset = shift_data[shift_data['shift'] == shift]
            fig_shift.add_trace(go.Scatterpolar(
                r=shift_subset['value'].tolist() + [shift_subset['value'].iloc[0]],
                theta=shift_subset['metric'].tolist() + [shift_subset['metric'].iloc[0]],
                fill='toself',
                name=shift,
                line=dict(color=colors[i % len(colors)])
            ))
        
        fig_shift.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=400, 
            margin=dict(l=30, r=30, t=30, b=30)
        )
        st.plotly_chart(fig_shift, use_container_width=True)

# Tab 6: AI Insights
with tab6:
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%); padding: 12px; border-radius: 12px;">
            <span style="font-size: 1.5rem;">🤖</span>
        </div>
        <div>
            <h3 style="margin: 0; color: #1a1a2e;">AI-Powered Insights & Recommendations</h3>
            <p style="margin: 0; color: #8892b0; font-size: 0.9rem;">Machine learning anomaly detection and optimization</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🧠 Anomaly Detection Results")
        
        # Run anomaly detection
        anomaly_results = st.session_state.anomaly_detector.detect_anomalies(
            st.session_state.historical_data
        )
        
        fig_anomaly = go.Figure()
        
        # Normal points
        normal_data = anomaly_results[anomaly_results['is_anomaly'] == False]
        fig_anomaly.add_trace(go.Scatter(
            x=normal_data['date'],
            y=normal_data['value'],
            mode='markers',
            name='Normal',
            marker=dict(color='#667eea', size=6)
        ))
        
        # Anomaly points
        anomaly_data = anomaly_results[anomaly_results['is_anomaly'] == True]
        fig_anomaly.add_trace(go.Scatter(
            x=anomaly_data['date'],
            y=anomaly_data['value'],
            mode='markers',
            name='Anomaly',
            marker=dict(color='#ff4444', size=12, symbol='x')
        ))
        
        fig_anomaly.update_layout(
            height=400,
            title="Sensor Data with Detected Anomalies",
            margin=dict(l=30, r=30, t=50, b=30)
        )
        st.plotly_chart(fig_anomaly, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Anomaly Statistics")
        
        total_anomalies = len(anomaly_data)
        anomaly_rate = (total_anomalies / len(anomaly_results)) * 100
        
        st.metric("Total Anomalies Detected", total_anomalies)
        st.metric("Anomaly Rate", f"{anomaly_rate:.2f}%")
        st.metric("Model Confidence", f"{np.random.uniform(92, 98):.1f}%")
        
        st.markdown("---")
        st.markdown("**Anomaly Categories:**")
        st.write("• Sensor Drift: 3")
        st.write("• Sudden Spike: 5")
        st.write("• Pattern Deviation: 2")
    
    st.markdown("---")
    
    # Feature Importance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Feature Importance Analysis")
        
        feature_importance = st.session_state.pm_model.get_feature_importance()
        
        fig_importance = px.bar(
            feature_importance,
            x='importance',
            y='feature',
            orientation='h',
            color='importance',
            color_continuous_scale='Viridis'
        )
        fig_importance.update_layout(height=400, margin=dict(l=30, r=30, t=30, b=30))
        st.plotly_chart(fig_importance, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔗 Correlation Matrix")
        
        corr_matrix = st.session_state.data_generator.generate_correlation_matrix()
        
        fig_corr = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        fig_corr.update_layout(height=400, margin=dict(l=30, r=30, t=30, b=30))
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # AI Recommendations
    st.markdown("---")
    st.markdown("#### 💡 AI-Generated Action Items")
    
    recommendations = [
        {
            "priority": "High",
            "title": "Immediate Maintenance Required - CNC Machine #3",
            "description": "Vibration patterns indicate bearing wear. Schedule maintenance within 48 hours to prevent unplanned downtime.",
            "impact": "Prevent $45,000 in potential losses",
            "confidence": 94
        },
        {
            "priority": "Medium",
            "title": "Optimize Energy Usage During Off-Peak Hours",
            "description": "Shift non-critical operations to 22:00-06:00 window for 15% energy cost reduction.",
            "impact": "Save $12,500/month",
            "confidence": 87
        },
        {
            "priority": "Medium",
            "title": "Quality Control Parameter Adjustment",
            "description": "Increase inspection frequency for Line B based on detected quality drift pattern.",
            "impact": "Reduce defect rate by 0.3%",
            "confidence": 82
        },
        {
            "priority": "Low",
            "title": "Process Optimization Opportunity",
            "description": "Machine learning model suggests reducing cycle time by 2.3s on Assembly Line A.",
            "impact": "Increase throughput by 150 units/day",
            "confidence": 79
        }
    ]
    
    for rec in recommendations:
        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[rec["priority"]]
        
        with st.expander(f"{priority_color} [{rec['priority']}] {rec['title']}"):
            st.write(rec['description'])
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"💰 **Impact:** {rec['impact']}")
            with col2:
                st.info(f"🎯 **Confidence:** {rec['confidence']}%")
            
            if st.button(f"Acknowledge & Take Action", key=f"btn_{rec['title'][:10]}"):
                st.success("✅ Action item acknowledged and added to maintenance queue")
    
    # Model Performance
    st.markdown("---")
    st.markdown("#### 📊 AI Model Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("##### Predictive Maintenance")
        st.metric("Accuracy", "94.2%")
        st.metric("Precision", "91.8%")
        st.metric("Recall", "96.3%")
    
    with col2:
        st.markdown("##### Anomaly Detection")
        st.metric("Accuracy", "97.5%")
        st.metric("F1 Score", "0.93")
        st.metric("AUC-ROC", "0.98")
    
    with col3:
        st.markdown("##### Energy Forecasting")
        st.metric("MAPE", "3.2%")
        st.metric("RMSE", "45.6 kWh")
        st.metric("R² Score", "0.94")
    
    with col4:
        st.markdown("##### Quality Prediction")
        st.metric("Accuracy", "92.7%")
        st.metric("Precision", "89.4%")
        st.metric("Recall", "94.1%")

# Tab 7: AI Assistant Chatbot
with tab7:
    st.markdown('''
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 12px; border-radius: 12px;">
            <span style="font-size: 1.5rem;">💬</span>
        </div>
        <div>
            <h3 style="margin: 0; color: #1a1a2e;">TitanForge AI Assistant</h3>
            <p style="margin: 0; color: #8892b0; font-size: 0.9rem;">Your intelligent manufacturing operations copilot</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.info("👋 Ask me anything about your manufacturing operations, equipment status, energy usage, quality metrics, or get optimization recommendations!")
    
    # Chat container with custom styling
    st.markdown("""
    <style>
        .chat-message {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .user-message {
            background-color: #e3f2fd;
            border-left: 4px solid #667eea;
        }
        .assistant-message {
            background-color: #f5f5f5;
            border-left: 4px solid #00C851;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Quick action buttons
    st.markdown("#### 🚀 Quick Actions")
    quick_cols = st.columns(5)
    
    quick_prompts = [
        ("📊 Daily Summary", "Give me today's summary"),
        ("🔧 Maintenance", "What maintenance is needed?"),
        ("⚡ Energy", "How is energy consumption?"),
        ("✅ Quality", "What's the current quality status?"),
        ("💡 Optimize", "How can we improve efficiency?")
    ]
    
    for i, (label, prompt) in enumerate(quick_prompts):
        with quick_cols[i]:
            if st.button(label, key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                response = st.session_state.chatbot.get_response(prompt, current_data)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    st.markdown("---")
    
    # Chat history display with scroll
    st.markdown("#### 💬 Conversation")
    
    if not st.session_state.chat_messages:
        st.info("👋 Hello! I'm your AI manufacturing assistant. Ask me about OEE, energy, quality, production, maintenance, or any operational questions!")
    else:
        # Create scrollable chat container
        chat_html = '<div style="max-height: 400px; overflow-y: auto; padding: 10px; border: 1px solid #ddd; border-radius: 10px; background-color: #fafafa;">'
        for idx, message in enumerate(st.session_state.chat_messages):
            if message["role"] == "user":
                chat_html += f'''
                <div style="background-color: #e3f2fd; padding: 12px 15px; border-radius: 15px; margin: 8px 0; border-left: 4px solid #2196F3;">
                    <strong>👤 You:</strong><br>{message["content"]}
                </div>
                '''
            else:
                chat_html += f'''
                <div style="background-color: #f5f5f5; padding: 12px 15px; border-radius: 15px; margin: 8px 0; border-left: 4px solid #00C851;">
                    <strong>🤖 AI Assistant:</strong><br>
                </div>
                '''
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
        
        # Display assistant content separately for markdown rendering
        for idx, message in enumerate(st.session_state.chat_messages):
            if message["role"] == "assistant":
                with st.expander(f"📝 Response {(idx//2)+1}", expanded=True):
                    st.markdown(message["content"])
    
    st.markdown("---")
    
    # Initialize chat input key
    if 'chat_input_key' not in st.session_state:
        st.session_state.chat_input_key = 0
    
    # Check if clear was requested
    if 'clear_chat_requested' not in st.session_state:
        st.session_state.clear_chat_requested = False
    
    if st.session_state.clear_chat_requested:
        st.session_state.chat_messages = []
        st.session_state.chatbot.clear_history()
        st.session_state.chat_input_key += 1
        st.session_state.clear_chat_requested = False
    
    # Check if send was requested
    if 'send_message_requested' not in st.session_state:
        st.session_state.send_message_requested = False
    
    if st.session_state.send_message_requested:
        user_input = st.session_state.get(f"chat_input_{st.session_state.chat_input_key - 1}", "")
        if user_input.strip():
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            response = st.session_state.chatbot.get_response(user_input, current_data)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.session_state.send_message_requested = False
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your question here...",
            key=f"chat_input_{st.session_state.chat_input_key}",
            placeholder="e.g., What is the current OEE? / Show me energy consumption / Any equipment issues?",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("Send 📤", use_container_width=True):
            if user_input.strip():
                st.session_state.chat_messages.append({"role": "user", "content": user_input})
                response = st.session_state.chatbot.get_response(user_input, current_data)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.session_state.chat_input_key += 1
                st.rerun()
    
    # Clear chat button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.chatbot.clear_history()
            st.session_state.chat_input_key += 1
            st.rerun()
    
    with col2:
        # Export chat history
        if st.session_state.chat_messages:
            chat_export = "\n\n".join([
                f"{'User' if m['role'] == 'user' else 'AI Assistant'}: {m['content']}"
                for m in st.session_state.chat_messages
            ])
            st.download_button(
                "📥 Export Chat",
                chat_export,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    # Sample questions
    with st.expander("💡 Sample Questions You Can Ask"):
        st.markdown("""
        **Production & OEE:**
        - What is the current OEE?
        - Show me today's production summary
        - How is Line B performing?
        
        **Maintenance:**
        - Which machines need maintenance?
        - When is the next scheduled maintenance?
        - Predict equipment failures
        
        **Energy:**
        - How much energy are we consuming?
        - Give me energy optimization tips
        - What's our carbon footprint?
        
        **Quality:**
        - What's the defect rate today?
        - Show quality metrics
        - Any quality issues?
        
        **Alerts & Issues:**
        - Are there any active alerts?
        - Show me anomalies
        - What problems need attention?
        
        **Optimization:**
        - How can we improve efficiency?
        - Give me optimization recommendations
        - What are the quick wins?
        """)

# Professional Footer (only one footer at the bottom)
st.markdown("""
<div style="background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); padding: 30px; border-radius: 15px; margin-top: 30px;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
        <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size: 2rem;">🏭</span>
                <div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #64ffda;">TitanForge Industries</div>
                    <div style="color: #8892b0; font-size: 0.8rem;">Smart Manufacturing Platform</div>
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 30px; color: #8892b0; font-size: 0.85rem;">
            <div>
                <div style="color: #64ffda; font-weight: 600; margin-bottom: 5px;">Platform</div>
                <div>Dashboard v2.0</div>
                <div>AI Engine v1.5</div>
            </div>
            <div>
                <div style="color: #64ffda; font-weight: 600; margin-bottom: 5px;">Features</div>
                <div>Real-Time Analytics</div>
                <div>Predictive AI</div>
            </div>
            <div>
                <div style="color: #64ffda; font-weight: 600; margin-bottom: 5px;">Tech Stack</div>
                <div>Python • Streamlit</div>
                <div>Plotly • scikit-learn</div>
            </div>
        </div>
    </div>
    <div style="border-top: 1px solid rgba(255,255,255,0.1); margin-top: 20px; padding-top: 15px; text-align: center;">
        <p style="color: #555; font-size: 0.75rem; margin: 0;">
            © 2026 TitanForge Industries. All rights reserved. | 
            <span style="color: #667eea;">Enterprise IoT Analytics Solution</span>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

