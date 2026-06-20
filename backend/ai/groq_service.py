import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)

MODEL = "llama-3.3-70b-versatile"

def build_executive_context(
    analysis: dict | None
) -> str:

    if not analysis:
        return "No analysis available."

    return f"""
KPIs:
{analysis.get("kpis", {})}

Insights:
{analysis.get("insights", [])}

Risk Assessment:
{analysis.get("risk_assessment", {})}

Forecasts:
{analysis.get("forecasts", {})}

Recommendations:
{analysis.get("recommendations", [])}

Decisions:
{analysis.get("decisions", {})}

Executive Summary:
{analysis.get("executive_summary", {})}
"""

def ask_ai(
    message: str,
    analysis: dict = None
) -> str:
    executive_context = (
        build_executive_context(
            analysis
        )
    )

    try:

        prompt = f"""
You are NeuroSync AI.

You are an executive business analyst,
not a report generator.

EXECUTIVE CONTEXT:

{executive_context}

USER QUESTION:

{message}

IMPORTANT RULES:

1. Answer ONLY the user's question.
2. Use dataset values as evidence.
3. Do NOT repeat the entire report.
4. Do NOT always generate:
   - Business Interpretation
   - Risks
   - Recommendations
   - Executive Summary

5. If the user asks:
   "What are anomalies?"
   explain anomalies only.

6. If the user asks:
   "Why is risk high?"
   explain risk only.

7. If the user asks:
   "Suggest growth opportunities"
   provide growth opportunities only.

8. Be conversational.
9. Be concise.
10. Think like a business consultant.

Return clean markdown.
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """
You are NeuroSync AI.

An executive decision intelligence copilot.

Answer naturally.

Do not generate unnecessary sections.

Focus on the user's question.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1200
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return f"Groq Error: {str(e)}"