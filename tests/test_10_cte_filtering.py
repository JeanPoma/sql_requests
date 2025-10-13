import pytest
from .helpers import run_sql_file, MissingQueryError

def test_cte_filtering(conn):
    try:
        rows = run_sql_file(conn, "../sql/queries/q10_cte_filtering.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    assert all(r.ratings_count >= 1000 for r in rows)
