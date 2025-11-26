"""
Tests pour les exercices avancés sur les triggers (t01-t06)
"""
import pytest
import pymysql
from tests.conftest import MissingQueryError
from tests.test_advanced.conftest import (
    execute_sql_file,
    cleanup_trigger,
)


def test_t01_validate_game_insert_trigger(conn):
    """
    Test t01: Trigger BEFORE INSERT qui valide les données
    """
    trigger_name = 'trg_validate_game_insert'
    cleanup_trigger(conn, trigger_name)

    try:
        # Créer le trigger
        execute_sql_file(conn, 'sql/advanced/triggers/t01_validate_game_insert.sql')

        # Vérifier que le trigger existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TRIGGERS
                WHERE TRIGGER_SCHEMA = DATABASE()
                AND TRIGGER_NAME = %s
            """, (trigger_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"Le trigger {trigger_name} n'a pas été créé"

        # Test 1: Insertion valide (devrait réussir)
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO games (name, year, metacritic, slug)
                VALUES ('Valid Test Game', 2023, 85, 'valid-test-game-trigger-t01')
            """)
            conn.commit()
            # Si on arrive ici, l'insertion a réussi (bon signe)

        # Test 2: Nom vide (devrait échouer)
        with pytest.raises(pymysql.err.InternalError) as exc_info:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO games (name, year, metacritic, slug)
                    VALUES ('', 2023, 85, 'empty-name-trigger-t01')
                """)
                conn.commit()

        # Vérifier le message d'erreur
        error_msg = str(exc_info.value).lower()
        assert 'game name' in error_msg or 'empty' in error_msg, \
            f"Le message d'erreur devrait mentionner 'game name' ou 'empty', obtenu: {exc_info.value}"

        conn.rollback()

        # Test 3: Année invalide (trop ancienne) (devrait échouer)
        with pytest.raises(pymysql.err.InternalError) as exc_info:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO games (name, year, metacritic, slug)
                    VALUES ('Old Game', 1800, 85, 'old-game-trigger-t01')
                """)
                conn.commit()

        error_msg = str(exc_info.value).lower()
        assert 'year' in error_msg or 'année' in error_msg or 'invalid' in error_msg, \
            f"Le message d'erreur devrait mentionner 'year' ou 'invalid', obtenu: {exc_info.value}"

        conn.rollback()

        # Test 4: Score Metacritic invalide (devrait échouer)
        with pytest.raises(pymysql.err.InternalError) as exc_info:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO games (name, year, metacritic, slug)
                    VALUES ('High Score Game', 2023, 150, 'high-score-trigger-t01')
                """)
                conn.commit()

        error_msg = str(exc_info.value).lower()
        assert 'metacritic' in error_msg or 'score' in error_msg, \
            f"Le message d'erreur devrait mentionner 'metacritic' ou 'score', obtenu: {exc_info.value}"

        conn.rollback()

    except FileNotFoundError:
        pytest.skip("Fichier t01_validate_game_insert.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        conn.rollback()
        cleanup_trigger(conn, trigger_name)


def test_t02_audit_game_insert_trigger(conn):
    """
    Test t02: Trigger AFTER INSERT qui enregistre dans un audit log
    """
    trigger_name = 'trg_audit_game_insert'
    cleanup_trigger(conn, trigger_name)

    try:
        # Créer le trigger (et la table games_audit)
        execute_sql_file(conn, 'sql/advanced/triggers/t02_audit_game_insert.sql')

        # Vérifier que le trigger existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TRIGGERS
                WHERE TRIGGER_SCHEMA = DATABASE()
                AND TRIGGER_NAME = %s
            """, (trigger_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"Le trigger {trigger_name} n'a pas été créé"

        # Vérifier que la table games_audit existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'games_audit'
            """)
            result = cursor.fetchone()
            assert result['cnt'] == 1, "La table games_audit doit être créée"

        # Compter les entrées d'audit avant
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM games_audit")
            before_count = cursor.fetchone()['cnt']

        # Insérer un jeu
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO games (name, year, slug)
                VALUES ('Audited Game', 2023, 'audited-game-trigger-t02')
            """)
            inserted_id = cursor.lastrowid
            conn.commit()

        # Vérifier qu'une entrée a été ajoutée dans games_audit
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM games_audit")
            after_count = cursor.fetchone()['cnt']
            assert after_count == before_count + 1, \
                "Une entrée devrait avoir été ajoutée dans games_audit"

        # Vérifier le contenu de l'audit
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT game_id, game_name, operation, operation_time
                FROM games_audit
                WHERE game_id = %s
                ORDER BY operation_time DESC
                LIMIT 1
            """, (inserted_id,))
            audit_row = cursor.fetchone()

            assert audit_row is not None, "L'audit devrait contenir une entrée pour ce jeu"
            assert audit_row['game_id'] == inserted_id, \
                f"L'audit devrait avoir le bon game_id: {inserted_id}"
            assert audit_row['game_name'] == 'Audited Game', \
                "L'audit devrait avoir le bon nom de jeu"
            assert audit_row['operation'] == 'INSERT', \
                "L'audit devrait indiquer l'opération INSERT"
            assert audit_row['operation_time'] is not None, \
                "L'audit devrait avoir une date/heure"

    except FileNotFoundError:
        pytest.skip("Fichier t02_audit_game_insert.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        conn.rollback()
        # Nettoyer la table games_audit
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS games_audit")
            conn.commit()
        cleanup_trigger(conn, trigger_name)


def test_t03_track_game_updates_trigger(conn):
    """
    Test t03: Trigger BEFORE UPDATE qui enregistre l'historique
    """
    trigger_name = 'trg_track_game_updates'
    cleanup_trigger(conn, trigger_name)

    try:
        # Créer le trigger (et la table games_history)
        execute_sql_file(conn, 'sql/advanced/triggers/t03_track_game_updates.sql')

        # Vérifier que le trigger existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TRIGGERS
                WHERE TRIGGER_SCHEMA = DATABASE()
                AND TRIGGER_NAME = %s
            """, (trigger_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"Le trigger {trigger_name} n'a pas été créé"

        # Vérifier que la table games_history existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'games_history'
            """)
            result = cursor.fetchone()
            assert result['cnt'] == 1, "La table games_history doit être créée"

        # Trouver un jeu existant
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, metacritic
                FROM games
                WHERE metacritic IS NOT NULL
                LIMIT 1
            """)
            game = cursor.fetchone()

            if not game:
                pytest.skip("Aucun jeu avec metacritic disponible pour le test")

            game_id = game['id']
            old_score = game['metacritic']
            new_score = 88 if old_score != 88 else 89

        # Compter les entrées d'historique avant
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM games_history WHERE game_id = %s", (game_id,))
            before_count = cursor.fetchone()['cnt']

        # Mettre à jour le jeu
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE games
                SET metacritic = %s
                WHERE id = %s
            """, (new_score, game_id))
            conn.commit()

        # Vérifier qu'une entrée a été ajoutée dans games_history
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM games_history WHERE game_id = %s", (game_id,))
            after_count = cursor.fetchone()['cnt']
            assert after_count == before_count + 1, \
                "Une entrée devrait avoir été ajoutée dans games_history"

        # Vérifier le contenu de l'historique
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT old_metacritic, new_metacritic, changed_at
                FROM games_history
                WHERE game_id = %s
                ORDER BY changed_at DESC
                LIMIT 1
            """, (game_id,))
            history_row = cursor.fetchone()

            assert history_row is not None, "L'historique devrait contenir une entrée"
            assert history_row['old_metacritic'] == old_score, \
                f"L'historique devrait avoir l'ancien score: {old_score}"
            assert history_row['new_metacritic'] == new_score, \
                f"L'historique devrait avoir le nouveau score: {new_score}"
            assert history_row['changed_at'] is not None, \
                "L'historique devrait avoir une date/heure"

    except FileNotFoundError:
        pytest.skip("Fichier t03_track_game_updates.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        conn.rollback()
        # Nettoyer la table games_history
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS games_history")
            conn.commit()
        cleanup_trigger(conn, trigger_name)


def test_t04_notify_high_score_trigger(conn):
    """
    Test t04: Trigger AFTER UPDATE qui crée des notifications
    """
    trigger_name = 'trg_notify_high_score'
    cleanup_trigger(conn, trigger_name)

    try:
        # Créer le trigger (et la table notifications)
        execute_sql_file(conn, 'sql/advanced/triggers/t04_notify_high_score.sql')

        # Vérifier que le trigger existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TRIGGERS
                WHERE TRIGGER_SCHEMA = DATABASE()
                AND TRIGGER_NAME = %s
            """, (trigger_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"Le trigger {trigger_name} n'a pas été créé"

        # Vérifier que la table notifications existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'notifications'
            """)
            result = cursor.fetchone()
            assert result['cnt'] == 1, "La table notifications doit être créée"

        # Trouver un jeu avec un score < 95 ou NULL
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, metacritic
                FROM games
                WHERE metacritic < 95 OR metacritic IS NULL
                LIMIT 1
            """)
            game = cursor.fetchone()

            if not game:
                pytest.skip("Aucun jeu avec score < 95 disponible pour le test")

            game_id = game['id']
            game_name = game['name']

        # Compter les notifications avant
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM notifications")
            before_count = cursor.fetchone()['cnt']

        # Mettre à jour le jeu pour atteindre un score >= 95
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE games
                SET metacritic = 96
                WHERE id = %s
            """, (game_id,))
            conn.commit()

        # Vérifier qu'une notification a été créée
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM notifications")
            after_count = cursor.fetchone()['cnt']
            assert after_count == before_count + 1, \
                "Une notification devrait avoir été créée"

        # Vérifier le contenu de la notification
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT game_id, game_name, message, created_at
                FROM notifications
                WHERE game_id = %s
                ORDER BY created_at DESC
                LIMIT 1
            """, (game_id,))
            notif = cursor.fetchone()

            assert notif is not None, "La notification devrait exister"
            assert notif['game_id'] == game_id, "La notification devrait avoir le bon game_id"
            assert '96' in str(notif['message']) or 'high' in notif['message'].lower(), \
                f"Le message devrait mentionner le score ou 'high', obtenu: {notif['message']}"

    except FileNotFoundError:
        pytest.skip("Fichier t04_notify_high_score.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        conn.rollback()
        # Nettoyer la table notifications
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS notifications")
            conn.commit()
        cleanup_trigger(conn, trigger_name)


def test_t05_prevent_delete_popular_trigger(conn):
    """
    Test t05: Trigger BEFORE DELETE qui empêche la suppression
    """
    trigger_name = 'trg_prevent_delete_popular'
    cleanup_trigger(conn, trigger_name)

    try:
        # Créer le trigger
        execute_sql_file(conn, 'sql/advanced/triggers/t05_prevent_delete_popular.sql')

        # Vérifier que le trigger existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TRIGGERS
                WHERE TRIGGER_SCHEMA = DATABASE()
                AND TRIGGER_NAME = %s
            """, (trigger_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"Le trigger {trigger_name} n'a pas été créé"

        # Test 1: Trouver un jeu populaire (ratings_count > 1000)
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, ratings_count
                FROM games
                WHERE ratings_count > 1000
                LIMIT 1
            """)
            popular_game = cursor.fetchone()

            if popular_game:
                game_id = popular_game['id']

                # Essayer de supprimer (devrait échouer)
                with pytest.raises(pymysql.err.InternalError) as exc_info:
                    cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
                    conn.commit()

                error_msg = str(exc_info.value).lower()
                assert 'popular' in error_msg or 'ratings' in error_msg or 'cannot delete' in error_msg, \
                    f"Le message d'erreur devrait mentionner 'popular' ou 'cannot delete', obtenu: {exc_info.value}"

                conn.rollback()

        # Test 2: Trouver un jeu peu populaire (ratings_count <= 1000)
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, ratings_count
                FROM games
                WHERE ratings_count <= 1000 OR ratings_count IS NULL
                LIMIT 1
            """)
            unpopular_game = cursor.fetchone()

            if unpopular_game:
                game_id = unpopular_game['id']

                # Essayer de supprimer (devrait réussir)
                cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
                # Si on arrive ici sans erreur, la suppression a réussi
                conn.rollback()  # Ne pas vraiment supprimer

    except FileNotFoundError:
        pytest.skip("Fichier t05_prevent_delete_popular.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        conn.rollback()
        cleanup_trigger(conn, trigger_name)


def test_t06_maintain_genre_stats_trigger(conn):
    """
    Test t06: Trigger pour maintenir une vue matérialisée
    """
    trigger_name = 'trg_maintain_genre_stats_insert'
    cleanup_trigger(conn, trigger_name)

    try:
        # Créer le trigger (et la table genre_stats)
        execute_sql_file(conn, 'sql/advanced/triggers/t06_maintain_genre_stats.sql')

        # Vérifier que le trigger existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TRIGGERS
                WHERE TRIGGER_SCHEMA = DATABASE()
                AND TRIGGER_NAME = %s
            """, (trigger_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"Le trigger {trigger_name} n'a pas été créé"

        # Vérifier que la table genre_stats existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'genre_stats'
            """)
            result = cursor.fetchone()
            assert result['cnt'] == 1, "La table genre_stats doit être créée"

        # Trouver un genre et un jeu
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM genres LIMIT 1")
            genre = cursor.fetchone()
            if not genre:
                pytest.skip("Aucun genre disponible pour le test")

            genre_id = genre['id']

            cursor.execute("SELECT id FROM games WHERE metacritic IS NOT NULL LIMIT 1")
            game = cursor.fetchone()
            if not game:
                pytest.skip("Aucun jeu avec metacritic disponible pour le test")

            game_id = game['id']

        # Vérifier les stats avant (ou NULL)
        with conn.cursor() as cursor:
            cursor.execute("SELECT total_games FROM genre_stats WHERE genre_id = %s", (genre_id,))
            before = cursor.fetchone()
            before_total = before['total_games'] if before else 0

        # Ajouter le jeu au genre (trigger devrait se déclencher)
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO game_genres (game_id, genre_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE game_id = game_id
            """, (game_id, genre_id))
            conn.commit()

        # Vérifier que genre_stats a été mis à jour
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT genre_id, total_games, avg_metacritic, last_updated
                FROM genre_stats
                WHERE genre_id = %s
            """, (genre_id,))
            stats = cursor.fetchone()

            assert stats is not None, "Les stats devraient être créées ou mises à jour"
            assert stats['total_games'] > 0, "Le total de jeux devrait être > 0"
            assert stats['avg_metacritic'] is not None, "La moyenne devrait être calculée"
            assert 0 <= stats['avg_metacritic'] <= 100, \
                f"La moyenne devrait être entre 0 et 100, obtenu {stats['avg_metacritic']}"
            assert stats['last_updated'] is not None, "La date de mise à jour devrait être renseignée"

    except FileNotFoundError:
        pytest.skip("Fichier t06_maintain_genre_stats.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        conn.rollback()
        # Nettoyer la table genre_stats
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS genre_stats")
            conn.commit()
        cleanup_trigger(conn, trigger_name)
