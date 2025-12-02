def clean_sql_output(text: str):
    if not text:
        return ""

    cleaned = (
        text.replace("```sql", "")
            .replace("```", "")
            .replace("`", "")
            .replace("<s>", "")
            .replace("</s>", "")
            .strip()
    )

    # Remove any "SQL:" prefix
    if cleaned.lower().startswith("sql:"):
        cleaned = cleaned[4:].strip()

    return cleaned