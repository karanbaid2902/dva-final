"""
Dashboard Builder Module
Allows users to create, customize, and save custom dashboards
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json


class WidgetLibrary:
    """Library of available widgets for dashboard creation"""
    
    WIDGET_TYPES = {
        "metric_card": {
            "name": "Metric Card",
            "icon": "📊",
            "description": "Display a single KPI with delta indicator",
            "category": "KPIs",
            "config_options": ["title", "value_field", "delta_field", "color"]
        },
        "line_chart": {
            "name": "Line Chart",
            "icon": "📈",
            "description": "Time series data visualization",
            "category": "Charts",
            "config_options": ["title", "x_field", "y_field", "color_field"]
        },
        "bar_chart": {
            "name": "Bar Chart",
            "icon": "📊",
            "description": "Categorical data comparison",
            "category": "Charts",
            "config_options": ["title", "x_field", "y_field", "orientation"]
        },
        "pie_chart": {
            "name": "Pie Chart",
            "icon": "🥧",
            "description": "Proportion visualization",
            "category": "Charts",
            "config_options": ["title", "values_field", "names_field"]
        },
        "gauge": {
            "name": "Gauge",
            "icon": "🎯",
            "description": "Progress or level indicator",
            "category": "KPIs",
            "config_options": ["title", "value", "min_val", "max_val", "thresholds"]
        },
        "area_chart": {
            "name": "Area Chart",
            "icon": "📉",
            "description": "Filled line chart for trends",
            "category": "Charts",
            "config_options": ["title", "x_field", "y_field", "fill"]
        },
        "scatter_plot": {
            "name": "Scatter Plot",
            "icon": "⚬",
            "description": "Correlation visualization",
            "category": "Charts",
            "config_options": ["title", "x_field", "y_field", "size_field", "color_field"]
        },
        "data_table": {
            "name": "Data Table",
            "icon": "📋",
            "description": "Tabular data display",
            "category": "Tables",
            "config_options": ["title", "columns", "rows_to_show"]
        },
        "heatmap": {
            "name": "Heatmap",
            "icon": "🗺️",
            "description": "Matrix visualization with color intensity",
            "category": "Charts",
            "config_options": ["title", "x_field", "y_field", "z_field"]
        },
        "text_block": {
            "name": "Text Block",
            "icon": "📝",
            "description": "Custom text or markdown content",
            "category": "Content",
            "config_options": ["title", "content", "style"]
        },
        "progress_bar": {
            "name": "Progress Bar",
            "icon": "▓",
            "description": "Linear progress indicator",
            "category": "KPIs",
            "config_options": ["title", "value", "max_value", "color"]
        },
        "stat_card": {
            "name": "Statistics Card",
            "icon": "📈",
            "description": "Multiple stats in one card",
            "category": "KPIs",
            "config_options": ["title", "stats_list"]
        }
    }
    
    DATA_SOURCES = {
        "production": {
            "name": "Production Data",
            "fields": ["timestamp", "units_produced", "target", "efficiency", "line", "shift"]
        },
        "quality": {
            "name": "Quality Metrics",
            "fields": ["timestamp", "defect_rate", "fpy", "rework_rate", "inspection_score"]
        },
        "energy": {
            "name": "Energy Data",
            "fields": ["timestamp", "consumption_kwh", "cost", "peak_demand", "carbon_footprint"]
        },
        "equipment": {
            "name": "Equipment Status",
            "fields": ["machine_id", "status", "health_score", "temperature", "vibration", "runtime"]
        },
        "maintenance": {
            "name": "Maintenance Data",
            "fields": ["equipment", "last_maintenance", "next_scheduled", "rul", "health_score"]
        },
        "alerts": {
            "name": "Alerts & Events",
            "fields": ["timestamp", "severity", "type", "message", "status"]
        }
    }
    
    @classmethod
    def get_widget_categories(cls):
        categories = {}
        for widget_id, widget_info in cls.WIDGET_TYPES.items():
            cat = widget_info["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((widget_id, widget_info))
        return categories
    
    @classmethod
    def get_widget_info(cls, widget_type):
        return cls.WIDGET_TYPES.get(widget_type, None)


class DashboardConfig:
    """Manages dashboard configurations"""
    
    def __init__(self):
        self.dashboards = {}
        self.current_dashboard = None
    
    @staticmethod
    def get_default_config():
        return {
            "name": "New Dashboard",
            "description": "",
            "theme": "dark",
            "layout": "auto",  # auto, 2-column, 3-column, custom
            "widgets": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def get_widget_config(widget_type, position=0):
        return {
            "id": f"widget_{datetime.now().timestamp()}_{position}",
            "type": widget_type,
            "title": WidgetLibrary.WIDGET_TYPES[widget_type]["name"],
            "data_source": "production",
            "config": {},
            "size": "medium",  # small, medium, large, full
            "position": position
        }


class WidgetRenderer:
    """Renders widgets based on configuration"""
    
    @staticmethod
    def generate_sample_data(data_source, n=100):
        """Generate sample data for preview"""
        np.random.seed(42)
        
        if data_source == "production":
            dates = pd.date_range(end=datetime.now(), periods=n, freq='H')
            return pd.DataFrame({
                'timestamp': dates,
                'units_produced': np.random.randint(150, 250, n),
                'target': [200] * n,
                'efficiency': np.random.uniform(75, 98, n),
                'line': np.random.choice(['Line A', 'Line B', 'Line C', 'Line D'], n),
                'shift': np.random.choice(['Morning', 'Afternoon', 'Night'], n)
            })
        
        elif data_source == "quality":
            dates = pd.date_range(end=datetime.now(), periods=n, freq='H')
            return pd.DataFrame({
                'timestamp': dates,
                'defect_rate': np.random.uniform(0.5, 2.5, n),
                'fpy': np.random.uniform(95, 99.5, n),
                'rework_rate': np.random.uniform(0.2, 1.5, n),
                'inspection_score': np.random.uniform(85, 100, n)
            })
        
        elif data_source == "energy":
            dates = pd.date_range(end=datetime.now(), periods=n, freq='H')
            return pd.DataFrame({
                'timestamp': dates,
                'consumption_kwh': np.random.uniform(1000, 2000, n),
                'cost': np.random.uniform(100, 300, n),
                'peak_demand': np.random.uniform(800, 1500, n),
                'carbon_footprint': np.random.uniform(400, 800, n)
            })
        
        elif data_source == "equipment":
            machines = ['CNC-01', 'CNC-02', 'Robot-A', 'Robot-B', 'Press-01', 'Conveyor-01']
            return pd.DataFrame({
                'machine_id': machines,
                'status': np.random.choice(['Online', 'Maintenance', 'Idle'], len(machines)),
                'health_score': np.random.uniform(70, 100, len(machines)),
                'temperature': np.random.uniform(35, 85, len(machines)),
                'vibration': np.random.uniform(0.1, 2.5, len(machines)),
                'runtime': np.random.randint(100, 5000, len(machines))
            })
        
        elif data_source == "maintenance":
            equipment = ['CNC-01', 'CNC-02', 'Robot-A', 'Robot-B', 'Press-01']
            return pd.DataFrame({
                'equipment': equipment,
                'last_maintenance': pd.date_range(end=datetime.now(), periods=len(equipment), freq='W'),
                'next_scheduled': pd.date_range(start=datetime.now(), periods=len(equipment), freq='W'),
                'rul': np.random.randint(10, 100, len(equipment)),
                'health_score': np.random.uniform(60, 100, len(equipment))
            })
        
        elif data_source == "alerts":
            dates = pd.date_range(end=datetime.now(), periods=20, freq='30min')
            return pd.DataFrame({
                'timestamp': dates,
                'severity': np.random.choice(['Critical', 'Warning', 'Info'], 20),
                'type': np.random.choice(['Temperature', 'Vibration', 'Production', 'Quality'], 20),
                'message': ['Alert message ' + str(i) for i in range(20)],
                'status': np.random.choice(['Active', 'Acknowledged', 'Resolved'], 20)
            })
        
        return pd.DataFrame()
    
    @staticmethod
    def render_metric_card(widget_config, data):
        """Render a metric card widget"""
        config = widget_config.get('config', {})
        value_field = config.get('value_field', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        
        if value_field in data.columns:
            value = data[value_field].iloc[-1] if len(data) > 0 else 0
            delta = np.random.uniform(-5, 10)
            
            if isinstance(value, (int, float)):
                st.metric(
                    label=widget_config.get('title', 'Metric'),
                    value=f"{value:,.1f}",
                    delta=f"{delta:+.1f}%"
                )
            else:
                st.metric(label=widget_config.get('title', 'Metric'), value=str(value))
    
    @staticmethod
    def render_line_chart(widget_config, data):
        """Render a line chart widget"""
        config = widget_config.get('config', {})
        x_field = config.get('x_field', 'timestamp')
        y_field = config.get('y_field', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        
        if x_field in data.columns and y_field in data.columns:
            fig = px.line(data, x=x_field, y=y_field, title=widget_config.get('title', 'Line Chart'))
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_bar_chart(widget_config, data):
        """Render a bar chart widget"""
        config = widget_config.get('config', {})
        x_field = config.get('x_field', data.columns[0])
        y_field = config.get('y_field', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        
        if x_field in data.columns and y_field in data.columns:
            fig = px.bar(data, x=x_field, y=y_field, title=widget_config.get('title', 'Bar Chart'))
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_pie_chart(widget_config, data):
        """Render a pie chart widget"""
        config = widget_config.get('config', {})
        values_field = config.get('values_field', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        names_field = config.get('names_field', data.columns[0])
        
        if values_field in data.columns and names_field in data.columns:
            agg_data = data.groupby(names_field)[values_field].sum().reset_index()
            fig = px.pie(agg_data, values=values_field, names=names_field, title=widget_config.get('title', 'Pie Chart'))
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_gauge(widget_config, data):
        """Render a gauge widget"""
        config = widget_config.get('config', {})
        value = config.get('value', 75)
        min_val = config.get('min_val', 0)
        max_val = config.get('max_val', 100)
        
        # Get value from data if available
        if 'value_field' in config and config['value_field'] in data.columns:
            value = data[config['value_field']].iloc[-1]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': widget_config.get('title', 'Gauge')},
            gauge={
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [min_val, max_val*0.5], 'color': "rgba(255,0,0,0.3)"},
                    {'range': [max_val*0.5, max_val*0.75], 'color': "rgba(255,255,0,0.3)"},
                    {'range': [max_val*0.75, max_val], 'color': "rgba(0,255,0,0.3)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 2},
                    'thickness': 0.75,
                    'value': value
                }
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_area_chart(widget_config, data):
        """Render an area chart widget"""
        config = widget_config.get('config', {})
        x_field = config.get('x_field', 'timestamp')
        y_field = config.get('y_field', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        
        if x_field in data.columns and y_field in data.columns:
            fig = px.area(data, x=x_field, y=y_field, title=widget_config.get('title', 'Area Chart'))
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_scatter_plot(widget_config, data):
        """Render a scatter plot widget"""
        config = widget_config.get('config', {})
        x_field = config.get('x_field', data.columns[0])
        y_field = config.get('y_field', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        
        if x_field in data.columns and y_field in data.columns:
            fig = px.scatter(data, x=x_field, y=y_field, title=widget_config.get('title', 'Scatter Plot'))
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_data_table(widget_config, data):
        """Render a data table widget"""
        config = widget_config.get('config', {})
        rows_to_show = config.get('rows_to_show', 10)
        
        st.markdown(f"**{widget_config.get('title', 'Data Table')}**")
        st.dataframe(data.head(rows_to_show), use_container_width=True)
    
    @staticmethod
    def render_text_block(widget_config, data):
        """Render a text block widget"""
        config = widget_config.get('config', {})
        content = config.get('content', 'Enter your content here...')
        
        st.markdown(f"**{widget_config.get('title', 'Text Block')}**")
        st.markdown(content)
    
    @staticmethod
    def render_progress_bar(widget_config, data):
        """Render a progress bar widget"""
        config = widget_config.get('config', {})
        value = config.get('value', 75)
        max_value = config.get('max_value', 100)
        
        st.markdown(f"**{widget_config.get('title', 'Progress')}**")
        st.progress(min(value / max_value, 1.0))
        st.caption(f"{value} / {max_value}")
    
    @staticmethod
    def render_widget(widget_config):
        """Main method to render any widget type"""
        widget_type = widget_config.get('type')
        data_source = widget_config.get('data_source', 'production')
        
        # Generate sample data
        data = WidgetRenderer.generate_sample_data(data_source)
        
        # Render based on widget type
        renderers = {
            'metric_card': WidgetRenderer.render_metric_card,
            'line_chart': WidgetRenderer.render_line_chart,
            'bar_chart': WidgetRenderer.render_bar_chart,
            'pie_chart': WidgetRenderer.render_pie_chart,
            'gauge': WidgetRenderer.render_gauge,
            'area_chart': WidgetRenderer.render_area_chart,
            'scatter_plot': WidgetRenderer.render_scatter_plot,
            'data_table': WidgetRenderer.render_data_table,
            'text_block': WidgetRenderer.render_text_block,
            'progress_bar': WidgetRenderer.render_progress_bar,
        }
        
        renderer = renderers.get(widget_type)
        if renderer:
            renderer(widget_config, data)
        else:
            st.warning(f"Unknown widget type: {widget_type}")


def render_dashboard_builder():
    """Main dashboard builder interface"""
    
    # Initialize dashboard state
    if 'builder_dashboards' not in st.session_state:
        st.session_state.builder_dashboards = {}
    if 'current_dashboard_id' not in st.session_state:
        st.session_state.current_dashboard_id = None
    if 'builder_widgets' not in st.session_state:
        st.session_state.builder_widgets = []
    if 'builder_mode' not in st.session_state:
        st.session_state.builder_mode = 'builder'  # 'builder' or 'preview'
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0;">🛠️ Dashboard Generator</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">Create, customize, and deploy your own dashboards</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode selector
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("🔨 Builder Mode", use_container_width=True, 
                     type="primary" if st.session_state.builder_mode == 'builder' else "secondary"):
            st.session_state.builder_mode = 'builder'
            st.rerun()
    with col2:
        if st.button("👁️ Preview Mode", use_container_width=True,
                     type="primary" if st.session_state.builder_mode == 'preview' else "secondary"):
            st.session_state.builder_mode = 'preview'
            st.rerun()
    with col3:
        if st.button("💾 Save Dashboard", use_container_width=True):
            if st.session_state.builder_widgets:
                dashboard_name = f"Dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.builder_dashboards[dashboard_name] = {
                    'widgets': st.session_state.builder_widgets.copy(),
                    'created': datetime.now().isoformat()
                }
                st.success(f"Dashboard saved as '{dashboard_name}'!")
    with col4:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.builder_widgets = []
            st.rerun()
    
    st.markdown("---")
    
    if st.session_state.builder_mode == 'builder':
        render_builder_mode()
    else:
        render_preview_mode()


def render_builder_mode():
    """Render the dashboard builder interface"""
    
    col_widgets, col_canvas = st.columns([1, 3])
    
    with col_widgets:
        st.markdown("### 📦 Widget Library")
        
        # Widget categories
        categories = WidgetLibrary.get_widget_categories()
        
        for category, widgets in categories.items():
            with st.expander(f"**{category}**", expanded=True):
                for widget_id, widget_info in widgets:
                    col_icon, col_name, col_add = st.columns([1, 3, 1])
                    with col_icon:
                        st.markdown(f"<span style='font-size: 1.5rem;'>{widget_info['icon']}</span>", unsafe_allow_html=True)
                    with col_name:
                        st.markdown(f"**{widget_info['name']}**")
                        st.caption(widget_info['description'])
                    with col_add:
                        if st.button("➕", key=f"add_{widget_id}"):
                            new_widget = DashboardConfig.get_widget_config(widget_id, len(st.session_state.builder_widgets))
                            st.session_state.builder_widgets.append(new_widget)
                            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Data Sources")
        for ds_id, ds_info in WidgetLibrary.DATA_SOURCES.items():
            with st.expander(ds_info['name']):
                st.caption("Available fields:")
                for field in ds_info['fields']:
                    st.code(field, language=None)
    
    with col_canvas:
        st.markdown("### 🎨 Dashboard Canvas")
        
        if not st.session_state.builder_widgets:
            st.info("👈 Add widgets from the library to start building your dashboard")
        else:
            # Render widget configuration cards
            for idx, widget in enumerate(st.session_state.builder_widgets):
                with st.container():
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid rgba(102,126,234,0.3);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #64ffda; font-weight: 600;">{WidgetLibrary.WIDGET_TYPES[widget['type']]['icon']} {widget['title']}</span>
                            <span style="color: #8892b0; font-size: 0.8rem;">#{idx + 1}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("⚙️ Configure", expanded=False):
                        # Widget title
                        new_title = st.text_input("Widget Title", value=widget['title'], key=f"title_{widget['id']}")
                        if new_title != widget['title']:
                            st.session_state.builder_widgets[idx]['title'] = new_title
                        
                        # Data source
                        ds_options = list(WidgetLibrary.DATA_SOURCES.keys())
                        current_ds = widget.get('data_source', 'production')
                        new_ds = st.selectbox(
                            "Data Source",
                            ds_options,
                            index=ds_options.index(current_ds) if current_ds in ds_options else 0,
                            key=f"ds_{widget['id']}"
                        )
                        if new_ds != current_ds:
                            st.session_state.builder_widgets[idx]['data_source'] = new_ds
                        
                        # Widget size
                        size_options = ['small', 'medium', 'large', 'full']
                        current_size = widget.get('size', 'medium')
                        new_size = st.selectbox(
                            "Widget Size",
                            size_options,
                            index=size_options.index(current_size) if current_size in size_options else 1,
                            key=f"size_{widget['id']}"
                        )
                        if new_size != current_size:
                            st.session_state.builder_widgets[idx]['size'] = new_size
                        
                        # Field configuration based on widget type
                        widget_type = widget['type']
                        ds_fields = WidgetLibrary.DATA_SOURCES[new_ds]['fields']
                        
                        if widget_type in ['line_chart', 'bar_chart', 'area_chart', 'scatter_plot']:
                            x_field = st.selectbox("X-Axis Field", ds_fields, key=f"x_{widget['id']}")
                            y_field = st.selectbox("Y-Axis Field", ds_fields, key=f"y_{widget['id']}")
                            st.session_state.builder_widgets[idx]['config']['x_field'] = x_field
                            st.session_state.builder_widgets[idx]['config']['y_field'] = y_field
                        
                        elif widget_type == 'metric_card':
                            value_field = st.selectbox("Value Field", ds_fields, key=f"val_{widget['id']}")
                            st.session_state.builder_widgets[idx]['config']['value_field'] = value_field
                        
                        elif widget_type == 'pie_chart':
                            names_field = st.selectbox("Names Field", ds_fields, key=f"names_{widget['id']}")
                            values_field = st.selectbox("Values Field", ds_fields, key=f"values_{widget['id']}")
                            st.session_state.builder_widgets[idx]['config']['names_field'] = names_field
                            st.session_state.builder_widgets[idx]['config']['values_field'] = values_field
                        
                        elif widget_type == 'gauge':
                            min_val = st.number_input("Min Value", value=0, key=f"min_{widget['id']}")
                            max_val = st.number_input("Max Value", value=100, key=f"max_{widget['id']}")
                            current_val = st.slider("Current Value", min_val, max_val, 75, key=f"curr_{widget['id']}")
                            st.session_state.builder_widgets[idx]['config']['min_val'] = min_val
                            st.session_state.builder_widgets[idx]['config']['max_val'] = max_val
                            st.session_state.builder_widgets[idx]['config']['value'] = current_val
                        
                        elif widget_type == 'text_block':
                            content = st.text_area("Content (Markdown supported)", key=f"content_{widget['id']}")
                            st.session_state.builder_widgets[idx]['config']['content'] = content
                        
                        elif widget_type == 'data_table':
                            rows = st.number_input("Rows to display", min_value=5, max_value=50, value=10, key=f"rows_{widget['id']}")
                            st.session_state.builder_widgets[idx]['config']['rows_to_show'] = rows
                        
                        # Delete button
                        if st.button("🗑️ Remove Widget", key=f"del_{widget['id']}"):
                            st.session_state.builder_widgets.pop(idx)
                            st.rerun()


def render_preview_mode():
    """Render the dashboard preview"""
    
    if not st.session_state.builder_widgets:
        st.info("No widgets added yet. Switch to Builder Mode to add widgets.")
        return
    
    st.markdown("### 📊 Dashboard Preview")
    
    # Group widgets by size for layout
    widgets = st.session_state.builder_widgets
    
    # Create responsive layout
    i = 0
    while i < len(widgets):
        widget = widgets[i]
        size = widget.get('size', 'medium')
        
        if size == 'full':
            with st.container():
                WidgetRenderer.render_widget(widget)
            i += 1
        elif size == 'large':
            col1, col2 = st.columns([2, 1])
            with col1:
                WidgetRenderer.render_widget(widget)
            i += 1
            if i < len(widgets) and widgets[i].get('size') == 'small':
                with col2:
                    WidgetRenderer.render_widget(widgets[i])
                i += 1
        elif size == 'medium':
            cols = st.columns(2)
            with cols[0]:
                WidgetRenderer.render_widget(widget)
            i += 1
            if i < len(widgets) and widgets[i].get('size') in ['medium', 'small']:
                with cols[1]:
                    WidgetRenderer.render_widget(widgets[i])
                i += 1
        else:  # small
            cols = st.columns(3)
            with cols[0]:
                WidgetRenderer.render_widget(widget)
            i += 1
            for j in range(1, 3):
                if i < len(widgets) and widgets[i].get('size') == 'small':
                    with cols[j]:
                        WidgetRenderer.render_widget(widgets[i])
                    i += 1


def render_saved_dashboards():
    """Display saved dashboards"""
    
    st.markdown("### 💾 Saved Dashboards")
    
    if not st.session_state.get('builder_dashboards'):
        st.info("No saved dashboards yet. Create and save a dashboard to see it here.")
        return
    
    for name, dashboard in st.session_state.builder_dashboards.items():
        with st.expander(f"📊 {name}"):
            st.caption(f"Created: {dashboard['created']}")
            st.caption(f"Widgets: {len(dashboard['widgets'])}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📂 Load", key=f"load_{name}"):
                    st.session_state.builder_widgets = dashboard['widgets'].copy()
                    st.session_state.builder_mode = 'preview'
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{name}"):
                    del st.session_state.builder_dashboards[name]
                    st.rerun()
