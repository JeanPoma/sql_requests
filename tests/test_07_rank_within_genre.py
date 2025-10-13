import pytest
from .helpers import run_sql_file, MissingQueryError

def test_rank_within_genre(conn):
    try:
        rows = run_sql_file(conn, "../sql/queries/q07_rank_within_genre.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    assert all(getattr(r, "rnk", 0) >= 1 for r in rows)
