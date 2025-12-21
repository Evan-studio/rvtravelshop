#!/usr/bin/env python3
"""
Script pour supprimer dist/ et images 4-6 de Git.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """Exécute une commande et retourne le résultat."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def main():
    print("=" * 70)
    print("🗑️  SUPPRESSION DE dist/ ET IMAGES 4-6 DE GIT")
    print("=" * 70)
    print()
    
    # 1. Supprimer dist/
    print("1️⃣  Suppression du dossier dist/ de Git...")
    success, output, error = run_command("git rm -r --cached dist/", check=False)
    if success or "did not match any files" not in error:
        deleted_dist = output.count("rm 'dist/")
        print(f"   ✅ {deleted_dist} fichiers dist/ supprimés de l'index")
    else:
        print(f"   ⚠️  Erreur: {error[:200]}")
    print()
    
    # 2. Supprimer images 4-6
    print("2️⃣  Suppression des images 4-6 de Git...")
    success, files_list, _ = run_command("git ls-files | grep 'image_[4-6]'", check=False)
    if success and files_list.strip():
        files = files_list.strip().split('\n')
        print(f"   📊 {len(files)} images 4-6 trouvées")
        
        # Supprimer par lots de 100
        batch_size = 100
        total_deleted = 0
        for i in range(0, len(files), batch_size):
            batch = files[i:i+batch_size]
            cmd = f"git rm --cached {' '.join([f'\"{f}\"' for f in batch])}"
            success, output, error = run_command(cmd, check=False)
            if success:
                deleted = output.count("rm '")
                total_deleted += deleted
                print(f"   ✅ Lot {i//batch_size + 1}: {deleted} images supprimées")
            else:
                print(f"   ⚠️  Erreur dans le lot {i//batch_size + 1}: {error[:100]}")
        
        print(f"   ✅ Total: {total_deleted} images supprimées de l'index")
    else:
        print("   ℹ️  Aucune image 4-6 trouvée")
    print()
    
    # 3. Vérifier l'index
    print("3️⃣  Vérification de l'index...")
    success, status, _ = run_command("git status --short", check=False)
    if success:
        staged_files = [line for line in status.split('\n') if line.startswith('D ')]
        print(f"   ✅ {len(staged_files)} fichiers marqués pour suppression")
    print()
    
    # 4. Créer le commit
    print("4️⃣  Création du commit...")
    commit_msg = "Remove dist/ folder and limit images to 3 per product (remove images 4-6)"
    success, output, error = run_command(f'git commit -m "{commit_msg}"', check=False)
    if success:
        print("   ✅ Commit créé avec succès!")
        print(f"   📝 Message: {commit_msg}")
    else:
        if "nothing to commit" in error.lower():
            print("   ⚠️  Rien à commiter (les suppressions sont peut-être déjà commitées)")
        else:
            print(f"   ❌ Erreur: {error[:200]}")
    print()
    
    # 5. Vérifier le nouveau total
    print("5️⃣  Vérification du nouveau total...")
    success, output, _ = run_command("git ls-files | wc -l", check=False)
    if success:
        total = int(output.strip())
        print(f"   📊 Nouveau total: {total} fichiers")
        if total < 20000:
            print("   ✅ SOUS la limite de 20,000!")
        else:
            print(f"   ⚠️  Toujours au-dessus de 20,000 (il faut supprimer {total - 20000} fichiers de plus)")
    print()
    
    print("=" * 70)
    print("✅ TERMINÉ!")
    print("=" * 70)
    print()
    print("💡 Pour pousser vers GitHub:")
    print("   python3 update_github_auto.py")
    print()

if __name__ == '__main__':
    main()

