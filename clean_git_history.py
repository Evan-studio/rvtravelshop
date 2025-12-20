#!/usr/bin/env python3
"""
Script pour nettoyer l'historique Git en supprimant les fichiers volumineux
(vidéos, backups CSV, etc.) qui ne devraient pas être dans Git.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """Exécute une commande shell."""
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

def main():
    print("=" * 70)
    print("🧹 NETTOYAGE DE L'HISTORIQUE GIT")
    print("=" * 70)
    print()
    print("⚠️  ATTENTION: Ce script va supprimer les fichiers volumineux de l'historique Git")
    print("   (vidéos MP4, backups CSV, etc.)")
    print()
    print("Options:")
    print("1. Nettoyer l'historique (recommandé si vous avez beaucoup de commits)")
    print("2. Créer un nouveau dépôt sans historique (plus rapide)")
    print("3. Annuler")
    print()
    
    choice = input("Votre choix (1/2/3): ").strip()
    
    if choice == "1":
        print("\n🧹 Nettoyage de l'historique avec git filter-branch...")
        print("   Cela peut prendre plusieurs minutes...")
        print()
        
        # Supprimer les vidéos de l'historique Git (PAS les fichiers physiques!)
        print("→ Suppression des fichiers vidéo de l'historique Git uniquement...")
        print("   ⚠️  ATTENTION: Les fichiers vidéo RESTENT sur votre disque!")
        print("   Seul l'historique Git est nettoyé (git rm --cached)")
        success, output, error = run_command(
            'git filter-branch --force --index-filter '
            '"git rm --cached --ignore-unmatch -r images/products/*/video.* images/products/*/*.mp4 images/products/*/*.webm images/products/*/*.mov images/products/*/*.avi images/products/*/*.mkv" '
            '--prune-empty --tag-name-filter cat -- --all'
        )
        if not success:
            print(f"❌ Erreur: {error}")
            return
        
        # Supprimer les backups CSV de l'historique Git (PAS les fichiers physiques!)
        print("→ Suppression des fichiers CSV de backup de l'historique Git uniquement...")
        print("   ⚠️  ATTENTION: Les fichiers de backup RESTENT sur votre disque!")
        success, output, error = run_command(
            'git filter-branch --force --index-filter '
            '"git rm --cached --ignore-unmatch **/*.backup **/*.backup2 **/*.backup_*" '
            '--prune-empty --tag-name-filter cat -- --all'
        )
        if not success:
            print(f"❌ Erreur: {error}")
            return
        
        print("\n✅ Historique nettoyé!")
        print("\n💡 Maintenant, exécutez:")
        print("   git push origin --force --all")
        print("   (ATTENTION: cela écrasera l'historique sur GitHub)")
        
    elif choice == "2":
        print("\n🆕 Création d'un nouveau dépôt sans historique...")
        print("   Cela va créer un nouveau commit initial avec seulement les fichiers actuels")
        print()
        
        # Sauvegarder les fichiers actuels
        print("→ Sauvegarde des fichiers actuels...")
        success, output, error = run_command("git stash")
        
        # Supprimer l'historique Git
        print("→ Suppression de l'historique Git...")
        success, output, error = run_command("rm -rf .git")
        if not success:
            print(f"❌ Erreur: {error}")
            return
        
        # Réinitialiser Git
        print("→ Réinitialisation de Git...")
        success, output, error = run_command("git init")
        if not success:
            print(f"❌ Erreur: {error}")
            return
        
        # Ajouter tous les fichiers (sauf ceux dans .gitignore)
        print("→ Ajout des fichiers...")
        success, output, error = run_command("git add -A")
        if not success:
            print(f"❌ Erreur: {error}")
            return
        
        # Créer le commit initial
        print("→ Création du commit initial...")
        success, output, error = run_command('git commit -m "Initial commit - cleaned history"')
        if not success:
            print(f"❌ Erreur: {error}")
            return
        
        # Reconfigurer le remote
        print("→ Reconfiguration du remote...")
        success, output, error = run_command("git remote add origin https://github.com/Evan-studio/rvtravelshop.git")
        if not success:
            print(f"⚠️  Remote déjà configuré ou erreur: {error}")
        
        print("\n✅ Nouveau dépôt créé!")
        print("\n💡 Maintenant, exécutez:")
        print("   git push origin main --force")
        print("   (ATTENTION: cela écrasera le dépôt sur GitHub)")
        
    else:
        print("❌ Opération annulée")
        return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Opération annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        sys.exit(1)

