import pytest
from .helpers import run_sql_file, MissingQueryError

def test_limit_offset(conn):
    """Test: LIMIT avec OFFSET (pagination page 2)"""
    try:
        rows = run_sql_file(conn, "sql/queries/q00f_limit_offset.sql")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")

    # Doit retourner exactement 10 lignes (page 2 avec 10 par page)
    assert len(rows) == 10, f"Attendu 10 lignes (LIMIT 10), obtenu {len(rows)}"

    # Tous les scores doivent être >= 80
    for row in rows:
        assert row.metacritic >= 80, f"Metacritic doit être >= 80, obtenu {row.metacritic}"

    # Vérifier le tri par metacritic DESC
    if len(rows) > 1:
        for i in range(len(rows) - 1):
            curr = rows[i]
            next_row = rows[i + 1]
            if curr.metacritic != next_row.metacritic:
                assert curr.metacritic >= next_row.metacritic, "Tri metacritic DESC non respecté"
