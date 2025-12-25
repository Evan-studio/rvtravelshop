#!/usr/bin/env python3
"""
Script pour configurer Git LFS pour les images volumineuses
Cela permettra de push les images sans bloquer
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip() if e.stdout else "", e.stderr.strip() if e.stderr else str(e)

def main():
    print("=" * 70)
    print("🔧 CONFIGURATION DE GIT LFS POUR LES IMAGES")
    print("=" * 70)
    print()
    print("Git LFS permet de stocker les gros fichiers séparément")
    print("Cela réduira la taille du push vers GitHub")
    print()
    
    # Vérifier si Git LFS est installé
    print("🔄 Vérification de Git LFS...")
    success, output, error = run_command("git lfs version", check=False)
    if not success:
        print("❌ Git LFS n'est pas installé!")
        print()
        print("💡 Pour installer Git LFS:")
        print("   macOS: brew install git-lfs")
        print("   Puis: git lfs install")
        return
    print(f"   ✅ {output}")
    
    # Installer Git LFS
    print()
    print("🔄 Installation de Git LFS...")
    success, output, error = run_command("git lfs install", check=True)
    if not success:
        print(f"❌ Erreur: {error}")
        return
    print("   ✅ Git LFS installé")
    
    # Configurer Git LFS pour les images WebP
    print()
    print("🔄 Configuration de Git LFS pour les images WebP...")
    success, output, error = run_command("git lfs track '*.webp'", check=True)
    if not success:
        print(f"❌ Erreur: {error}")
        return
    print("   ✅ WebP configuré pour Git LFS")
    
    # Ajouter .gitattributes
    print()
    print("🔄 Ajout de .gitattributes...")
    success, output, error = run_command("git add .gitattributes", check=True)
    if not success:
        print(f"❌ Erreur: {error}")
        return
    print("   ✅ .gitattributes ajouté")
    
    # Migrer les images existantes vers LFS
    print()
    print("🔄 Migration des images WebP vers Git LFS...")
    print("   (Cela peut prendre 1-2 minutes...)")
    success, output, error = run_command("git lfs migrate import --include='*.webp' --everything", check=True)
    if not success:
        print(f"⚠️  Erreur lors de la migration: {error}")
        print("   Continuons quand même...")
    else:
        print("   ✅ Images migrées vers Git LFS")
    
    # Vérifier la taille
    print()
    print("🔄 Vérification de la taille du dépôt...")
    success, output, _ = run_command("git count-objects -vH", check=False)
    if success:
        for line in output.split('\n'):
            if 'size-pack' in line:
                print(f"   Taille: {line.split(':')[1].strip()}")
    
    print()
    print("=" * 70)
    print("✅ GIT LFS CONFIGURÉ!")
    print("=" * 70)
    print()
    print("💡 Maintenant, essayez le push:")
    print("   git push origin main --force")
    print()
    print("⚠️  Note: La première fois, Git LFS peut prendre du temps")
    print("   pour uploader les images vers le serveur LFS")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Opération annulée")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


