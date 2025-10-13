import pytest
from sqlalchemy import text
from .helpers import run_sql_file, MissingQueryError

def test_subquery_vs_join(conn):
    try:
        rows_b = run_sql_file(conn, "../sql/queries/q11_subquery_vs_join.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows_b
    rows_a = conn.execute(text("""
        SELECT d.name AS developer, MAX(g.metacritic) AS max_meta
        FROM developers d
        JOIN game_developers gd ON gd.developer_id=d.id
        JOIN games g ON g.id=gd.game_id
        GROUP BY d.name
        ORDER BY max_meta DESC, d.name ASC
        LIMIT 20
        """)).fetchall()
    assert rows_a[:5] == rows_b[:5]
