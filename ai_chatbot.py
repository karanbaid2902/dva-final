"""
AI Chatbot for Smart Manufacturing Dashboard
Provides intelligent responses about manufacturing data and insights
"""

import random
import re
from datetime import datetime


class ManufacturingChatbot:
    """AI-powered chatbot for manufacturing analytics queries"""
    
    def __init__(self):
        self.context = {}
        self.conversation_history = []
        
        # Knowledge base for manufacturing queries
        self.knowledge_base = {
            'oee': {
                'keywords': ['oee', 'overall equipment effectiveness', 'equipment effectiveness'],
                'response': """**Overall Equipment Effectiveness (OEE)** is currently at {oee:.1f}%.

OEE is calculated as: **Availability × Performance × Quality**

📊 **Current Breakdown:**
- Availability: {availability:.1f}%
- Performance: {performance:.1f}%
- Quality: {quality:.1f}%

💡 **Recommendation:** {recommendation}"""
            },
            'maintenance': {
                'keywords': ['maintenance', 'repair', 'fix', 'broken', 'failure', 'predict'],
                'response': """🔧 **Predictive Maintenance Analysis**

Based on AI analysis of sensor data:

{equipment_status}

⏰ **Upcoming Maintenance:**
{maintenance_schedule}

💰 **Projected Cost Savings:** ${savings:,} this month through predictive maintenance."""
            },
            'energy': {
                'keywords': ['energy', 'power', 'consumption', 'electricity', 'kwh', 'carbon'],
                'response': """⚡ **Energy Analytics Summary**

📊 **Today's Consumption:** {today_kwh:,.0f} kWh
📈 **Peak Demand:** {peak_kw:,.0f} kW
💵 **Cost:** ${cost:,.2f}
🌱 **Carbon Footprint:** {carbon:.0f} kg CO₂

💡 **AI Recommendations:**
{recommendations}"""
            },
            'quality': {
                'keywords': ['quality', 'defect', 'defects', 'reject', 'scrap', 'yield', 'fpy'],
                'response': """✅ **Quality Control Summary**

📊 **First Pass Yield:** {fpy:.1f}%
❌ **Defect Rate:** {defect_rate:.2f}%
🔄 **Rework Rate:** {rework_rate:.2f}%

🔍 **Top Defect Types:**
{defect_types}

💡 **AI Insight:** {insight}"""
            },
            'production': {
                'keywords': ['production', 'output', 'units', 'throughput', 'capacity', 'rate'],
                'response': """📈 **Production Analytics**

📊 **Today's Output:** {units:,} units
🎯 **Target Achievement:** {target_pct:.1f}%
⏱️ **Average Cycle Time:** {cycle_time:.1f} seconds
🏭 **Throughput:** {throughput:.0f} units/hour

📉 **Production by Line:**
{line_production}"""
            },
            'alert': {
                'keywords': ['alert', 'alarm', 'warning', 'critical', 'issue', 'problem'],
                'response': """⚠️ **Active Alerts Summary**

{alerts}

💡 **Recommended Actions:**
{actions}"""
            },
            'anomaly': {
                'keywords': ['anomaly', 'anomalies', 'unusual', 'abnormal', 'outlier'],
                'response': """🔍 **Anomaly Detection Results**

📊 **Anomalies Detected (Last 24h):** {count}
📈 **Anomaly Rate:** {rate:.2f}%
🎯 **Model Confidence:** {confidence:.1f}%

🚨 **Recent Anomalies:**
{anomaly_list}

💡 **Root Cause Analysis:** {root_cause}"""
            },
            'help': {
                'keywords': ['help', 'what can you do', 'commands', 'how to', 'guide'],
                'response': """🤖 **TitanForge AI Assistant**

I can help you with:

📊 **Analytics Queries:**
- "What is the current OEE?"
- "Show me energy consumption"
- "Analyze production rates"
- "What's the defect rate?"

🔧 **Maintenance:**
- "When is the next maintenance?"
- "Which machines need attention?"
- "Predict equipment failures"

⚠️ **Alerts & Issues:**
- "Show active alerts"
- "Any anomalies detected?"
- "What problems need attention?"

📈 **Insights:**
- "Give me optimization tips"
- "How can we improve efficiency?"
- "Summarize today's performance"

Just ask your question naturally!"""
            },
            'summary': {
                'keywords': ['summary', 'overview', 'status', 'dashboard', 'report', 'today'],
                'response': """📊 **Daily Operations Summary**

🏭 **Production:**
- Units Produced: {units:,}
- Target Achievement: {target_pct:.1f}%
- OEE: {oee:.1f}%

⚡ **Energy:**
- Consumption: {energy:,.0f} kWh
- Cost: ${cost:,.2f}

✅ **Quality:**
- First Pass Yield: {fpy:.1f}%
- Defect Rate: {defect_rate:.2f}%

🔧 **Maintenance:**
- Equipment Health: {health_status}
- Next Scheduled: {next_maintenance}

⚠️ **Alerts:** {alert_count} active

💡 **Top Priority:** {priority}"""
            },
            'optimize': {
                'keywords': ['optimize', 'improve', 'better', 'increase', 'reduce', 'efficiency', 'tips'],
                'response': """💡 **AI Optimization Recommendations**

Based on current data analysis:

🎯 **High Impact Actions:**
{high_impact}

📊 **Medium Impact Actions:**
{medium_impact}

⏰ **Quick Wins:**
{quick_wins}

📈 **Projected Improvements:**
- OEE: +{oee_improvement:.1f}%
- Energy Savings: {energy_savings}%
- Quality Improvement: +{quality_improvement:.1f}%"""
            }
        }
        
        # Default responses for unmatched queries
        self.default_responses = [
            "I understand you're asking about '{query}'. Could you be more specific? Try asking about OEE, energy, quality, production, or maintenance.",
            "I'm not sure about '{query}'. You can ask me about equipment status, energy consumption, quality metrics, or production data.",
            "Let me help you better! Try questions like 'What's the current OEE?' or 'Show me today's production summary'.",
        ]
    
    def update_context(self, data):
        """Update chatbot context with current dashboard data"""
        self.context = data
    
    def get_response(self, user_query, dashboard_data=None):
        """Generate AI response based on user query"""
        
        if dashboard_data:
            self.context = dashboard_data
        
        query_lower = user_query.lower().strip()
        
        # Find matching topic
        matched_topic = None
        for topic, info in self.knowledge_base.items():
            for keyword in info['keywords']:
                if keyword in query_lower:
                    matched_topic = topic
                    break
            if matched_topic:
                break
        
        if matched_topic:
            response = self._generate_response(matched_topic)
        else:
            response = random.choice(self.default_responses).format(query=user_query[:50])
        
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'user': user_query,
            'assistant': response
        })
        
        return response
    
    def _generate_response(self, topic):
        """Generate response with real data"""
        
        template = self.knowledge_base[topic]['response']
        
        # Generate dynamic data based on topic
        if topic == 'oee':
            oee = self.context.get('oee', random.uniform(78, 92))
            availability = random.uniform(88, 96)
            performance = random.uniform(85, 95)
            quality = random.uniform(95, 99.5)
            
            recommendations = [
                "Focus on reducing changeover time to improve availability.",
                "Consider implementing TPM to boost performance.",
                "Review quality inspection protocols on Line B.",
                "Current performance is above target. Maintain current practices."
            ]
            
            return template.format(
                oee=oee,
                availability=availability,
                performance=performance,
                quality=quality,
                recommendation=random.choice(recommendations)
            )
        
        elif topic == 'maintenance':
            equipment_list = [
                "✅ CNC Machine #1: Healthy (92% health score)",
                "✅ CNC Machine #2: Healthy (88% health score)",
                "⚠️ CNC Machine #3: Attention needed (65% health score)",
                "✅ Robot Arm A: Healthy (94% health score)",
                "🔴 Press Machine: Maintenance due in 3 days"
            ]
            
            schedule = [
                "• CNC Machine #3: Bearing replacement - Feb 5",
                "• Press Machine: Full inspection - Feb 7",
                "• Conveyor System: Belt check - Feb 10"
            ]
            
            return template.format(
                equipment_status='\n'.join(equipment_list),
                maintenance_schedule='\n'.join(schedule),
                savings=random.randint(15000, 45000)
            )
        
        elif topic == 'energy':
            recommendations = [
                "• Shift peak operations to off-peak hours (10 PM - 6 AM)",
                "• Install VFDs on main motors - potential 15% savings",
                "• Fix compressed air leaks detected in Zone 3",
                "• Optimize HVAC scheduling based on occupancy"
            ]
            
            return template.format(
                today_kwh=random.uniform(15000, 18000),
                peak_kw=random.uniform(800, 1200),
                cost=random.uniform(1800, 2500),
                carbon=random.uniform(8000, 12000),
                recommendations='\n'.join(recommendations)
            )
        
        elif topic == 'quality':
            defect_types = [
                "1. Surface scratches: 35%",
                "2. Dimensional errors: 28%",
                "3. Color variations: 20%",
                "4. Weld defects: 17%"
            ]
            
            insights = [
                "Temperature fluctuations on Line B correlate with increased defects.",
                "Morning shift shows 15% better quality metrics than night shift.",
                "Consider recalibrating sensors on Station 5.",
                "Quality trending upward - maintain current process parameters."
            ]
            
            return template.format(
                fpy=random.uniform(95, 99),
                defect_rate=random.uniform(0.5, 1.5),
                rework_rate=random.uniform(0.8, 2.0),
                defect_types='\n'.join(defect_types),
                insight=random.choice(insights)
            )
        
        elif topic == 'production':
            line_production = [
                "• Line A (Assembly): 1,350 units (102% of target)",
                "• Line B (Welding): 1,180 units (94% of target)",
                "• Line C (Painting): 980 units (98% of target)",
                "• Line D (Packaging): 1,420 units (108% of target)"
            ]
            
            return template.format(
                units=random.randint(4500, 5500),
                target_pct=random.uniform(92, 105),
                cycle_time=random.uniform(12, 16),
                throughput=random.uniform(200, 250),
                line_production='\n'.join(line_production)
            )
        
        elif topic == 'alert':
            alerts = [
                "🔴 CRITICAL: Temperature threshold exceeded on CNC #3",
                "🟡 WARNING: Vibration anomaly on Robot Arm A",
                "🟡 WARNING: Energy consumption 15% above baseline",
                "🔵 INFO: Scheduled maintenance reminder for tomorrow"
            ]
            
            actions = [
                "1. Immediately check CNC Machine #3 cooling system",
                "2. Schedule inspection for Robot Arm A bearings",
                "3. Review energy usage patterns for optimization",
                "4. Confirm maintenance crew availability for tomorrow"
            ]
            
            return template.format(
                alerts='\n'.join(alerts),
                actions='\n'.join(actions)
            )
        
        elif topic == 'anomaly':
            anomaly_list = [
                "• 14:23 - Pressure spike on Hydraulic System (+45%)",
                "• 11:47 - Temperature drift on Motor 2 (+12°C)",
                "• 09:15 - Vibration pattern change on Conveyor"
            ]
            
            root_causes = [
                "Pattern suggests bearing degradation in hydraulic pump.",
                "Cooling system efficiency may be reduced - check filters.",
                "Likely caused by belt tension variation."
            ]
            
            return template.format(
                count=random.randint(3, 12),
                rate=random.uniform(0.5, 2.5),
                confidence=random.uniform(92, 98),
                anomaly_list='\n'.join(anomaly_list),
                root_cause=random.choice(root_causes)
            )
        
        elif topic == 'summary':
            health_statuses = ["Good", "Excellent", "Needs Attention"]
            priorities = [
                "Address CNC Machine #3 temperature warning",
                "Complete scheduled maintenance on Press Machine",
                "Review Line B quality metrics",
                "All systems operating normally"
            ]
            
            return template.format(
                units=random.randint(4500, 5500),
                target_pct=random.uniform(92, 105),
                oee=random.uniform(78, 92),
                energy=random.uniform(15000, 18000),
                cost=random.uniform(1800, 2500),
                fpy=random.uniform(95, 99),
                defect_rate=random.uniform(0.5, 1.5),
                health_status=random.choice(health_statuses),
                next_maintenance="Feb 5, 2026",
                alert_count=random.randint(2, 6),
                priority=random.choice(priorities)
            )
        
        elif topic == 'optimize':
            high_impact = [
                "1. Implement predictive maintenance on CNC machines (-30% downtime)",
                "2. Optimize batch scheduling to reduce changeover time",
                "3. Install real-time quality monitoring on Line B"
            ]
            
            medium_impact = [
                "1. Upgrade to energy-efficient motors on conveyor system",
                "2. Implement automated defect detection using computer vision",
                "3. Cross-train operators for multi-line capability"
            ]
            
            quick_wins = [
                "1. Adjust temperature setpoints based on AI recommendations",
                "2. Reschedule energy-intensive operations to off-peak hours",
                "3. Update SPC control limits based on recent data"
            ]
            
            return template.format(
                high_impact='\n'.join(high_impact),
                medium_impact='\n'.join(medium_impact),
                quick_wins='\n'.join(quick_wins),
                oee_improvement=random.uniform(3, 8),
                energy_savings=random.randint(10, 20),
                quality_improvement=random.uniform(0.5, 2)
            )
        
        elif topic == 'help':
            return template
        
        return template
    
    def get_conversation_history(self):
        """Return conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
