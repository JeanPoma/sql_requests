import pytest
from .helpers import run_sql_file, MissingQueryError

def test_top10_recent_highscore(conn):
    try:
        rows = run_sql_file(conn, "sql/queries/q02_top10_recent_highscore.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert len(rows) == 10
    assert all(r.year >= 2015 for r in rows)
    metas = [r.metacritic for r in rows]
    assert metas == sorted(metas, reverse=True)
