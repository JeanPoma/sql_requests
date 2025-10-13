import pytest
from .helpers import run_sql_file, MissingQueryError

def test_duplicates_detection(conn):
    try:
        rows = run_sql_file(conn, "sql/queries/q14_duplicates_detection.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows is not None
