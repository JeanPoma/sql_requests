import pytest
from .helpers import run_sql_file, MissingQueryError

def test_gaps_and_islands_years(conn):
    try:
        rows = run_sql_file(conn, "../sql/queries/q19_gaps_and_islands_years.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    assert rows
    r = rows[0]
    assert hasattr(r, "start_year") and hasattr(r, "end_year") and hasattr(r, "span_years")
