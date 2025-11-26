import pytest
from .helpers import run_sql_file, MissingQueryError

def test_order_by(conn):
    """Test: ORDER BY multi-colonnes (metacritic DESC, ratings_count DESC, name ASC)"""
    try:
        rows = run_sql_file(conn, "sql/queries/q00e_order_by.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")

    # Doit retourner au maximum 25 lignes
    assert len(rows) <= 25, f"LIMIT 25 attendu, obtenu {len(rows)} lignes"
    assert len(rows) > 0, "Aucune ligne retournée"

    # Tous les jeux doivent avoir un metacritic non NULL
    for row in rows:
        assert row.metacritic is not None, f"Metacritic ne doit pas être NULL pour {row.name}"

    # Vérifier le tri: metacritic DESC en priorité
    if len(rows) > 1:
        metacritics = [r.metacritic for r in rows]
        assert metacritics == sorted(metacritics, reverse=True), "Le tri par metacritic DESC n'est pas correct"
