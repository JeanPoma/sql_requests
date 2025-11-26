import pytest
from .helpers import run_sql_file, MissingQueryError

def test_where_simple(conn):
    """Test: WHERE avec condition simple (year = 2020)"""
    try:
        rows = run_sql_file(conn, "sql/queries/q00c_where_simple.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")

    # Doit retourner au maximum 15 lignes
    assert len(rows) <= 15, f"LIMIT 15 attendu, obtenu {len(rows)} lignes"

    # Tous les jeux doivent être de l'année 2020
    for row in rows:
        assert row.year == 2020, f"Attendu year=2020, obtenu {row.year} pour {row.name}"

    # Vérifier que le tri par metacritic DESC est respecté
    if len(rows) > 1:
        metacritics = [r.metacritic for r in rows if r.metacritic is not None]
        assert metacritics == sorted(metacritics, reverse=True), "Le tri par metacritic DESC n'est pas respecté"
