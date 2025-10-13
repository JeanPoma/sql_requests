import pytest
from .helpers import run_sql_file, MissingQueryError

def test_top3_per_year_windows(conn):
    try:
        rows = run_sql_file(conn, "s../ql/queries/q05_top3_per_year_windows.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    assert all(1 <= r.rnk <= 3 for r in rows)
