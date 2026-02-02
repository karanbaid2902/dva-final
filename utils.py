"""
Utility functions for Smart Manufacturing Dashboard
"""

import plotly.graph_objects as go
import numpy as np


def format_metric(value, suffix='', prefix='', decimals=1):
    """Format a metric value with prefix/suffix"""
    if isinstance(value, (int, float)):
        if decimals == 0:
            formatted = f"{prefix}{int(value):,}{suffix}"
        else:
            formatted = f"{prefix}{value:,.{decimals}f}{suffix}"
    else:
        formatted = str(value)
    return formatted


def get_status_color(value, thresholds):
    """
    Get color based on value and thresholds
    thresholds = {'good': 80, 'warning': 50}
    """
    if value >= thresholds.get('good', 80):
        return '#00C851'  # Green
    elif value >= thresholds.get('warning', 50):
        return '#ffbb33'  # Yellow
    else:
        return '#ff4444'  # Red


def create_gauge_chart(value, title, color):
    """Create a gauge chart for OEE components"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 16}},
        number={'suffix': '%', 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e0e0e0",
            'steps': [
                {'range': [0, 50], 'color': '#ffebee'},
                {'range': [50, 75], 'color': '#fff3e0'},
                {'range': [75, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    
    fig.update_layout(
        height=180,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#333"}
    )
    
    return fig


def create_sparkline(data, color='#667eea'):
    """Create a simple sparkline chart"""
    
    fig = go.Figure(go.Scatter(
        y=data,
        mode='lines',
        fill='tozeroy',
        line=dict(color=color, width=1),
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2)'
    ))
    
    fig.update_layout(
        height=50,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def calculate_trend(current, previous):
    """Calculate percentage change between current and previous values"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100


def format_duration(minutes):
    """Format duration in minutes to human-readable string"""
    if minutes < 60:
        return f"{int(minutes)}m"
    elif minutes < 1440:
        hours = minutes // 60
        mins = minutes % 60
        return f"{int(hours)}h {int(mins)}m"
    else:
        days = minutes // 1440
        hours = (minutes % 1440) // 60
        return f"{int(days)}d {int(hours)}h"


def severity_to_color(severity):
    """Convert severity level to color"""
    colors = {
        'critical': '#ff4444',
        'high': '#ff8800',
        'medium': '#ffbb33',
        'low': '#00C851',
        'info': '#33b5e5'
    }
    return colors.get(severity.lower(), '#999999')


def generate_random_walk(n_points, start_value=100, volatility=0.02):
    """Generate a random walk time series"""
    returns = np.random.normal(0, volatility, n_points)
    walk = start_value * np.cumprod(1 + returns)
    return walk


def moving_average(data, window=5):
    """Calculate moving average"""
    return np.convolve(data, np.ones(window)/window, mode='valid')


def detect_outliers_iqr(data, k=1.5):
    """Detect outliers using IQR method"""
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    
    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr
    
    outliers = (data < lower_bound) | (data > upper_bound)
    return outliers


def normalize_data(data, min_val=0, max_val=100):
    """Normalize data to a specified range"""
    data_min = np.min(data)
    data_max = np.max(data)
    
    if data_max - data_min == 0:
        return np.full_like(data, (min_val + max_val) / 2)
    
    normalized = (data - data_min) / (data_max - data_min)
    scaled = normalized * (max_val - min_val) + min_val
    
    return scaled
