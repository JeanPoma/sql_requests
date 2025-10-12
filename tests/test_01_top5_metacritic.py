import pytest
from .helpers import run_sql_file, MissingQueryError

def test_top5_metacritic(conn):
    try:
        rows = run_sql_file(conn, "sql/queries/q01_top5_metacritic.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert len(rows) == 5
    metas = [r.metacritic for r in rows]
    assert metas == sorted(metas, reverse=True)
