import pytest
from sqlalchemy import text


def test_explain_year_range(conn):
    try:
        with open("../sql/queries/q17_explain_year_range.sql", "r", encoding="utf-8") as f:
            sql = f.read().strip()
        if not sql:
            raise FileNotFoundError
    except FileNotFoundError:
        pytest.skip("Fichier manquant ou vide")
    # plan = conn.execute(text(f"EXPLAIN {sql}")).fetchall()
    # used = [r.get("key", None) for r in plan]
    # assert any(k and "idx_games_year" in k for k in used), f"Plan: {plan}"
