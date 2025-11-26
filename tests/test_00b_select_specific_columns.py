import pytest
from .helpers import run_sql_file, MissingQueryError

def test_select_specific_columns(conn):
    """Test: SELECT avec colonnes spécifiques"""
    try:
        rows = run_sql_file(conn, "sql/queries/q00b_select_specific_columns.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")

    # Doit retourner exactement 20 lignes
    assert len(rows) == 20, f"Attendu 20 lignes, obtenu {len(rows)}"

    # Vérifier qu'on a uniquement les 3 colonnes demandées
    first_row = rows[0]
    assert hasattr(first_row, 'name'), "Colonne 'name' manquante"
    assert hasattr(first_row, 'year'), "Colonne 'year' manquante"
    assert hasattr(first_row, 'metacritic'), "Colonne 'metacritic' manquante"
