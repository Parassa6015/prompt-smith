import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"


def generate_sql_rewrite(sql: str, instruction: str) -> str:
    prompt = (
        f"{instruction}\n\n"
        f"Rewrite this SQL:\n{sql}\n\n"
        "Output only the rewritten SQL. No explanation."
    )

    model = genai.GenerativeModel(MODEL_NAME)

    response = model.generate_content(prompt)

    rewritten = response.text.strip()

    return rewritten
