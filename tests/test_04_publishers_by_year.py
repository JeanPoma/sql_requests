import pytest
from .helpers import run_sql_file, MissingQueryError

def test_publishers_by_year(conn):
    try:
        rows = run_sql_file(conn, "sql/queries/q04_publishers_by_year.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    assert all(r.year is not None for r in rows)
