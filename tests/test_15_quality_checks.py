import pytest
from .helpers import run_sql_file, MissingQueryError

def test_quality_checks(conn):
    try:
        rows = run_sql_file(conn, "../sql/queries/q15_quality_checks.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
