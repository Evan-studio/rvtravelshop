#!/usr/bin/env python3
"""
Script Python pour mettre à jour GitHub automatiquement (sans confirmation).
Usage: python3 update_github_auto.py [message de commit]
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

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
    success, output, _ = run_command("git status --porcelain", check=False)
    return success and len(output) > 0

def get_changes_summary():
    """Récupère un résumé des changements."""
    success, output, _ = run_command("git status --short", check=False)
    if success:
        return output.split('\n') if output else []
    return []

def ensure_remote():
    """
    Lit git_remote_config.json (user/repo) et s'assure que origin pointe vers ce dépôt.
    Si le fichier est absent, ne fait rien.
    """
    config_path = Path(__file__).parent / "git_remote_config.json"
    if not config_path.exists():
        return True  # rien à faire
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        user = data.get("user", "").strip()
        repo = data.get("repo", "").strip()
        if not user or not repo:
            print_warning("git_remote_config.json : user ou repo manquant, aucune mise à jour du remote.")
            return True
        target = f"https://github.com/{user}/{repo}.git"
        # Récupérer le remote actuel
        success, current, _ = run_command("git remote get-url origin", check=False)
        if success and current.strip() == target:
            print_info(f"Remote déjà configuré : {target}")
            return True
        print_info(f"Configuration du remote origin vers {target}...")
        # Supprimer origin si présent, puis ajouter
        run_command("git remote remove origin", check=False)
        ok, _, err = run_command(f'git remote add origin "{target}"', check=False)
        if not ok:
            print_error(f"Impossible de configurer origin : {err}")
            return False
        print_success(f"Remote origin configuré : {target}")
        return True
    except Exception as e:
        print_warning(f"Impossible de lire git_remote_config.json : {e}")
        return True

def main():
    """Fonction principale."""
    print("=" * 70)
    print_header("🚀 MISE À JOUR AUTOMATIQUE VERS GITHUB")
    print("=" * 70)
    print()
    
    # Afficher le répertoire de travail
    current_dir = Path.cwd()
    script_dir = Path(__file__).parent.resolve()
    print_info(f"Répertoire de travail: {current_dir}")
    print_info(f"Répertoire du script: {script_dir}")
    
    # Vérifier qu'on est dans le bon répertoire (celui du script)
    if current_dir != script_dir:
        print_warning(f"⚠️  Le répertoire de travail ({current_dir}) est différent du répertoire du script ({script_dir})")
        print_info("Changement vers le répertoire du script...")
        import os
        os.chdir(script_dir)
        print_success(f"Répertoire changé vers: {Path.cwd()}")
    print()
    
    if not ensure_remote():
        sys.exit(1)
    
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
        commit_message = f"Update: Mise à jour du site {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    print_info(f"Message de commit: {commit_message}")
    print()
    
    # Ajouter tous les fichiers (modifiés, supprimés et non trackés)
    print_info("Ajout de tous les fichiers du dépôt...")
    print_info("  → Fichiers modifiés et supprimés...")
    success, output, error = run_command("git add -A")
    if not success:
        print_error(f"Erreur lors de l'ajout des fichiers: {error}")
        sys.exit(1)
    
    # Afficher les fichiers ajoutés
    success, output, _ = run_command("git diff --cached --name-only", check=False)
    files_added = [f for f in output.split('\n') if f] if success and output else []
    files_count = len(files_added)
    
    if files_count == 0:
        print_warning("Aucun fichier à commiter.")
        sys.exit(0)
    
    print_success(f"{files_count} fichier(s) ajouté(s)")
    
    # Afficher la liste des fichiers (limité à 20 pour ne pas surcharger)
    if files_count <= 20:
        print_info("Fichiers à commiter:")
        for f in files_added:
            print(f"  • {f}")
    else:
        print_info(f"Fichiers à commiter (affichage des 20 premiers sur {files_count}):")
        for f in files_added[:20]:
            print(f"  • {f}")
        print(f"  ... et {files_count - 20} autre(s) fichier(s)")
    print()
    
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
    
    # Détecter la branche actuelle
    success, current_branch, _ = run_command("git branch --show-current", check=False)
    if not success or not current_branch:
        # Fallback sur main si la détection échoue
        current_branch = "main"
    else:
        current_branch = current_branch.strip()
    
    # Vérifier si c'est le premier push (dépôt vide)
    success, remote_branch, _ = run_command(f"git ls-remote --heads origin {current_branch}", check=False)
    is_first_push = not success or not remote_branch.strip()
    
    # Push vers GitHub automatiquement
    if is_first_push:
        print_info(f"Envoi initial vers GitHub (branche: {current_branch})...")
        print_warning("⚠️  Premier push : cela peut prendre plusieurs minutes si le dépôt est volumineux")
        print_info("   Le script affiche la progression en temps réel...")
        print()
        # Pour le premier push, utiliser --set-upstream et --progress
        push_cmd = f"git push --set-upstream origin {current_branch} --progress"
    else:
        print_info(f"Envoi vers GitHub (branche: {current_branch})...")
        push_cmd = f"git push origin {current_branch} --progress"
    
    # Exécuter le push avec affichage en temps réel
    try:
        process = subprocess.Popen(
            push_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Afficher la sortie en temps réel
        output_lines = []
        for line in process.stdout:
            line = line.strip()
            if line:
                output_lines.append(line)
                # Afficher les lignes de progression importantes
                if 'Writing objects' in line or 'Counting objects' in line or '%' in line or 'done' in line.lower():
                    print(f"  {line}")
        
        process.wait()
        success = process.returncode == 0
        output = '\n'.join(output_lines)
        error = "" if success else output
        
    except Exception as e:
        success = False
        output = ""
        error = str(e)
    
    if not success:
        print_error(f"Erreur lors du push vers GitHub: {error}")
        print_info("💡 Essayez de vérifier votre connexion et vos permissions Git")
        if is_first_push:
            print_info("💡 Pour un premier push volumineux, vous pouvez aussi utiliser:")
            print_info(f"   git push --set-upstream origin {current_branch}")
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

