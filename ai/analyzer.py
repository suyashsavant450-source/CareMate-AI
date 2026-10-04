import os
from dotenv import load_dotenv
from groq import Groq

from ai.prompts import SYSTEM_PROMPT, build_analysis_prompt

load_dotenv()

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured in .env"
        )

    return Groq(api_key=api_key)


def _run_ai(prompt, temperature=0.2, max_tokens=1200):
    client = get_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("Groq returned an empty response.")

    return result.strip()


# =========================================================
# FULL MEDICAL REPORT ANALYSIS
# =========================================================

def analyze_report(report_text, previous_report_text=None):

    if not report_text or not report_text.strip():
        raise ValueError(
            "No medical report text was provided."
        )

    prompt = build_analysis_prompt(
        report_text,
        previous_report_text
    )

    return _run_ai(
        prompt,
        temperature=0.2,
        max_tokens=1800
    )


# =========================================================
# TRANSLATE FULL ANALYSIS
# =========================================================

def translate_analysis(text, language):

    if not text or not text.strip():
        raise ValueError(
            "No analysis text available."
        )

    prompt = f"""
Translate the following CareMate AI medical report explanation
into {language}.

IMPORTANT:

- Preserve the meaning of the original.
- Use simple patient-friendly language.
- Do not add new medical information.
- Do not remove important abnormal findings.
- Do not diagnose.
- Do not prescribe medicines.
- Do not change medicine doses.
- Do not invent values.
- Keep medical values, dates and reference ranges accurate.
- Keep the response reasonably detailed.
- Use natural {language}.

ORIGINAL CAREMATE ANALYSIS:
---------------------------
{text}
---------------------------
"""

    return _run_ai(
        prompt,
        temperature=0.2,
        max_tokens=1500
    )


# =========================================================
# SHORT VOICE SUMMARY
# =========================================================

def create_voice_summary(report_text):

    if not report_text or not report_text.strip():
        raise ValueError(
            "No report text available for voice summary."
        )

    prompt = f"""
Create a short voice-friendly summary of the following
medical report.

RULES:

- Maximum 90 words.
- Suitable for approximately 30–45 seconds of speech.
- Mention the 2–4 most important findings.
- Prioritize abnormal or notable values.
- Include actual values when available.
- Include reference ranges when useful.
- Explain important findings in simple language.
- Do not diagnose.
- Do not prescribe medicines.
- Do not recommend treatment.
- Do not invent information.
- End by suggesting discussion with a qualified healthcare
  professional if there are concerning findings.
- Use short natural sentences.

MEDICAL REPORT:
----------------
{report_text}
----------------
"""

    return _run_ai(
        prompt,
        temperature=0.2,
        max_tokens=400
    )