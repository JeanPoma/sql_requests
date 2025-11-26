import pytest
from .helpers import run_sql_file, MissingQueryError

def test_aggregates_basic(conn):
    """Test: Agrégats AVG, MIN, MAX, COUNT"""
    try:
        rows = run_sql_file(conn, "sql/queries/q00h_aggregates_basic.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")

    # Doit retourner exactement 1 ligne (résultat d'agrégats)
    assert len(rows) == 1, f"Les agrégats doivent retourner 1 ligne, obtenu {len(rows)}"

    result = rows[0]

    # Vérifier que toutes les colonnes existent avec les bons noms
    assert hasattr(result, 'avg_score'), "Colonne 'avg_score' manquante"
    assert hasattr(result, 'min_score'), "Colonne 'min_score' manquante"
    assert hasattr(result, 'max_score'), "Colonne 'max_score' manquante"
    assert hasattr(result, 'total_games'), "Colonne 'total_games' manquante"

    # Vérifier la cohérence des valeurs
    assert 0 <= result.min_score <= 100, f"min_score doit être entre 0 et 100"
    assert 0 <= result.max_score <= 100, f"max_score doit être entre 0 et 100"
    assert result.min_score <= result.avg_score <= result.max_score, \
        f"Incohérence: min({result.min_score}) <= avg({result.avg_score}) <= max({result.max_score})"
    assert result.total_games > 0, "Le nombre de jeux doit être > 0"

    # Vérifier que avg_score est bien arrondi à 2 décimales
    avg_str = str(float(result.avg_score))
    if '.' in avg_str:
        decimals = len(avg_str.split('.')[1])
        assert decimals <= 2, f"avg_score doit être arrondi à 2 décimales max, obtenu {decimals}"
