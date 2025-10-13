import pytest
from .helpers import run_sql_file, MissingQueryError

def test_best_devs_by_decade(conn):
    try:
        rows = run_sql_file(conn, "../sql/queries/q08_best_devs_by_decade.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    assert hasattr(rows[0], "decade")
