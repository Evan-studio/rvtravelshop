#!/usr/bin/env python3
"""
Script pour créer un nouveau dépôt Git sans historique
(plus rapide que de nettoyer l'historique existant)
"""

import subprocess
import sys
import json
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
    print("🆕 CRÉATION D'UN NOUVEAU DÉPÔT GIT SANS HISTORIQUE")
    print("=" * 70)
    print()
    print("⚠️  ATTENTION: Ce script va:")
    print("   1. Supprimer l'historique Git actuel (.git)")
    print("   2. Créer un nouveau dépôt Git")
    print("   3. Ajouter tous les fichiers actuels (sauf .gitignore)")
    print("   4. Créer un commit initial")
    print()
    print("✅ Les fichiers physiques (vidéos, images, etc.) RESTENT sur votre disque!")
    print("   Seul l'historique Git est supprimé.")
    print()
    
    response = input("Continuer? (oui/non): ").strip().lower()
    if response not in ['oui', 'o', 'yes', 'y']:
        print("❌ Opération annulée")
        return
    
    print()
    print("🔄 Étape 1/6: Vérification du répertoire...")
    current_dir = Path.cwd()
    print(f"   Répertoire: {current_dir}")
    
    print()
    print("🔄 Étape 2/6: Sauvegarde de la configuration Git...")
    # Lire la config du remote
    config_path = current_dir / "git_remote_config.json"
    remote_url = None
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            user = data.get("user", "").strip()
            repo = data.get("repo", "").strip()
            if user and repo:
                remote_url = f"https://github.com/{user}/{repo}.git"
                print(f"   Remote configuré: {remote_url}")
        except:
            pass
    
    if not remote_url:
        success, current_remote, _ = run_command("git remote get-url origin", check=False)
        if success:
            remote_url = current_remote.strip()
            print(f"   Remote détecté: {remote_url}")
    
    print()
    print("🔄 Étape 3/6: Suppression de l'historique Git...")
    success, output, error = run_command("rm -rf .git")
    if not success:
        print(f"❌ Erreur: {error}")
        return
    print("   ✅ Historique supprimé")
    
    print()
    print("🔄 Étape 4/6: Réinitialisation de Git...")
    success, output, error = run_command("git init")
    if not success:
        print(f"❌ Erreur: {error}")
        return
    print("   ✅ Git initialisé")
    
    print()
    print("🔄 Étape 5/6: Ajout des fichiers (sauf .gitignore)...")
    print("   → Toutes les images WebP, HTML, CSS, etc. seront ajoutées")
    print("   → Les vidéos MP4 seront exclues (dans .gitignore)")
    success, output, error = run_command("git add -A")
    if not success:
        print(f"❌ Erreur: {error}")
        return
    
    # Compter les fichiers ajoutés
    success, output, _ = run_command("git status --short", check=False)
    files_count = len([f for f in output.split('\n') if f]) if success and output else 0
    
    # Compter les images
    success, images_count, _ = run_command("git ls-files | grep -E '\\.(webp|jpg|jpeg|png)$' | wc -l", check=False)
    images_count = int(images_count.strip()) if images_count.strip().isdigit() else 0
    
    print(f"   ✅ {files_count} fichier(s) ajouté(s)")
    print(f"   ✅ {images_count} image(s) WebP/JPG/PNG incluse(s)")
    
    print()
    print("🔄 Étape 6/6: Création du commit initial...")
    success, output, error = run_command('git commit -m "Initial commit - cleaned repository"')
    if not success:
        print(f"❌ Erreur: {error}")
        return
    print("   ✅ Commit créé")
    
    if remote_url:
        print()
        print("🔄 Configuration du remote...")
        success, output, error = run_command(f'git remote add origin "{remote_url}"', check=False)
        if success:
            print(f"   ✅ Remote configuré: {remote_url}")
        else:
            print(f"   ⚠️  Remote déjà configuré ou erreur: {error}")
    
    print()
    print("=" * 70)
    print("✅ NOUVEAU DÉPÔT CRÉÉ AVEC SUCCÈS!")
    print("=" * 70)
    print()
    print("💡 Pour envoyer vers GitHub, exécutez:")
    print("   git push origin main --force")
    print()
    print("⚠️  ATTENTION: --force écrasera le dépôt sur GitHub")
    print("   (mais c'est normal car le dépôt est vide)")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Opération annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        sys.exit(1)

