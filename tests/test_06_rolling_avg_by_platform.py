import pytest
from .helpers import run_sql_file, MissingQueryError

def test_rolling_avg_by_platform(conn):
    try:
        rows = run_sql_file(conn, "sql/queries/q06_rolling_avg_by_platform.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    row = rows[0]
    assert hasattr(row, "platform") and hasattr(row, "year") and hasattr(row, "meta_avg_roll")
