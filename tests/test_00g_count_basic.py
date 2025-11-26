import pytest
from .helpers import run_sql_file, MissingQueryError

def test_count_basic(conn):
    """Test: COUNT basique (compter les jeux avec score)"""
    try:
        rows = run_sql_file(conn, "sql/queries/q00g_count_basic.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")

    # Doit retourner exactement 1 ligne (résultat d'agrégat)
    assert len(rows) == 1, f"Un agrégat doit retourner 1 ligne, obtenu {len(rows)}"

    result = rows[0]

    # Vérifier que la colonne existe (total_games_with_score)
    assert hasattr(result, 'total_games_with_score'), "Colonne 'total_games_with_score' manquante (utilisez AS)"

    # Le nombre doit être positif
    count = result.total_games_with_score
    assert count > 0, f"Le nombre de jeux avec score doit être > 0, obtenu {count}"
    assert isinstance(count, int), f"Le résultat doit être un entier, obtenu {type(count)}"
