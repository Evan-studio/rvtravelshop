#!/usr/bin/env python3
"""
Script Python pour mettre à jour GitHub automatiquement.
Usage: python3 update_github.py [message de commit]
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.NC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

def print_header(message):
    print(f"{Colors.CYAN}{message}{Colors.NC}")

def run_command(cmd, check=True):
    """Exécute une commande shell et retourne le résultat."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip() if e.stdout else "", e.stderr.strip() if e.stderr else str(e)

def check_git_repo():
    """Vérifie qu'on est dans un dépôt Git."""
    success, _, _ = run_command("git rev-parse --git-dir", check=False)
    if not success:
        print_error("Ce n'est pas un dépôt Git !")
        return False
    return True

def has_changes():
    """Vérifie s'il y a des changements à commiter."""
    # Vérifier les fichiers modifiés
    success, output, _ = run_command("git status --porcelain", check=False)
    return success and len(output) > 0

def get_changes_summary():
    """Récupère un résumé des changements."""
    success, output, _ = run_command("git status --short", check=False)
    if success:
        return output.split('\n') if output else []
    return []

def main():
    """Fonction principale."""
    print("=" * 70)
    print_header("🚀 MISE À JOUR VERS GITHUB")
    print("=" * 70)
    print()
    
    # Vérifier qu'on est dans un dépôt Git
    if not check_git_repo():
        sys.exit(1)
    
    # Vérifier s'il y a des changements
    if not has_changes():
        print_warning("Aucun changement détecté. Rien à commiter.")
        sys.exit(0)
    
    # Afficher le statut
    print_info("Statut actuel du dépôt :")
    changes = get_changes_summary()
    for change in changes:
        if change:
            print(f"  {change}")
    print()
    
    # Récupérer le message de commit
    if len(sys.argv) > 1:
        commit_message = " ".join(sys.argv[1:])
    else:
        default_message = f"Update: Mise à jour du site {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        print(f"📝 Message de commit (Entrée pour '{default_message}'): ", end="")
        user_input = input().strip()
        commit_message = user_input if user_input else default_message
    
    # Ajouter tous les fichiers
    print_info("Ajout des fichiers modifiés...")
    success, output, error = run_command("git add -A")
    if not success:
        print_error(f"Erreur lors de l'ajout des fichiers: {error}")
        sys.exit(1)
    
    # Compter les fichiers ajoutés
    success, output, _ = run_command("git diff --cached --name-only", check=False)
    files_count = len([f for f in output.split('\n') if f]) if success and output else 0
    
    if files_count == 0:
        print_warning("Aucun fichier à commiter.")
        sys.exit(0)
    
    print_success(f"{files_count} fichier(s) ajouté(s)")
    
    # Créer le commit
    print_info("Création du commit...")
    success, output, error = run_command(f'git commit -m "{commit_message}"')
    if not success:
        print_error(f"Erreur lors de la création du commit: {error}")
        sys.exit(1)
    
    print_success("Commit créé avec succès")
    
    # Afficher les détails du commit
    print()
    print_info("Détails du commit :")
    success, output, _ = run_command("git log -1 --stat --oneline", check=False)
    if success:
        print(output)
    print()
    
    # Demander confirmation pour le push
    print("📤 Pousser vers GitHub ? (o/N): ", end="")
    confirm = input().strip().lower()
    
    if confirm not in ['o', 'o']:
        print_warning("Push annulé. Vous pouvez le faire manuellement avec: git push origin main")
        sys.exit(0)
    
    # Push vers GitHub
    print_info("Envoi vers GitHub...")
    success, output, error = run_command("git push origin main")
    if not success:
        print_error(f"Erreur lors du push vers GitHub: {error}")
        print_info("💡 Essayez de vérifier votre connexion et vos permissions Git")
        sys.exit(1)
    
    # Afficher l'URL du dépôt
    success, repo_url, _ = run_command("git remote get-url origin", check=False)
    if success:
        print_success("✅ Mise à jour envoyée vers GitHub avec succès !")
        print()
        print_info(f"🌐 Dépôt: {repo_url}")
    else:
        print_success("✅ Mise à jour envoyée vers GitHub avec succès !")
    
    print()
    print("=" * 70)
    print_success("TERMINÉ !")
    print("=" * 70)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Opération annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erreur inattendue: {e}")
        sys.exit(1)

