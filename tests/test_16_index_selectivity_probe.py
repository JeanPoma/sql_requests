import pytest
from .helpers import run_sql_file, MissingQueryError

def test_index_selectivity_probe(conn):
    try:
        rows = run_sql_file(conn, "sql/queries/q16_index_selectivity_probe.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
