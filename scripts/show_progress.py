#!/usr/bin/env python3
"""
Script de visualisation de la progression des exercices SQL.
Affiche les tests complétés, les badges débloqués et les recommandations.
"""

import subprocess
import sys
import re
from collections import defaultdict

# Définition des couleurs ANSI
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Définition des exercices par niveau
EXERCISES = {
    'beginner': ['00a', '00b', '00c', '00d', '00e', '00f', '00g', '00h'],
    'intermediate': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10'],
    'advanced': ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
}

# Définition des badges
BADGES = {
    'bases': {
        'name': '🌱 Bases SQL',
        'exercises': ['00a', '00b', '00c', '00d', '00e', '00f', '00g', '00h'],
        'skills': 'SELECT, WHERE, ORDER BY, LIMIT'
    },
    'aggregation': {
        'name': '🔢 Agrégation',
        'exercises': ['00g', '00h', '03', '04'],
        'skills': 'COUNT, AVG, GROUP BY, HAVING'
    },
    'joins': {
        'name': '🔗 Jointures',
        'exercises': ['03', '04', '08', '09'],
        'skills': 'INNER JOIN, LEFT JOIN, many-to-many'
    },
    'windows': {
        'name': '🪟 Window Functions',
        'exercises': ['05', '06', '07'],
        'skills': 'RANK, PARTITION BY, OVER'
    },
    'ctes': {
        'name': '📝 CTEs',
        'exercises': ['05', '10'],
        'skills': 'WITH clause, sous-requêtes'
    },
    'optimization': {
        'name': '⚡ Optimisation',
        'exercises': ['16', '17'],
        'skills': 'EXPLAIN, index, performance'
    },
    'master': {
        'name': '🎓 Maître SQL',
        'exercises': None,  # All exercises
        'skills': 'Toutes les compétences !'
    }
}

