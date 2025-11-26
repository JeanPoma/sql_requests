import pytest
from .helpers import run_sql_file, MissingQueryError

def test_select_all_games(conn):
    """Test: SELECT simple avec toutes les colonnes et LIMIT"""
    try:
        rows = run_sql_file(conn, "sql/queries/q00a_select_all_games.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")

    # Doit retourner exactement 10 lignes
    assert len(rows) == 10, f"Attendu 10 lignes, obtenu {len(rows)}"

    # Vérifier qu'on a bien toutes les colonnes importantes
    first_row = rows[0]
    required_attrs = ['id', 'name', 'year', 'metacritic']
    for attr in required_attrs:
        assert hasattr(first_row, attr), f"Colonne manquante: {attr}"
