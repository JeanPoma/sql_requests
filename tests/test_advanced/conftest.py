"""Configuration for advanced SQL tests (views, procedures, triggers)."""
import pytest
import pymysql


@pytest.fixture(scope='module')
def conn():
    """Create a database connection for advanced tests."""
    connection = pymysql.connect(
        host='mariadb',
        user='root',
        password='rootpwd',
        database='vg',
        cursorclass=pymysql.cursors.DictCursor
    )
    yield connection
    connection.close()


def execute_sql_file(conn, filepath):
    """Execute SQL from a file, return results."""
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
        except:
            return None


def cleanup_view(conn, view_name):
    """Drop a view if it exists."""
    with conn.cursor() as cursor:
        cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
        conn.commit()


def cleanup_procedure(conn, proc_name):
    """Drop a procedure if it exists."""
    with conn.cursor() as cursor:
        cursor.execute(f"DROP PROCEDURE IF EXISTS {proc_name}")
        conn.commit()


def cleanup_trigger(conn, trigger_name):
    """Drop a trigger if it exists."""
    with conn.cursor() as cursor:
        cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name}")
        conn.commit()
