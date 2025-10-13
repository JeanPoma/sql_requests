import pytest
from .helpers import run_sql_file, MissingQueryError

def test_union_compare_platforms(conn):
    try:
        rows = run_sql_file(conn, "../sql/queries/q12_union_compare_platforms.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    groups = set(r.platform_group for r in rows)
    assert {"PC", "PlayStation"} & groups
