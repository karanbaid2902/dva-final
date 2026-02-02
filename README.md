# 🏭 TitanForge Industries - Smart Manufacturing & IoT Analytics Dashboard

A **Master's level project** featuring an AI-powered Smart Manufacturing Dashboard built with Streamlit. This dashboard provides real-time monitoring, predictive maintenance, energy analytics, quality control, and production analytics using synthetic IoT sensor data.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [AI/ML Components](#-aiml-components)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Dashboard Modules](#-dashboard-modules)
- [Technical Architecture](#-technical-architecture)
- [Future Enhancements](#-future-enhancements)

---

## ✨ Features

### 📊 Real-Time Monitoring
- Live sensor data visualization (temperature, vibration, pressure)
- Machine status overview with efficiency metrics
- Active alerts and notifications system
- Auto-refresh with configurable intervals

### 🔧 Predictive Maintenance
- Equipment health scoring using Random Forest classifier
- Remaining Useful Life (RUL) prediction with confidence intervals
- Failure mode analysis with treemap visualization
- AI-optimized maintenance scheduling

### ⚡ Energy Analytics
- 24-hour energy consumption profiling
- AI-powered energy forecasting (7-day horizon)
- Cost optimization recommendations
- Carbon footprint tracking

### ✅ Quality Control
- Statistical Process Control (SPC) charts
- Defect distribution analysis
- Real-time quality prediction based on process parameters
- First Pass Yield and defect rate monitoring

### 📈 Production Analytics
- OEE (Overall Equipment Effectiveness) breakdown
- Production trend analysis
- Downtime analysis with sunburst visualization
- Shift performance comparison using radar charts

### 🤖 AI Insights
- Anomaly detection using Isolation Forest
- Feature importance analysis
- Correlation matrix visualization
- AI-generated action items with priority ranking

---

## 🧠 AI/ML Components

| Model | Algorithm | Purpose |
|-------|-----------|---------|
| Predictive Maintenance | Random Forest Classifier | Equipment failure prediction |
| Anomaly Detection | Isolation Forest | Sensor anomaly identification |
| Energy Forecasting | Gradient Boosting Regressor | Energy consumption prediction |
| Quality Prediction | Gradient Boosting Regressor | Product quality scoring |

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd SmartManufacturingDashboard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

### Configuration Options

- **Live Data Streaming**: Toggle real-time data updates
- **Refresh Rate**: Adjust update interval (1-10 seconds)
- **Production Lines**: Select lines to monitor
- **Prediction Horizon**: Choose AI prediction timeframe
- **Anomaly Sensitivity**: Adjust anomaly detection threshold

---

## 📁 Project Structure

```
SmartManufacturingDashboard/
│
├── app.py                 # Main Streamlit application
├── data_generator.py      # Synthetic data generation module
├── ml_models.py           # AI/ML models for analytics
├── utils.py               # Utility functions and helpers
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 📊 Dashboard Modules

### 1. Real-Time Monitoring
Monitor live sensor data with interactive visualizations:
- Temperature gauges for multiple sensors
- Real-time vibration analysis with threshold alerts
- Pressure monitoring (hydraulic, pneumatic, cooling)
- Machine status with efficiency metrics

### 2. Predictive Maintenance
AI-powered maintenance intelligence:
- Health score calculation for each equipment
- Days until maintenance prediction
- Failure mode probability analysis
- Gantt chart for maintenance scheduling

### 3. Energy Analytics
Comprehensive energy management:
- Hourly consumption vs baseline comparison
- Energy distribution by production line
- 7-day AI forecast with confidence bands
- Optimization recommendations with ROI

### 4. Quality Control
Ensure product quality with AI:
- Real-time SPC with control limits
- Interactive quality prediction tool
- Defect pareto analysis
- Process parameter optimization

### 5. Production Analytics
Track and optimize production:
- OEE component breakdown (Availability, Performance, Quality)
- 30-day production trend analysis
- Downtime root cause analysis
- Multi-shift performance comparison

### 6. AI Insights
Advanced analytics and recommendations:
- Automated anomaly detection results
- Feature importance for model interpretability
- Sensor correlation analysis
- Prioritized action items

---

## 🏗️ Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│
│  │Real-Time│ │Pred.    │ │Energy   │ │Quality  │ │AI       ││
│  │Monitor  │ │Maint.   │ │Analytics│ │Control  │ │Insights ││
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘│
└───────┼──────────┼──────────┼──────────┼──────────┼────────┘
        │          │          │          │          │
        ▼          ▼          ▼          ▼          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Processing Layer                          │
│  ┌─────────────────┐        ┌─────────────────────────────┐ │
│  │ Data Generator  │        │      ML Models              │ │
│  │ - Sensors       │        │ - Predictive Maintenance    │ │
│  │ - Production    │◄──────►│ - Anomaly Detection        │ │
│  │ - Quality       │        │ - Energy Forecasting        │ │
│  │ - Energy        │        │ - Quality Prediction        │ │
│  └─────────────────┘        └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Visualization Layer                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │   Plotly    │ │  Gauges &   │ │   Statistical Charts    ││
│  │   Charts    │ │  Indicators │ │   (SPC, Pareto, etc.)   ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## 🔮 Future Enhancements

- [ ] **Database Integration**: Connect to real IoT databases (InfluxDB, TimescaleDB)
- [ ] **Deep Learning Models**: Implement LSTM for time-series forecasting
- [ ] **Computer Vision**: Add defect detection using image analysis
- [ ] **Natural Language**: Integrate LLM for conversational analytics
- [ ] **Edge Computing**: Support for edge device data ingestion
- [ ] **Multi-tenant**: Support for multiple factory locations
- [ ] **API Layer**: RESTful API for external integrations
- [ ] **Alerting System**: Email/SMS notifications for critical events

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**TitanForge Industries R&D Team**

*Smart Manufacturing & IoT Analytics Dashboard - A Master's Level Project*

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

<p align="center">
  <strong>🏭 TitanForge Industries</strong><br>
  <em>Powering the Future of Manufacturing with AI</em>
</p>
