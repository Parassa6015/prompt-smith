import re;
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

def is_prompt_safe(prompt: str):
    p = prompt.lower()

    forbidden = [
        r"\bdelete\b", r"\bdrop\b", r"\btruncate\b", r"\bremove\b",
        r"\bupdate\b", r"\binsert\b", r"\bmodify\b", r"\bdestroy\b",
        r"\bwipe\b", r"\bclear\b", r"\berase\b"
    ]

    for pattern in forbidden:
        if re.search(pattern, p):
            return False

    return True