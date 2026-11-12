import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

from backend.config.settings import settings

logger = logging.getLogger(__name__)

client = None
if settings.GROQ_API_KEY:
    client = Groq(api_key=settings.GROQ_API_KEY)

MODEL = "llama-3.3-70b-versatile"

def build_executive_context(analysis: dict | None) -> str:
    if not analysis:
        return "No analysis available."

    # Helper to safely truncate lists to prevent token bloat
    def truncate_list(data, limit=5):
        if not data: return []
        return data[:limit]

    anomalies = truncate_list(analysis.get("anomalies", []))
    insights = truncate_list(analysis.get("insights", []))
    recommendations = truncate_list(analysis.get("recommendations", []))
    executive_action_plan = truncate_list(analysis.get("executive_action_plan", []))

    return f"""
BUSINESS STATUS: {analysis.get("business_status", "Unknown")}
HEALTH SCORE: {analysis.get("health_score", "Unknown")}
DATASET SUMMARY: {analysis.get("dataset_summary", {})}
EXECUTIVE SUMMARY: {analysis.get("executive_summary", {})}
KPIs: {analysis.get("kpis", {})}
INSIGHTS: {insights}
ANOMALIES DETECTED ({len(analysis.get("anomalies", []))} total, showing top {len(anomalies)}): {anomalies}
RISK ASSESSMENT: {analysis.get("risk_assessment", {})}
FORECASTS: {analysis.get("forecasts", {})}
RECOMMENDATIONS: {recommendations}
ROOT CAUSE ANALYSIS: {analysis.get("root_cause_analysis", {})}
CORRELATION INTELLIGENCE: {analysis.get("correlation_analysis", {})}
DEPENDENCY INTELLIGENCE: {analysis.get("dependency_analysis", {})}
CAUSAL INTELLIGENCE: {analysis.get("causal_analysis", {})}
STRATEGIC LEVERAGE INTELLIGENCE: {analysis.get("strategic_leverage_analysis", {})}
EXECUTIVE OPTIMIZATION: {analysis.get("executive_optimization", {})}
SCENARIO SIMULATIONS: {analysis.get("scenario_simulations", {})}
EXECUTIVE ACTION PLAN: {executive_action_plan}
"""

def ask_ai(message: str, analysis: dict = None, conversation_history: list = None) -> str:
    if not client:
        return "NeuroSync Executive AI is currently unavailable. Configure GROQ_API_KEY to enable AI features."

    if conversation_history is None:
        conversation_history = []

    executive_context = build_executive_context(analysis)

    # 1. Consolidated System Prompt (Persona + Rules)
    system_prompt = """You are NeuroSync Executive AI, an elite Decision Intelligence Consultant acting simultaneously as CFO, CEO Advisor, Risk Consultant, and Growth Strategist.

CORE DIRECTIVES:
1. Use ONLY information available in the provided executive context. Never invent numbers.
2. Always provide reasoning before recommendations. Think strategically.
3. Connect recommendations to KPIs, risk scores, anomalies, forecasts, root causes, and critical dependencies.
4. Avoid generic consulting advice. Be practical, decision-oriented, and executive-level.
5. Explain using: Observation -> Business Meaning -> Impact -> Recommendation.
6. Use markdown formatting for clean, readable responses.

CONVERSATION RULES:
- Use previous discussion when relevant and continue naturally.
- Do not regenerate the entire executive report unless explicitly requested.
- Answer follow-up questions directly.

When asked for a full diagnosis/summary, use this structure:
# 📋 Executive Summary
# 🔍 Key Findings
# ⚠️ Risk Assessment
# 📈 Growth Opportunities
# 🎯 Strategic Recommendations
# 🚀 Executive Action Plan
"""

    # 2. Build the Messages Array
    messages = [
        {"role": "system", "content": system_prompt},
        # Inject the data as a user message so the AI treats it as ground truth
        {"role": "user", "content": f"Here is the current business data and executive context:\n\n{executive_context}"},
        # Acknowledge the data so the AI knows it has "read" it
        {"role": "assistant", "content": "I have reviewed the executive context and am ready to provide strategic guidance. What is your primary focus or question?"}
    ]
    
    # Append actual conversation history (now properly formatted as separate messages)
    messages.extend(conversation_history)
    
    # Append the current user question
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.35,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq request failed: {str(e)}")
        # Return the actual error so you can debug. 
        # (IMPORTANT: Change this to a generic message before going to production!)
        return f"AI Error: {str(e)}"