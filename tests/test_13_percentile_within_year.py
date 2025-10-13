import pytest
from .helpers import run_sql_file, MissingQueryError

def test_percentile_within_year(conn):
    try:
        rows = run_sql_file(conn, "../sql/queries/q13_percentile_within_year.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    assert all(0 <= r.p90 <= 100 for r in rows)
