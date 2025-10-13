import os, pandas as pd
import sqlalchemy as sa
from sqlalchemy import text
from datetime import datetime

DB_URL = os.getenv("DB_URL", "mysql+pymysql://root:secret@mariadb:3306/vg")
CSV_PATH = os.getenv("CSV_PATH", "data/rawg_games.csv")
SEP = "||"  # séparateur de listes dans le CSV Kaggle (jummyegg)

def parse_list(val):
    if pd.isna(val) or not str(val).strip():
        return []
    return [x.strip() for x in str(val).split(SEP) if x.strip()]

def to_date(s):
    s = str(s).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            pass
    return None

def main():
    eng = sa.create_engine(DB_URL, pool_pre_ping=True)
    with eng.begin() as conn:
        chunks = pd.read_csv(CSV_PATH, chunksize=5000)
        # print(chunks)
        for df in chunks:
            print(df)
            cols = {c.lower(): c for c in df.columns}
            get = lambda k: cols.get(k)
            for _, r in df.iterrows():
                name = str(r[get("name")]).strip() if get("name") else None
                if not name:
                    continue
                released = to_date(r[get("released")]) if get("released") else None
                year = released.year if released else None
                metacritic = int(r[get("metacritic")]) if get("metacritic") and pd.notna(r[get("metacritic")]) else None
                rating = float(r[get("rating")]) if get("rating") and pd.notna(r[get("rating")]) else None
                ratings_count = int(r[get("ratings_count")]) if get("ratings_count") and pd.notna(r[get("ratings_count")]) else None
                esrb = str(r[get("esrb_rating")]).strip() if get("esrb_rating") and pd.notna(r[get("esrb_rating")]) else None
                rawg_id = int(r[get("id")]) if get("id") and pd.notna(r[get("id")]) else None
                playtime = int(r[get("playtime")]) if get("playtime") and pd.notna(r[get("playtime")]) else None

                res = conn.execute(text(
                    """
                    INSERT INTO games(rawg_id, name, released, year, metacritic, rating, ratings_count, playtime, esrb)
                    VALUES(:rid,:n,:rel,:y,:m,:r,:rc,:pt,:esrb)
                    """
                ), dict(rid=rawg_id, n=name, rel=released, y=year, m=metacritic, r=rating, rc=ratings_count, pt=playtime, esrb=esrb))
                # print(res.lastrowid)
                game_id = res.lastrowid
                if not game_id:
                    game_id = conn.execute(text(
                        "SELECT id FROM games WHERE name=:n AND ((released=:rel) OR (released IS NULL AND :rel IS NULL)) ORDER BY id DESC LIMIT 1"
                    ), {"n": name, "rel": released}).scalar()

                def upsert_many(table, key, values, link_table, link_fk):
                    for v in values:
                        obj_id = conn.execute(text(f"SELECT id FROM {table} WHERE {key}=:v"), {"v": v}).scalar()
                        if not obj_id:
                            obj_id = conn.execute(text(f"INSERT INTO {table}({key}) VALUES(:v)"), {"v": v}).lastrowid
                        conn.execute(text(f"INSERT IGNORE INTO {link_table}(game_id, {link_fk}) VALUES(:g,:o)"),
                                     {"g": game_id, "o": obj_id})

                platforms = parse_list(r.get(get("platforms"))) if get("platforms") else []
                genres    = parse_list(r.get(get("genres"))) if get("genres") else []
                publishers= parse_list(r.get(get("publishers"))) if get("publishers") else []
                developers= parse_list(r.get(get("developers"))) if get("developers") else []
                tags      = parse_list(r.get(get("tags"))) if get("tags") else []

                upsert_many("platforms","code", platforms, "game_platforms","platform_id")
                upsert_many("genres","name", genres, "game_genres","genre_id")
                upsert_many("publishers","name", publishers, "game_publishers","publisher_id")
                upsert_many("developers","name", developers, "game_developers","developer_id")
                upsert_many("tags","name", tags, "game_tags","tag_id")

    print("Import RAWG (Kaggle) terminé ✅")

if __name__ == "__main__":
    main()