def run_tests():
    """Execute pytest and capture results."""
    try:
        result = subprocess.run(
            ['pytest', '--tb=no', '-v', 'tests/'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def parse_test_results(output):
    """Parse pytest output to get passed/failed tests."""
    passed = []
    failed = []
    skipped = []
    
    # Pattern to match test results: test_XXX_name PASSED/FAILED/SKIPPED
    pattern = r'test_(\w+)\.py.*?(PASSED|FAILED|SKIPPED)'
    
    for match in re.finditer(pattern, output):
        test_id = match.group(1)
        status = match.group(2)
        
        # Extract exercise number (00a, 01, 02, etc.)
        if test_id.startswith('00'):
            # Beginner exercises: 00a, 00b, etc.
            ex_id = test_id[:3]
        else:
            # Other exercises: 01, 02, etc.
            ex_id = test_id[:2].lstrip('0') or '0'
        
        if status == 'PASSED':
            passed.append(ex_id)
        elif status == 'FAILED':
            failed.append(ex_id)
        elif status == 'SKIPPED':
            skipped.append(ex_id)
    
    return set(passed), set(failed), set(skipped)

def print_progress_bar(completed, total, level_name, color):
    """Print a colored progress bar."""
    percentage = (completed / total * 100) if total > 0 else 0
    bar_length = 30
    filled = int(bar_length * completed / total) if total > 0 else 0
    bar = '█' * filled + '░' * (bar_length - filled)
    
    print(f"{color}{Colors.BOLD}{level_name:15}{Colors.RESET} {color}{bar}{Colors.RESET} {completed}/{total} ({percentage:.0f}%)")

def check_badges(passed_exercises):
    """Check which badges are unlocked."""
    unlocked = []
    
    for badge_id, badge_info in BADGES.items():
        if badge_id == 'master':
            # Master badge requires all exercises
            all_exercises = EXERCISES['beginner'] + EXERCISES['intermediate'] + EXERCISES['advanced']
            if all(ex in passed_exercises for ex in all_exercises):
                unlocked.append(badge_info)
        else:
            # Other badges require specific exercises
            if all(ex in passed_exercises for ex in badge_info['exercises']):
                unlocked.append(badge_info)
    
    return unlocked

def get_next_recommendations(passed_exercises):
    """Get next recommended exercises."""
    recommendations = []
    
    # Check beginner level
    beginner_remaining = [ex for ex in EXERCISES['beginner'] if ex not in passed_exercises]
    if beginner_remaining:
        return beginner_remaining[:3]  # Return first 3
    
    # Check intermediate level
    intermediate_remaining = [ex for ex in EXERCISES['intermediate'] if ex not in passed_exercises]
    if intermediate_remaining:
        return intermediate_remaining[:3]
    
    # Check advanced level
    advanced_remaining = [ex for ex in EXERCISES['advanced'] if ex not in passed_exercises]
    if advanced_remaining:
        return advanced_remaining[:3]
    
    return []

def main():
    """Main function."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}📊  PROGRESSION SQL - Dataset RAWG{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    
    print("🔍 Analyse des tests en cours...\n")
    
    # Run tests
    output = run_tests()
    
    if output == "TIMEOUT":
        print(f"{Colors.RED}❌ Les tests ont dépassé le délai d'exécution{Colors.RESET}")
        sys.exit(1)
    elif output.startswith("ERROR"):
        print(f"{Colors.RED}❌ {output}{Colors.RESET}")
        sys.exit(1)
    
    # Parse results
    passed, failed, skipped = parse_test_results(output)
    
    # Calculate progress by level
    beginner_passed = len([ex for ex in EXERCISES['beginner'] if ex in passed])
    intermediate_passed = len([ex for ex in EXERCISES['intermediate'] if ex in passed])
    advanced_passed = len([ex for ex in EXERCISES['advanced'] if ex in passed])
    
    beginner_total = len(EXERCISES['beginner'])
    intermediate_total = len(EXERCISES['intermediate'])
    advanced_total = len(EXERCISES['advanced'])
    
    # Display progress bars
    print(f"{Colors.BOLD}Progression par niveau :{Colors.RESET}\n")
    print_progress_bar(beginner_passed, beginner_total, "🟢 Débutant", Colors.GREEN)
    print_progress_bar(intermediate_passed, intermediate_total, "🟡 Intermédiaire", Colors.YELLOW)
    print_progress_bar(advanced_passed, advanced_total, "🔴 Avancé", Colors.RED)
    
    total_passed = beginner_passed + intermediate_passed + advanced_passed
    total_exercises = beginner_total + intermediate_total + advanced_total
    print(f"\n{Colors.BOLD}Total{Colors.RESET}")
    print_progress_bar(total_passed, total_exercises, "Tous niveaux", Colors.CYAN)
    
    # Check badges
    unlocked_badges = check_badges(passed)
    
    print(f"\n{Colors.BOLD}🏆 Badges débloqués : {len(unlocked_badges)}/{len(BADGES)}{Colors.RESET}\n")
    
    if unlocked_badges:
        for badge in unlocked_badges:
            print(f"   {badge['name']} - {Colors.CYAN}{badge['skills']}{Colors.RESET}")
    else:
        print(f"   {Colors.YELLOW}Aucun badge débloqué pour le moment. Continuez !{Colors.RESET}")
    
    # Next recommendations
    next_ex = get_next_recommendations(passed)
    
    if next_ex:
        print(f"\n{Colors.BOLD}🎯 Prochains exercices recommandés :{Colors.RESET}\n")
        for ex in next_ex:
            print(f"   → q{ex}")
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Félicitations ! Vous avez terminé tous les exercices !{Colors.RESET}")
    
    # Summary
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"\n{Colors.BOLD}Résumé :{Colors.RESET}")
    print(f"   ✅ {Colors.GREEN}{len(passed)} tests réussis{Colors.RESET}")
    if failed:
        print(f"   ❌ {Colors.RED}{len(failed)} tests échoués{Colors.RESET}")
    if skipped:
        print(f"   ⏭️  {Colors.YELLOW}{len(skipped)} tests ignorés{Colors.RESET}")
    
    print(f"\n💡 Pour plus de détails : {Colors.CYAN}docker exec -it vg-app pytest -v{Colors.RESET}")
    print(f"📖 Consultez PARCOURS.md pour la cartographie complète\n")

if __name__ == '__main__':
    main()
