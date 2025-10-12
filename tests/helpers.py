from sqlalchemy import text

class MissingQueryError(AssertionError):
    pass

def run_sql_file(conn, path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read().strip()
    if not sql or sql.startswith("-- CONSIGNE") or sql.startswith("-- CHALLENGE"):
        raise MissingQueryError(f"Le fichier {path} ne contient pas encore de requête SQL.")
    return conn.execute(text(sql)).fetchall()
