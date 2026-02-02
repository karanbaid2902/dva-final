"""
Synthetic Data Generator for Smart Manufacturing Dashboard
Generates realistic IoT sensor data, production metrics, and events
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


class SyntheticDataGenerator:
    """Generate realistic synthetic manufacturing data"""
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        
        self.machine_names = [
            "CNC Machine #1", "CNC Machine #2", "CNC Machine #3",
            "Robot Arm A", "Robot Arm B", "Conveyor System",
            "Welding Station", "Press Machine", "Packaging Unit"
        ]
        
        self.production_lines = [
            "Line A - Assembly", "Line B - Welding",
            "Line C - Painting", "Line D - Packaging"
        ]
    
    def generate_real_time_data(self):
        """Generate current real-time sensor readings"""
        
        # Temperatures for multiple sensors
        temperatures = {
            "Motor 1": np.random.normal(68, 5),
            "Motor 2": np.random.normal(72, 6),
            "Hydraulic": np.random.normal(55, 4),
            "Ambient": np.random.normal(25, 2)
        }
        
        # Machine status
        machine_status = []
        statuses = ['Running', 'Running', 'Running', 'Idle', 'Maintenance', 'Standby']
        
        for machine in self.machine_names:
            status = random.choice(statuses)
            efficiency = np.random.uniform(75, 98) if status == 'Running' else np.random.uniform(0, 30)
            machine_status.append({
                'machine': machine,
                'status': status,
                'efficiency': efficiency
            })
        
        # Quality metrics
        quality_metrics = {
            'fpy': np.random.uniform(95, 99.5),
            'defect_rate': np.random.uniform(0.1, 0.8),
            'inspection_accuracy': np.random.uniform(97, 99.8),
            'rework_rate': np.random.uniform(0.5, 2.0)
        }
        
        return {
            'oee': np.random.uniform(78, 92),
            'production_rate': np.random.uniform(180, 220),
            'defect_rate': np.random.uniform(0.5, 1.5),
            'uptime': np.random.uniform(94, 99.5),
            'energy_consumption': np.random.uniform(1200, 1800),
            'temperatures': temperatures,
            'machine_status': machine_status,
            'quality_metrics': quality_metrics
        }
    
    def generate_historical_data(self, days=30):
        """Generate historical production data"""
        
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Create realistic production patterns with weekly seasonality
        base_production = 5000
        weekly_pattern = [1.0, 1.05, 1.1, 1.08, 1.02, 0.7, 0.5]  # Mon-Sun
        
        production = []
        efficiency = []
        
        for i, date in enumerate(dates):
            day_of_week = date.dayofweek
            seasonal_factor = weekly_pattern[day_of_week]
            trend = 1 + (i * 0.002)  # Slight upward trend
            noise = np.random.normal(1, 0.05)
            
            prod = base_production * seasonal_factor * trend * noise
            eff = np.random.normal(85, 5) * seasonal_factor
            
            production.append(prod)
            efficiency.append(min(eff, 99))
        
        return pd.DataFrame({
            'date': dates,
            'production': production,
            'efficiency': efficiency,
            'defects': [p * np.random.uniform(0.005, 0.015) for p in production],
            'energy': [p * np.random.uniform(0.35, 0.45) for p in production]
        })
    
    def generate_vibration_stream(self, n_points=100):
        """Generate real-time vibration sensor data"""
        
        now = datetime.now()
        timestamps = [now - timedelta(seconds=i) for i in range(n_points, 0, -1)]
        
        # Generate correlated sensor readings
        base_signal = np.sin(np.linspace(0, 4*np.pi, n_points)) * 2
        
        sensor_1 = base_signal + np.random.normal(3.5, 0.5, n_points)
        sensor_2 = base_signal + np.random.normal(4.0, 0.6, n_points) + 0.5
        sensor_3 = base_signal + np.random.normal(3.8, 0.4, n_points) - 0.3
        
        # Add occasional spikes (anomalies)
        for _ in range(3):
            idx = random.randint(0, n_points-1)
            sensor_1[idx] += random.uniform(3, 5)
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'sensor_1': sensor_1,
            'sensor_2': sensor_2,
            'sensor_3': sensor_3
        })
    
    def generate_pressure_data(self, n_points=50):
        """Generate pressure sensor readings"""
        
        now = datetime.now()
        timestamps = [now - timedelta(minutes=i) for i in range(n_points, 0, -1)]
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'hydraulic': np.random.normal(120, 8, n_points),
            'pneumatic': np.random.normal(85, 5, n_points),
            'cooling': np.random.normal(45, 3, n_points)
        })
    
    def generate_alerts(self, n_alerts=8):
        """Generate random alerts"""
        
        alert_templates = [
            {"severity": "critical", "message": "Temperature threshold exceeded on CNC Machine #3"},
            {"severity": "critical", "message": "Vibration anomaly detected on Robot Arm A"},
            {"severity": "warning", "message": "Hydraulic pressure dropping on Press Machine"},
            {"severity": "warning", "message": "Energy consumption above baseline on Line B"},
            {"severity": "warning", "message": "Cycle time deviation detected on Assembly Line"},
            {"severity": "info", "message": "Scheduled maintenance reminder for Conveyor System"},
            {"severity": "info", "message": "Quality inspection completed for Batch #4521"},
            {"severity": "info", "message": "Shift change completed - Line A now operating at full capacity"}
        ]
        
        selected_alerts = random.sample(alert_templates, min(n_alerts, len(alert_templates)))
        
        now = datetime.now()
        for i, alert in enumerate(selected_alerts):
            alert['timestamp'] = (now - timedelta(minutes=random.randint(1, 60))).strftime('%H:%M:%S')
        
        return selected_alerts
    
    def generate_energy_data(self):
        """Generate energy consumption metrics"""
        
        return {
            'today_kwh': np.random.uniform(15000, 18000),
            'today_delta': np.random.uniform(-8, 5),
            'peak_kw': np.random.uniform(800, 1200),
            'peak_delta': np.random.uniform(-5, 10),
            'cost_today': np.random.uniform(1800, 2500),
            'cost_delta': np.random.uniform(-10, 8),
            'carbon_kg': np.random.uniform(8000, 12000),
            'carbon_delta': np.random.uniform(-5, 5)
        }
    
    def generate_hourly_energy(self):
        """Generate 24-hour energy profile"""
        
        hours = list(range(24))
        
        # Realistic hourly pattern
        base_pattern = [
            0.3, 0.25, 0.2, 0.2, 0.25, 0.4,  # 00-05
            0.6, 0.85, 1.0, 1.0, 0.95, 0.9,   # 06-11
            0.85, 1.0, 1.0, 0.95, 0.9, 0.85,  # 12-17
            0.7, 0.6, 0.5, 0.45, 0.4, 0.35    # 18-23
        ]
        
        consumption = [p * np.random.uniform(800, 900) for p in base_pattern]
        baseline = [700 * p for p in base_pattern]
        
        return pd.DataFrame({
            'hour': hours,
            'consumption': consumption,
            'baseline': baseline
        })
    
    def generate_line_energy(self):
        """Generate energy by production line"""
        
        return pd.DataFrame({
            'line': self.production_lines,
            'consumption': [
                np.random.uniform(4000, 5000),
                np.random.uniform(3500, 4500),
                np.random.uniform(2500, 3500),
                np.random.uniform(2000, 3000)
            ]
        })
    
    def generate_spc_data(self, n_samples=50):
        """Generate Statistical Process Control data"""
        
        # Target value and control limits
        target = 50.0
        ucl = 52.5
        lcl = 47.5
        
        # Generate measurements with occasional out-of-control points
        measurements = np.random.normal(target, 1.2, n_samples)
        
        # Add a few out-of-control points
        for _ in range(3):
            idx = random.randint(0, n_samples-1)
            measurements[idx] += random.choice([-1, 1]) * random.uniform(2.5, 4)
        
        return pd.DataFrame({
            'sample': list(range(1, n_samples + 1)),
            'measurement': measurements,
            'ucl': [ucl] * n_samples,
            'lcl': [lcl] * n_samples,
            'center': [target] * n_samples
        })
    
    def generate_defect_data(self):
        """Generate defect distribution data"""
        
        defect_types = ['Scratch', 'Dent', 'Misalignment', 'Color Variation', 
                        'Dimension Error', 'Surface Roughness', 'Weld Defect']
        severities = ['Critical', 'Major', 'Minor']
        
        data = []
        for defect in defect_types:
            for severity in severities:
                count = np.random.randint(1, 20)
                if severity == 'Critical':
                    count = count // 3
                elif severity == 'Minor':
                    count = count * 2
                data.append({
                    'defect_type': defect,
                    'severity': severity,
                    'count': count
                })
        
        return pd.DataFrame(data)
    
    def generate_production_data(self):
        """Generate production metrics"""
        
        return {
            'units_today': int(np.random.uniform(4500, 5500)),
            'units_delta': int(np.random.uniform(50, 200)),
            'target_pct': np.random.uniform(92, 105),
            'target_delta': np.random.uniform(-2, 5),
            'cycle_time': np.random.uniform(12, 16),
            'cycle_delta': np.random.uniform(-0.5, 0.3),
            'throughput': np.random.uniform(200, 250),
            'throughput_delta': np.random.uniform(5, 15),
            'scrap_rate': np.random.uniform(0.5, 1.5),
            'scrap_delta': np.random.uniform(-0.2, 0.1)
        }
    
    def generate_line_production(self):
        """Generate production by line"""
        
        return pd.DataFrame({
            'line': self.production_lines,
            'actual': [
                np.random.uniform(1200, 1400),
                np.random.uniform(1100, 1300),
                np.random.uniform(900, 1100),
                np.random.uniform(1000, 1200)
            ],
            'target': [1350, 1250, 1050, 1150]
        })
    
    def generate_oee_breakdown(self):
        """Generate OEE component breakdown"""
        
        availability = np.random.uniform(88, 96)
        performance = np.random.uniform(85, 95)
        quality = np.random.uniform(95, 99.5)
        oee = (availability * performance * quality) / 10000
        
        return {
            'availability': availability,
            'performance': performance,
            'quality': quality,
            'oee': oee
        }
    
    def generate_downtime_data(self):
        """Generate downtime analysis data"""
        
        data = [
            {'category': 'Planned', 'reason': 'Scheduled Maintenance', 'duration': np.random.uniform(60, 120)},
            {'category': 'Planned', 'reason': 'Changeover', 'duration': np.random.uniform(30, 60)},
            {'category': 'Planned', 'reason': 'Breaks', 'duration': np.random.uniform(45, 60)},
            {'category': 'Unplanned', 'reason': 'Equipment Failure', 'duration': np.random.uniform(20, 80)},
            {'category': 'Unplanned', 'reason': 'Material Shortage', 'duration': np.random.uniform(10, 40)},
            {'category': 'Unplanned', 'reason': 'Quality Issue', 'duration': np.random.uniform(15, 35)},
            {'category': 'Unplanned', 'reason': 'Operator Error', 'duration': np.random.uniform(5, 20)},
        ]
        
        return pd.DataFrame(data)
    
    def generate_shift_data(self):
        """Generate shift performance comparison"""
        
        metrics = ['Productivity', 'Quality', 'Efficiency', 'Safety', 'Delivery']
        shifts = ['Morning', 'Afternoon', 'Night']
        
        data = []
        for shift in shifts:
            for metric in metrics:
                base = 85 if shift != 'Night' else 80
                value = np.random.uniform(base - 5, base + 10)
                data.append({
                    'shift': shift,
                    'metric': metric,
                    'value': value
                })
        
        return pd.DataFrame(data)
    
    def generate_correlation_matrix(self):
        """Generate correlation matrix for sensor data"""
        
        variables = ['Temperature', 'Pressure', 'Vibration', 'Speed', 
                     'Power', 'Humidity', 'Flow Rate']
        
        n = len(variables)
        
        # Generate a valid correlation matrix
        A = np.random.randn(n, n)
        corr = np.corrcoef(A)
        
        # Make diagonal exactly 1
        np.fill_diagonal(corr, 1.0)
        
        return pd.DataFrame(corr, columns=variables, index=variables)
