import pytest
from .helpers import run_sql_file, MissingQueryError

def test_tags_popularity(conn):
    try:
        rows = run_sql_file(conn, "sql/queries/q09_tags_popularity.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    assert hasattr(rows[0], "tag") and hasattr(rows[0], "n_games")
