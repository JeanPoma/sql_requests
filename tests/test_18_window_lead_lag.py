import pytest
from .helpers import run_sql_file, MissingQueryError

def test_window_lead_lag(conn):
    try:
        rows = run_sql_file(conn, "../sql/queries/q18_window_lead_lag.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    row = rows[0]
    assert hasattr(row, "prev_meta") and hasattr(row, "diff_meta")
