from sqlalchemy import text

def test_dataset_non_vide(conn):
    n = conn.execute(text("SELECT COUNT(*) FROM games")).scalar()
    assert n and n > 1000, "Le dataset semble vide ou trop petit. Avez-vous importé le CSV?"
