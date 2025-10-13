import pytest
from .helpers import run_sql_file, MissingQueryError

def test_genre_platform_score(conn):
    try:
        rows = run_sql_file(conn, "sql/queries/q03_genre_platform_score.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    assert hasattr(rows[0], "genre") and hasattr(rows[0], "platform")
    assert hasattr(rows[0], "meta_avg") and hasattr(rows[0], "n_games")
