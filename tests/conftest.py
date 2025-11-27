import pytest
import psycopg2
import psycopg2.extras
import os

class MissingQueryError(Exception):
    pass

@pytest.fixture(scope="session")
def conn():
    """Create PostgreSQL database connection."""
    connection = psycopg2.connect(
        host='postgres',
        user='root',
        password='rootpwd',
        database='vg',
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    connection.autocommit = False
    yield connection
    connection.close()

def run_sql_file(conn, filepath):
    """Execute SQL from a file and return results."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} not found")

    with open(filepath, 'r') as f:
        sql = f.read()

    # Strip comments and empty lines
    lines = []
    for line in sql.split('\n'):
        line = line.strip()
        if line and not line.startswith('--'):
            lines.append(line)

    sql_clean = '\n'.join(lines)

    if not sql_clean.strip():
        raise MissingQueryError(f"No SQL found in {filepath}")

    with conn.cursor() as cursor:
        cursor.execute(sql_clean)
        try:
            return cursor.fetchall()
        except psycopg2.ProgrammingError:
            # No results to fetch (INSERT, UPDATE, etc.)
            return None
