"""Configuration for advanced SQL tests (views, procedures, triggers) - PostgreSQL."""
import pytest
import psycopg2
import psycopg2.extras


@pytest.fixture(scope='module')
def conn():
    """Create a database connection for advanced tests."""
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


def execute_sql_file(conn, filepath):
    """Execute SQL from a file, handling PostgreSQL-specific syntax."""
    with open(filepath, 'r') as f:
        sql = f.read()

    # Remove comments and empty lines
    lines = []
    for line in sql.split('\n'):
        line = line.strip()
        if line and not line.startswith('--'):
            lines.append(line)

    sql_clean = '\n'.join(lines)

    if not sql_clean.strip():
        raise ValueError(f"No SQL found in {filepath}")

    with conn.cursor() as cursor:
        cursor.execute(sql_clean)
        conn.commit()

        # Try to fetch results if it's a SELECT
        try:
            return cursor.fetchall()
        except psycopg2.ProgrammingError:
            return None


def cleanup_view(conn, view_name):
    """Drop a view if it exists."""
    with conn.cursor() as cursor:
        cursor.execute(f"DROP VIEW IF EXISTS {view_name} CASCADE")
        conn.commit()


def cleanup_procedure(conn, proc_name):
    """Drop a procedure if it exists."""
    with conn.cursor() as cursor:
        cursor.execute(f"DROP PROCEDURE IF EXISTS {proc_name} CASCADE")
        conn.commit()


def cleanup_trigger(conn, trigger_name):
    """Drop a trigger if it exists."""
    with conn.cursor() as cursor:
        # In PostgreSQL, we need to drop the trigger AND its function
        cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name} ON games CASCADE")
        # Try to drop common trigger function names
        function_name = trigger_name.replace('trg_', '').replace('trigger_', '')
        cursor.execute(f"DROP FUNCTION IF EXISTS {function_name}() CASCADE")
        conn.commit()


def cleanup_function(conn, function_name):
    """Drop a function if it exists."""
    with conn.cursor() as cursor:
        cursor.execute(f"DROP FUNCTION IF EXISTS {function_name} CASCADE")
        conn.commit()
