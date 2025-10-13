import pytest
from .helpers import run_sql_file, MissingQueryError

def test_common_mistakes_fix(conn):
    try:
        rows = run_sql_file(conn, "../sql/queries/q20_common_mistakes_fix.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    assert hasattr(rows[0], "genre") and hasattr(rows[0], "n_games") and hasattr(rows[0], "meta_avg")
