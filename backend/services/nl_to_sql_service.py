import google.generativeai as genai
from services.cleaner import clean_sql_output
from services.schema_service import get_schema_text



def generate_sql_from_prompt(prompt: str):
    schema_text = get_schema_text()

    final_prompt = f"""
You are an expert SQL generator.

User request:
{prompt}

Database schema:
{schema_text}

Rules:
- ONLY return valid SQL for PostgreSQL.
- DO NOT include markdown or backticks.
- DO NOT explain anything.
- SELECT-only queries.
- Always include LIMIT 100 unless the user requests otherwise.
- Columns and table names must match the schema exactly.

Return ONLY the SQL query.
"""

    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(final_prompt)
    sql_raw = response.text

    return clean_sql_output(sql_raw)
