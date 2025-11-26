import pytest
from .helpers import run_sql_file, MissingQueryError

def test_where_and_or(conn):
    """Test: WHERE avec AND et OR (années 2019/2020/2021 ET metacritic >= 85)"""
    try:
        rows = run_sql_file(conn, "sql/queries/q00d_where_and_or.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")

    # Doit retourner au maximum 20 lignes
    assert len(rows) <= 20, f"LIMIT 20 attendu, obtenu {len(rows)} lignes"

    # Vérifier les conditions
    for row in rows:
        assert row.year in [2019, 2020, 2021], f"Year doit être 2019, 2020 ou 2021, obtenu {row.year}"
        assert row.metacritic >= 85, f"Metacritic doit être >= 85, obtenu {row.metacritic}"

    # Vérifier le tri: metacritic DESC puis ratings_count DESC
    if len(rows) > 1:
        for i in range(len(rows) - 1):
            curr = rows[i]
            next_row = rows[i + 1]
            # Si metacritic différent, doit être décroissant
            if curr.metacritic != next_row.metacritic:
                assert curr.metacritic > next_row.metacritic, "Tri metacritic DESC non respecté"
