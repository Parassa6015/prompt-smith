from utils.db import get_connection

def get_schema_text():
    conn = get_connection()
    cur = conn.cursor()

    # Get all table names
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    tables = [t["table_name"] for t in cur.fetchall()]

    schema_info = []

    for table in tables:
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, (table,))

        columns = cur.fetchall()

        column_lines = [
            f"- {col['column_name']} ({col['data_type']})"
            for col in columns
        ]

        schema_info.append(
            f"Table: {table}\n" + "\n".join(column_lines)
        )

    conn.close()

    return "\n\n".join(schema_info)
