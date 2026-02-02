"""
Machine Learning Models for Smart Manufacturing Dashboard
Includes Predictive Maintenance, Anomaly Detection, Energy Forecasting, and Quality Prediction
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest, RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class PredictiveMaintenanceModel:
    """AI model for predicting equipment maintenance needs"""
    
    def __init__(self):
        self.equipment_list = [
            "CNC Machine #1", "CNC Machine #2", "CNC Machine #3",
            "Robot Arm A", "Robot Arm B", "Conveyor System",
            "Welding Station", "Press Machine", "Packaging Unit"
        ]
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_model()
    
    def _train_model(self):
        """Train the predictive maintenance model with synthetic data"""
        # Generate synthetic training data
        n_samples = 1000
        
        X = np.column_stack([
            np.random.normal(70, 15, n_samples),    # Temperature
            np.random.normal(5, 2, n_samples),       # Vibration
            np.random.normal(100, 20, n_samples),    # Pressure
            np.random.uniform(0, 5000, n_samples),   # Operating hours
            np.random.uniform(0, 100, n_samples),    # Age (days since maintenance)
        ])
        
        # Create target: 1 = needs maintenance soon
        y = ((X[:, 0] > 80) | (X[:, 1] > 7) | (X[:, 4] > 60)).astype(int)
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
    
    def predict_health_scores(self, historical_data):
        """Predict health scores for each piece of equipment"""
        
        health_scores = []
        
        for equipment in self.equipment_list:
            # Simulate feature extraction from historical data
            features = np.array([[
                np.random.normal(68, 10),      # Temperature
                np.random.normal(4.5, 1.5),    # Vibration
                np.random.normal(105, 15),     # Pressure
                np.random.uniform(100, 3000),  # Operating hours
                np.random.uniform(5, 90),      # Days since maintenance
            ]])
            
            features_scaled = self.scaler.transform(features)
            
            # Get probability of needing maintenance
            maintenance_prob = self.model.predict_proba(features_scaled)[0][1]
            
            # Convert to health score (inverse of maintenance probability)
            health_score = (1 - maintenance_prob) * 100
            
            # Calculate days until maintenance
            days_until = int((health_score / 100) * 45)
            
            health_scores.append({
                'equipment': equipment,
                'health_score': health_score,
                'days_until_maintenance': max(1, days_until),
                'maintenance_probability': maintenance_prob * 100
            })
        
        return health_scores
    
    def predict_rul(self, days=60):
        """Predict Remaining Useful Life over time"""
        
        dates = pd.date_range(start=datetime.now() - timedelta(days=30),
                             end=datetime.now() + timedelta(days=30), freq='D')
        
        # Generate RUL curve with degradation
        n = len(dates)
        half_n = n // 2
        
        # Actual (historical) part - random walk with slight degradation
        actual_start = 100
        actual = [actual_start]
        for i in range(1, half_n):
            change = np.random.normal(-0.3, 0.5)
            actual.append(max(10, min(100, actual[-1] + change)))
        
        # Pad actual to full length with NaN
        while len(actual) < n:
            actual.append(np.nan)
        
        # Predicted part - exponential decay model
        last_actual = actual[half_n - 1] if half_n > 0 else 100
        predicted = [np.nan] * half_n
        
        remaining = n - half_n
        for i in range(remaining):
            decay = last_actual * np.exp(-0.015 * i) + np.random.normal(0, 1)
            predicted.append(max(10, min(100, decay)))
        
        # Ensure predicted is exactly n length
        while len(predicted) < n:
            predicted.append(np.nan)
        predicted = predicted[:n]
        
        # Confidence intervals
        upper = []
        lower = []
        for p in predicted:
            if pd.isna(p) or p == 0:
                upper.append(np.nan)
                lower.append(np.nan)
            else:
                upper.append(p + 10)
                lower.append(max(0, p - 10))
        
        return pd.DataFrame({
            'date': dates,
            'rul_actual': actual[:n],
            'rul_predicted': predicted[:n],
            'confidence_upper': upper[:n],
            'confidence_lower': lower[:n]
        })
    
    def analyze_failure_modes(self):
        """Analyze potential failure modes and their probabilities"""
        
        failure_data = [
            {'category': 'Mechanical', 'failure_mode': 'Bearing Wear', 'probability': 35, 'severity': 8},
            {'category': 'Mechanical', 'failure_mode': 'Belt Degradation', 'probability': 25, 'severity': 5},
            {'category': 'Mechanical', 'failure_mode': 'Gear Damage', 'probability': 15, 'severity': 9},
            {'category': 'Electrical', 'failure_mode': 'Motor Overheating', 'probability': 30, 'severity': 7},
            {'category': 'Electrical', 'failure_mode': 'Sensor Failure', 'probability': 20, 'severity': 4},
            {'category': 'Electrical', 'failure_mode': 'Wiring Issue', 'probability': 10, 'severity': 6},
            {'category': 'Hydraulic', 'failure_mode': 'Fluid Leak', 'probability': 28, 'severity': 6},
            {'category': 'Hydraulic', 'failure_mode': 'Pump Failure', 'probability': 18, 'severity': 8},
            {'category': 'Software', 'failure_mode': 'Controller Error', 'probability': 12, 'severity': 5},
            {'category': 'Software', 'failure_mode': 'Communication Loss', 'probability': 8, 'severity': 7},
        ]
        
        return pd.DataFrame(failure_data)
    
    def generate_maintenance_schedule(self):
        """Generate AI-optimized maintenance schedule"""
        
        now = datetime.now()
        schedule = []
        
        for i, equipment in enumerate(self.equipment_list):
            start_offset = np.random.randint(1, 30)
            duration = np.random.randint(2, 8)
            
            priority = np.random.choice(['High', 'Medium', 'Low'], p=[0.2, 0.5, 0.3])
            
            schedule.append({
                'equipment': equipment,
                'start': now + timedelta(days=start_offset),
                'end': now + timedelta(days=start_offset + duration),
                'priority': priority,
                'task': np.random.choice(['Inspection', 'Replacement', 'Calibration', 'Overhaul'])
            })
        
        return pd.DataFrame(schedule)
    
    def get_feature_importance(self):
        """Get feature importance from the model"""
        
        features = ['Temperature', 'Vibration', 'Pressure', 'Operating Hours', 'Days Since Maintenance']
        importance = self.model.feature_importances_
        
        df = pd.DataFrame({
            'feature': features,
            'importance': importance
        }).sort_values('importance', ascending=True)
        
        return df


class AnomalyDetector:
    """Isolation Forest based anomaly detection for sensor data"""
    
    def __init__(self, contamination=0.1):
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.sensitivity = 0.7
    
    def set_sensitivity(self, sensitivity):
        """Adjust anomaly detection sensitivity"""
        self.sensitivity = sensitivity
        self.contamination = 0.05 + (1 - sensitivity) * 0.15
        self.model = IsolationForest(contamination=self.contamination, random_state=42)
    
    def detect_anomalies(self, historical_data):
        """Detect anomalies in historical sensor data"""
        
        n_points = len(historical_data)
        
        # Generate synthetic sensor values
        values = np.random.normal(50, 10, n_points)
        
        # Add some anomalies
        n_anomalies = int(n_points * self.contamination)
        anomaly_indices = np.random.choice(n_points, n_anomalies, replace=False)
        
        for idx in anomaly_indices:
            values[idx] += np.random.choice([-1, 1]) * np.random.uniform(25, 40)
        
        # Fit model and predict
        X = values.reshape(-1, 1)
        predictions = self.model.fit_predict(X)
        
        return pd.DataFrame({
            'date': historical_data['date'],
            'value': values,
            'is_anomaly': predictions == -1
        })


class EnergyForecaster:
    """AI model for energy consumption forecasting"""
    
    def __init__(self):
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self._train_model()
    
    def _train_model(self):
        """Train the energy forecasting model"""
        # Generate synthetic training data
        n_samples = 500
        
        # Features: hour, day_of_week, temperature, production_level
        hours = np.random.randint(0, 24, n_samples)
        X = np.column_stack([
            hours,
            np.random.randint(0, 7, n_samples),
            np.random.normal(25, 10, n_samples),
            np.random.uniform(50, 100, n_samples)
        ])
        
        # Energy consumption with realistic patterns
        hourly_factor = np.array([0.3, 0.25, 0.2, 0.2, 0.25, 0.4, 0.6, 0.85, 1.0, 1.0,
                                  0.95, 0.9, 0.85, 1.0, 1.0, 0.95, 0.9, 0.85, 0.7, 0.6,
                                  0.5, 0.45, 0.4, 0.35])
        
        y = 500 + X[:, 3] * 10 + np.array([hourly_factor[int(h)] * 300 for h in hours])
        y = y + np.random.normal(0, 50, n_samples)
        
        self.model.fit(X, y)
    
    def predict_energy(self, days=7):
        """Predict energy consumption for the next N days"""
        
        hours = days * 24 + 24  # Include 24 hours of historical
        dates = pd.date_range(start=datetime.now() - timedelta(hours=24),
                             periods=hours, freq='H')
        
        # Generate features
        X = np.column_stack([
            [d.hour for d in dates],
            [d.dayofweek for d in dates],
            np.random.normal(25, 5, hours),
            np.random.uniform(70, 95, hours)
        ])
        
        # Predictions
        predictions = self.model.predict(X)
        
        # Add confidence intervals
        std = np.std(predictions) * 0.15
        
        # Historical (first 24 hours) - use as "actual"
        actual = predictions[:24] + np.random.normal(0, 20, 24)
        actual = list(actual) + [np.nan] * (hours - 24)
        
        return pd.DataFrame({
            'date': dates,
            'actual': actual,
            'predicted': predictions,
            'upper': predictions + 2 * std,
            'lower': predictions - 2 * std
        })
    
    def get_recommendations(self):
        """Generate AI-based energy optimization recommendations"""
        
        return [
            {
                'title': 'Shift Peak Operations to Off-Peak Hours',
                'description': 'Move high-energy operations from 2-6 PM to 10 PM-6 AM to reduce peak demand charges by up to 20%.',
                'savings': '$4,500/month',
                'confidence': 0.92
            },
            {
                'title': 'Implement Variable Frequency Drives',
                'description': 'Install VFDs on main motors to optimize speed based on actual load requirements.',
                'savings': '$8,200/month',
                'confidence': 0.88
            },
            {
                'title': 'Optimize HVAC Scheduling',
                'description': 'Adjust HVAC pre-cooling schedule based on production calendar and weather forecast.',
                'savings': '$2,100/month',
                'confidence': 0.85
            },
            {
                'title': 'Compressed Air System Leak Detection',
                'description': 'AI analysis suggests 15% air leakage. Repair identified leaks in pneumatic system.',
                'savings': '$1,800/month',
                'confidence': 0.78
            }
        ]
    
    def calculate_savings(self):
        """Calculate potential savings breakdown"""
        
        return pd.DataFrame({
            'category': ['Current Cost', 'Peak Shaving', 'Efficiency Gains', 
                        'Demand Response', 'Process Optimization', 'Total Savings'],
            'value': [-25000, 3500, 4200, 1800, 2500, 12000]
        })


class QualityPredictor:
    """AI model for predicting product quality based on process parameters"""
    
    def __init__(self):
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self._train_model()
    
    def _train_model(self):
        """Train the quality prediction model"""
        n_samples = 1000
        
        # Features: temperature, pressure, speed, humidity
        temp = np.random.normal(65, 15, n_samples)
        pressure = np.random.normal(120, 30, n_samples)
        speed = np.random.normal(55, 15, n_samples)
        humidity = np.random.normal(45, 10, n_samples)
        
        X = np.column_stack([temp, pressure, speed, humidity])
        
        # Quality score (0-100) with realistic relationships
        y = 95 - 0.2 * np.abs(temp - 65) - 0.1 * np.abs(pressure - 120)
        y = y - 0.15 * np.abs(speed - 55) - 0.1 * np.abs(humidity - 45)
        y = y + np.random.normal(0, 3, n_samples)
        y = np.clip(y, 0, 100)
        
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
    
    def predict(self, temperature, pressure, speed, humidity):
        """Predict quality score based on input parameters"""
        
        features = np.array([[temperature, pressure, speed, humidity]])
        features_scaled = self.scaler.transform(features)
        
        quality_score = self.model.predict(features_scaled)[0]
        quality_score = np.clip(quality_score, 0, 100)
        
        # Calculate derived metrics
        pass_probability = min(99, quality_score + np.random.uniform(-3, 5))
        defect_risk = max(0, 100 - quality_score - np.random.uniform(-2, 3))
        
        # Determine key factors
        key_factors = []
        
        if temperature > 80:
            key_factors.append("⚠️ High temperature may affect adhesion")
        elif temperature < 50:
            key_factors.append("⚠️ Low temperature may slow curing")
        else:
            key_factors.append("✅ Temperature in optimal range")
        
        if pressure > 150:
            key_factors.append("⚠️ High pressure may cause deformation")
        elif pressure < 90:
            key_factors.append("⚠️ Low pressure may affect bonding")
        else:
            key_factors.append("✅ Pressure in optimal range")
        
        if speed > 70:
            key_factors.append("⚠️ High speed may reduce precision")
        else:
            key_factors.append("✅ Speed is appropriate")
        
        return {
            'quality_score': quality_score,
            'pass_probability': pass_probability,
            'defect_risk': defect_risk,
            'key_factors': key_factors
        }
