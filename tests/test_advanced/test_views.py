"""Tests for SQL views exercises."""
import pytest
from .conftest import execute_sql_file, cleanup_view


def test_v01_genre_stats_view(conn):
    """Test v01: Create view_genre_stats with genre aggregations."""
    view_name = 'view_genre_stats'
    
    # Cleanup before test
    cleanup_view(conn, view_name)
    
    try:
        # Execute the CREATE VIEW statement
        execute_sql_file(conn, 'sql/advanced/views/v01_genre_stats.sql')
        
        # Test that the view exists and works
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {view_name} LIMIT 5")
            results = cursor.fetchall()
            
            # Should return at least one genre
            assert len(results) > 0, "View should return at least one genre"
            
            # Check columns exist
            first_row = results[0]
            assert 'genre' in first_row, "Column 'genre' missing"
            assert 'total_games' in first_row, "Column 'total_games' missing"
            assert 'avg_score' in first_row, "Column 'avg_score' missing"
            assert 'first_year' in first_row, "Column 'first_year' missing"
            assert 'last_year' in first_row, "Column 'last_year' missing"
            
            # Check data quality
            assert first_row['total_games'] > 0, "total_games should be > 0"
            assert first_row['avg_score'] > 0, "avg_score should be > 0"
            assert first_row['first_year'] <= first_row['last_year'], "first_year should be <= last_year"
            
        print(f"✅ View {view_name} created and working correctly")
        
    finally:
        # Cleanup after test
        cleanup_view(conn, view_name)


def test_v02_top_games_by_platform_view(conn):
    """Test v02: Create view_top_games_by_platform with ranking."""
    view_name = 'view_top_games_by_platform'
    
    cleanup_view(conn, view_name)
    
    try:
        execute_sql_file(conn, 'sql/advanced/views/v02_top_games_by_platform.sql')
        
        with conn.cursor() as cursor:
            # Test the view works
            cursor.execute(f"SELECT * FROM {view_name} WHERE platform_rank <= 3 LIMIT 10")
            results = cursor.fetchall()
            
            assert len(results) > 0, "View should return ranked games"
            
            # Check columns
            first_row = results[0]
            assert 'platform' in first_row
            assert 'game_name' in first_row
            assert 'year' in first_row
            assert 'metacritic' in first_row
            assert 'platform_rank' in first_row
            
            # Check ranking logic
            assert first_row['platform_rank'] >= 1, "Rank should start at 1"
            
            # Check that rankings are correct within same platform
            cursor.execute(f"""
                SELECT platform, game_name, metacritic, platform_rank 
                FROM {view_name} 
                WHERE platform = (SELECT platform FROM {view_name} LIMIT 1)
                ORDER BY platform_rank 
                LIMIT 3
            """)
            platform_results = cursor.fetchall()
            if len(platform_results) >= 2:
                assert platform_results[0]['metacritic'] >= platform_results[1]['metacritic'], \
                    "Higher rank should have better or equal score"
            
        print(f"✅ View {view_name} created and working correctly")
        
    finally:
        cleanup_view(conn, view_name)


def test_v03_trending_genres_view(conn):
    """Test v03: Create view_trending_genres based on view_genre_stats."""
    base_view = 'view_genre_stats'
    trending_view = 'view_trending_genres'
    
    # Cleanup
    cleanup_view(conn, trending_view)
    cleanup_view(conn, base_view)
    
    try:
        # First create the base view
        execute_sql_file(conn, 'sql/advanced/views/v01_genre_stats.sql')
        
        # Then create the trending view
        execute_sql_file(conn, 'sql/advanced/views/v03_trending_genres.sql')
        
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {trending_view} LIMIT 10")
            results = cursor.fetchall()
            
            # Should have trending genres
            assert len(results) > 0, "View should return trending genres"
            
            # Check columns
            first_row = results[0]
            assert 'genre' in first_row
            assert 'total_games' in first_row
            assert 'avg_score' in first_row
            
            # Check filters are applied
            for row in results:
                assert row['avg_score'] >= 75, f"avg_score should be >= 75, got {row['avg_score']}"
                # Note: last_year filter is applied in the view, we can't check it here
            
        print(f"✅ View {trending_view} created and working correctly")
        
    finally:
        cleanup_view(conn, trending_view)
        cleanup_view(conn, base_view)


def test_v04_high_quality_games_view(conn):
    """Test v04: Create view_high_quality_games with GROUP_CONCAT."""
    view_name = 'view_high_quality_games'
    
    cleanup_view(conn, view_name)
    
    try:
        execute_sql_file(conn, 'sql/advanced/views/v04_high_quality_games.sql')
        
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {view_name} LIMIT 10")
            results = cursor.fetchall()
            
            assert len(results) > 0, "View should return high-quality games"
            
            # Check columns
            first_row = results[0]
            assert 'id' in first_row
            assert 'name' in first_row
            assert 'year' in first_row
            assert 'metacritic' in first_row
            assert 'ratings_count' in first_row
            assert 'genres' in first_row
            
            # Check filter is applied
            for row in results:
                assert row['metacritic'] >= 85, f"Metacritic should be >= 85, got {row['metacritic']}"
            
            # Check GROUP_CONCAT worked (genres should be a string with commas)
            if first_row['genres']:
                assert isinstance(first_row['genres'], str), "Genres should be a string"
            
        print(f"✅ View {view_name} created and working correctly")
        
    finally:
        cleanup_view(conn, view_name)


def test_v05_games_complete_view(conn):
    """Test v05: Create view_games_complete with all metadata."""
    view_name = 'view_games_complete'
    
    cleanup_view(conn, view_name)
    
    try:
        execute_sql_file(conn, 'sql/advanced/views/v05_games_complete.sql')
        
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {view_name} LIMIT 5")
            results = cursor.fetchall()
            
            assert len(results) > 0, "View should return complete game info"
            
            # Check all columns
            first_row = results[0]
            required_cols = ['id', 'name', 'year', 'metacritic', 'rating',
                           'platforms', 'genres', 'publishers', 'developers']
            for col in required_cols:
                assert col in first_row, f"Column '{col}' missing"
            
            # Check GROUP_CONCAT fields are strings (or None)
            for col in ['platforms', 'genres', 'publishers', 'developers']:
                if first_row[col] is not None:
                    assert isinstance(first_row[col], str), f"{col} should be a string"
            
        print(f"✅ View {view_name} created and working correctly")
        
    finally:
        cleanup_view(conn, view_name)


def test_v06_games_basic_view(conn):
    """Test v06: Create view_games_basic (updatable view)."""
    view_name = 'view_games_basic'
    
    cleanup_view(conn, view_name)
    
    try:
        execute_sql_file(conn, 'sql/advanced/views/v06_games_basic.sql')
        
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {view_name} LIMIT 10")
            results = cursor.fetchall()
            
            assert len(results) > 0, "View should return games"
            
            # Check columns
            first_row = results[0]
            assert 'id' in first_row
            assert 'name' in first_row
            assert 'year' in first_row
            assert 'metacritic' in first_row
            assert 'ratings_count' in first_row
            
            # Check that year IS NOT NULL filter is applied
            for row in results:
                assert row['year'] is not None, "All games should have a year (view filter)"
            
            # Note: We don't test UPDATE here as it would modify the actual data
            # In a real scenario, you'd test on a copy of the database
            
        print(f"✅ View {view_name} created and working correctly")
        
    finally:
        cleanup_view(conn, view_name)
