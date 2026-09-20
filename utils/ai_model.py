from google import genai
from utils.config import GEMINI_API_KEY
from rag.rag_engine import search_documents

client = genai.Client(api_key=GEMINI_API_KEY)


def ask_ai(question):

    try:
        context = search_documents(question)

        prompt = f"""
You are JP Arogya AI, a healthcare assistant.

Medical Context:
{context}

User Question:
{question}

Rules:
1. Explain in simple English.
2. Do not diagnose with certainty.
3. Give useful general health information.
4. Suggest consulting a doctor when appropriate.
5. Keep the answer concise.

This information is for educational purposes only and is not a substitute for professional medical advice.
"""

        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"AI Error: {e}"


def analyze_report(report_text):

    try:

        prompt = f"""
You are JP Arogya AI.

Analyze this medical report:

{report_text}

Return:

1. Report Summary
2. Important Findings
3. Abnormal Values
4. Possible Meaning
5. Diet Suggestions
6. Lifestyle Advice
7. When to Visit a Doctor

This report explanation is for educational purposes only and is not a substitute for a doctor's diagnosis.
"""

        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"AI Error: {e}"