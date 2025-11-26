"""
Tests pour les exercices avancés sur les procédures stockées (p01-p06)
"""
import pytest
import pymysql
from tests.conftest import MissingQueryError
from tests.test_advanced.conftest import (
    execute_sql_file,
    cleanup_procedure,
)


def test_p01_cleanup_old_data_procedure(conn):
    """
    Test p01: Procédure simple sans paramètres qui nettoie les vieux jeux
    """
    proc_name = 'sp_cleanup_old_data'
    cleanup_procedure(conn, proc_name)

    try:
        # Créer la procédure
        execute_sql_file(conn, 'sql/advanced/procedures/p01_cleanup_old_data.sql')

        # Vérifier que la procédure existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.ROUTINES
                WHERE ROUTINE_SCHEMA = DATABASE()
                AND ROUTINE_NAME = %s
                AND ROUTINE_TYPE = 'PROCEDURE'
            """, (proc_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"La procédure {proc_name} n'a pas été créée"

        # Compter les jeux qui correspondent aux critères AVANT l'appel
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM games
                WHERE year < 1990
                AND ratings_count < 10
                AND metacritic IS NOT NULL
            """)
            before_count = cursor.fetchone()['cnt']

        # Appeler la procédure
        with conn.cursor() as cursor:
            cursor.execute(f"CALL {proc_name}()")
            # La procédure retourne ROW_COUNT()
            result = cursor.fetchone()

            # Vérifier que le résultat contient 'rows_affected'
            assert 'rows_affected' in result or 'ROW_COUNT()' in result, \
                "La procédure doit retourner ROW_COUNT() AS rows_affected"

            rows_affected = result.get('rows_affected') or result.get('ROW_COUNT()')

            # Le nombre de lignes affectées doit correspondre au comptage
            assert rows_affected == before_count, \
                f"Expected {before_count} rows affected, got {rows_affected}"

        # Vérifier qu'il n'y a plus de jeux correspondant aux critères
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM games
                WHERE year < 1990
                AND ratings_count < 10
                AND metacritic IS NOT NULL
            """)
            after_count = cursor.fetchone()['cnt']
            assert after_count == 0, \
                "Tous les jeux anciens avec peu de ratings devraient avoir metacritic = NULL"

        conn.commit()

    except FileNotFoundError:
        pytest.skip("Fichier p01_cleanup_old_data.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        # Restaurer les données (rollback implicite par cleanup)
        conn.rollback()
        cleanup_procedure(conn, proc_name)


def test_p02_get_games_by_score_procedure(conn):
    """
    Test p02: Procédure avec paramètre IN qui recherche des jeux par score
    """
    proc_name = 'sp_get_games_by_score'
    cleanup_procedure(conn, proc_name)

    try:
        # Créer la procédure
        execute_sql_file(conn, 'sql/advanced/procedures/p02_get_games_by_score.sql')

        # Vérifier que la procédure existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.ROUTINES
                WHERE ROUTINE_SCHEMA = DATABASE()
                AND ROUTINE_NAME = %s
                AND ROUTINE_TYPE = 'PROCEDURE'
            """, (proc_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"La procédure {proc_name} n'a pas été créée"

        # Tester avec un score de 90
        with conn.cursor() as cursor:
            cursor.execute(f"CALL {proc_name}(90)")
            results = cursor.fetchall()

            # Vérifier qu'on a des résultats
            assert len(results) > 0, "Devrait retourner des jeux avec score >= 90"
            assert len(results) <= 20, "Ne devrait pas retourner plus de 20 résultats"

            # Vérifier que toutes les colonnes attendues sont présentes
            assert 'name' in results[0], "La colonne 'name' doit être présente"
            assert 'year' in results[0], "La colonne 'year' doit être présente"
            assert 'metacritic' in results[0], "La colonne 'metacritic' doit être présente"

            # Vérifier que tous les scores sont >= 90
            for row in results:
                assert row['metacritic'] >= 90, \
                    f"Tous les scores devraient être >= 90, trouvé {row['metacritic']}"

            # Vérifier l'ordre décroissant
            scores = [row['metacritic'] for row in results]
            assert scores == sorted(scores, reverse=True), \
                "Les résultats devraient être triés par metacritic DESC"

        # Tester avec un score de 95 (plus sélectif)
        with conn.cursor() as cursor:
            cursor.execute(f"CALL {proc_name}(95)")
            results = cursor.fetchall()

            # Tous les scores doivent être >= 95
            for row in results:
                assert row['metacritic'] >= 95, \
                    f"Tous les scores devraient être >= 95, trouvé {row['metacritic']}"

    except FileNotFoundError:
        pytest.skip("Fichier p02_get_games_by_score.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        cleanup_procedure(conn, proc_name)


def test_p03_calculate_genre_stats_procedure(conn):
    """
    Test p03: Procédure avec paramètres OUT qui calcule des statistiques
    """
    proc_name = 'sp_calculate_genre_stats'
    cleanup_procedure(conn, proc_name)

    try:
        # Créer la procédure
        execute_sql_file(conn, 'sql/advanced/procedures/p03_calculate_genre_stats.sql')

        # Vérifier que la procédure existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.ROUTINES
                WHERE ROUTINE_SCHEMA = DATABASE()
                AND ROUTINE_NAME = %s
                AND ROUTINE_TYPE = 'PROCEDURE'
            """, (proc_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"La procédure {proc_name} n'a pas été créée"

        # Vérifier qu'un genre "Action" existe dans la base
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM genres WHERE name = 'Action'")
            genre_exists = cursor.fetchone()['cnt'] > 0

            if not genre_exists:
                pytest.skip("Le genre 'Action' n'existe pas dans la base de test")

        # Appeler la procédure avec le genre "Action"
        with conn.cursor() as cursor:
            # Initialiser les variables de session pour les OUT parameters
            cursor.execute("SET @total = 0, @avg = 0.0, @top = ''")

            # Appeler la procédure
            cursor.execute(f"CALL {proc_name}('Action', @total, @avg, @top)")

            # Récupérer les valeurs des OUT parameters
            cursor.execute("SELECT @total as total_games, @avg as avg_score, @top as top_game")
            result = cursor.fetchone()

            # Vérifications
            total_games = result['total_games']
            avg_score = result['avg_score']
            top_game = result['top_game']

            assert total_games > 0, "Devrait trouver des jeux Action"
            assert avg_score is not None, "Le score moyen ne devrait pas être NULL"
            assert 0 <= avg_score <= 100, f"Le score moyen devrait être entre 0 et 100, trouvé {avg_score}"
            assert top_game is not None and len(top_game) > 0, \
                "Le meilleur jeu ne devrait pas être vide"

        # Vérifier la cohérence avec une requête manuelle
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt, ROUND(AVG(g.metacritic), 2) as avg_val
                FROM games g
                JOIN game_genres gg ON g.id = gg.game_id
                JOIN genres gr ON gg.genre_id = gr.id
                WHERE gr.name = 'Action' AND g.metacritic IS NOT NULL
            """)
            verification = cursor.fetchone()

            # Les valeurs devraient correspondre (avec tolérance pour l'arrondi)
            assert abs(total_games - verification['cnt']) <= 1, \
                f"Le total de jeux devrait correspondre: attendu ~{verification['cnt']}, obtenu {total_games}"

    except FileNotFoundError:
        pytest.skip("Fichier p03_calculate_genre_stats.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        cleanup_procedure(conn, proc_name)


def test_p04_classify_game_procedure(conn):
    """
    Test p04: Procédure avec IF/ELSE qui classifie un jeu
    """
    proc_name = 'sp_classify_game'
    cleanup_procedure(conn, proc_name)

    try:
        # Créer la procédure
        execute_sql_file(conn, 'sql/advanced/procedures/p04_classify_game.sql')

        # Vérifier que la procédure existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.ROUTINES
                WHERE ROUTINE_SCHEMA = DATABASE()
                AND ROUTINE_NAME = %s
                AND ROUTINE_TYPE = 'PROCEDURE'
            """, (proc_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"La procédure {proc_name} n'a pas été créée"

        # Test 1: Jeu avec score >= 90 → "Chef-d'œuvre"
        with conn.cursor() as cursor:
            # Trouver un jeu avec score >= 90
            cursor.execute("SELECT id FROM games WHERE metacritic >= 90 LIMIT 1")
            game = cursor.fetchone()

            if game:
                game_id = game['id']
                cursor.execute("SET @class = ''")
                cursor.execute(f"CALL {proc_name}({game_id}, @class)")
                cursor.execute("SELECT @class as classification")
                result = cursor.fetchone()

                assert result['classification'] == "Chef-d'œuvre", \
                    f"Score >= 90 devrait donner 'Chef-d'œuvre', obtenu '{result['classification']}'"

        # Test 2: Jeu avec score entre 80 et 89 → "Excellent"
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM games WHERE metacritic >= 80 AND metacritic < 90 LIMIT 1")
            game = cursor.fetchone()

            if game:
                game_id = game['id']
                cursor.execute("SET @class = ''")
                cursor.execute(f"CALL {proc_name}({game_id}, @class)")
                cursor.execute("SELECT @class as classification")
                result = cursor.fetchone()

                assert result['classification'] == "Excellent", \
                    f"Score 80-89 devrait donner 'Excellent', obtenu '{result['classification']}'"

        # Test 3: Jeu avec score entre 70 et 79 → "Bon"
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM games WHERE metacritic >= 70 AND metacritic < 80 LIMIT 1")
            game = cursor.fetchone()

            if game:
                game_id = game['id']
                cursor.execute("SET @class = ''")
                cursor.execute(f"CALL {proc_name}({game_id}, @class)")
                cursor.execute("SELECT @class as classification")
                result = cursor.fetchone()

                assert result['classification'] == "Bon", \
                    f"Score 70-79 devrait donner 'Bon', obtenu '{result['classification']}'"

        # Test 4: Jeu avec score NULL → "Non noté"
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM games WHERE metacritic IS NULL LIMIT 1")
            game = cursor.fetchone()

            if game:
                game_id = game['id']
                cursor.execute("SET @class = ''")
                cursor.execute(f"CALL {proc_name}({game_id}, @class)")
                cursor.execute("SELECT @class as classification")
                result = cursor.fetchone()

                assert result['classification'] == "Non noté", \
                    f"Score NULL devrait donner 'Non noté', obtenu '{result['classification']}'"

    except FileNotFoundError:
        pytest.skip("Fichier p04_classify_game.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        cleanup_procedure(conn, proc_name)


def test_p05_update_game_categories_procedure(conn):
    """
    Test p05: Procédure avec curseur qui parcourt des jeux
    """
    proc_name = 'sp_update_game_categories'
    cleanup_procedure(conn, proc_name)

    try:
        # Créer la procédure
        execute_sql_file(conn, 'sql/advanced/procedures/p05_update_game_categories.sql')

        # Vérifier que la procédure existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.ROUTINES
                WHERE ROUTINE_SCHEMA = DATABASE()
                AND ROUTINE_NAME = %s
                AND ROUTINE_TYPE = 'PROCEDURE'
            """, (proc_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"La procédure {proc_name} n'a pas été créée"

        # Appeler la procédure (devrait s'exécuter sans erreur)
        with conn.cursor() as cursor:
            cursor.execute(f"CALL {proc_name}()")
            result = cursor.fetchone()

            # Vérifier le message de retour
            assert result is not None, "La procédure devrait retourner un résultat"
            assert 'result' in result or 'Categories updated' in str(result.values()), \
                "La procédure devrait retourner 'Categories updated'"

            # Vérifier que le message est correct
            result_msg = result.get('result') or list(result.values())[0]
            assert result_msg == 'Categories updated', \
                f"Le message devrait être 'Categories updated', obtenu '{result_msg}'"

        # La procédure ne modifie rien, donc pas besoin de vérifier les données
        # On vérifie juste qu'elle s'exécute sans erreur

    except FileNotFoundError:
        pytest.skip("Fichier p05_update_game_categories.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        cleanup_procedure(conn, proc_name)


def test_p06_insert_game_safe_procedure(conn):
    """
    Test p06: Procédure avec transactions et gestion d'erreurs
    """
    proc_name = 'sp_insert_game_safe'
    cleanup_procedure(conn, proc_name)

    try:
        # Créer la procédure
        execute_sql_file(conn, 'sql/advanced/procedures/p06_insert_game_safe.sql')

        # Vérifier que la procédure existe
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as cnt
                FROM information_schema.ROUTINES
                WHERE ROUTINE_SCHEMA = DATABASE()
                AND ROUTINE_NAME = %s
                AND ROUTINE_TYPE = 'PROCEDURE'
            """, (proc_name,))
            result = cursor.fetchone()
            assert result['cnt'] == 1, f"La procédure {proc_name} n'a pas été créée"

        # Test 1: Insertion valide
        with conn.cursor() as cursor:
            cursor.execute("SET @ok = FALSE, @msg = ''")
            cursor.execute(f"CALL {proc_name}('Test Game Valid', 2023, 85, @ok, @msg)")
            cursor.execute("SELECT @ok as success, @msg as error_msg")
            result = cursor.fetchone()

            success = result['success']
            error_msg = result['error_msg']

            # Convertir success en booléen si nécessaire
            if isinstance(success, int):
                success = bool(success)

            assert success == True or success == 1, \
                f"L'insertion valide devrait réussir, obtenu success={success}, msg='{error_msg}'"
            assert 'réussie' in error_msg.lower() or 'success' in error_msg.lower(), \
                f"Le message devrait indiquer le succès, obtenu '{error_msg}'"

        # Rollback pour ne pas garder le jeu de test
        conn.rollback()

        # Test 2: Année invalide (trop ancienne)
        with conn.cursor() as cursor:
            cursor.execute("SET @ok = FALSE, @msg = ''")
            cursor.execute(f"CALL {proc_name}('Test Game Old', 1800, 85, @ok, @msg)")
            cursor.execute("SELECT @ok as success, @msg as error_msg")
            result = cursor.fetchone()

            success = result['success']
            error_msg = result['error_msg']

            # Convertir success en booléen si nécessaire
            if isinstance(success, int):
                success = bool(success)

            assert success == False or success == 0, \
                f"L'insertion avec année invalide devrait échouer, obtenu success={success}"
            assert 'année' in error_msg.lower() or 'year' in error_msg.lower(), \
                f"Le message d'erreur devrait mentionner l'année, obtenu '{error_msg}'"

        # Test 3: Score invalide (trop élevé)
        with conn.cursor() as cursor:
            cursor.execute("SET @ok = FALSE, @msg = ''")
            cursor.execute(f"CALL {proc_name}('Test Game High Score', 2023, 150, @ok, @msg)")
            cursor.execute("SELECT @ok as success, @msg as error_msg")
            result = cursor.fetchone()

            success = result['success']
            error_msg = result['error_msg']

            # Convertir success en booléen si nécessaire
            if isinstance(success, int):
                success = bool(success)

            assert success == False or success == 0, \
                f"L'insertion avec score invalide devrait échouer, obtenu success={success}"
            assert 'score' in error_msg.lower(), \
                f"Le message d'erreur devrait mentionner le score, obtenu '{error_msg}'"

        # Test 4: Score invalide (négatif)
        with conn.cursor() as cursor:
            cursor.execute("SET @ok = FALSE, @msg = ''")
            cursor.execute(f"CALL {proc_name}('Test Game Negative', 2023, -10, @ok, @msg)")
            cursor.execute("SELECT @ok as success, @msg as error_msg")
            result = cursor.fetchone()

            success = result['success']

            # Convertir success en booléen si nécessaire
            if isinstance(success, int):
                success = bool(success)

            assert success == False or success == 0, \
                f"L'insertion avec score négatif devrait échouer, obtenu success={success}"

        # Rollback final pour nettoyer tout
        conn.rollback()

    except FileNotFoundError:
        pytest.skip("Fichier p06_insert_game_safe.sql non trouvé")
    except MissingQueryError:
        pytest.skip("Requête non encore écrite")
    finally:
        conn.rollback()
        cleanup_procedure(conn, proc_name)
