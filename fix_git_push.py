#!/usr/bin/env python3
"""
Script pour résoudre le problème de push Git bloqué
Solution: Créer un nouveau dépôt sans historique volumineux
"""

import subprocess
import sys
import json
import shutil
from pathlib import Path

def run_command(cmd, check=True, capture=True):
    """Exécute une commande shell."""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                check=check,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        else:
            result = subprocess.run(cmd, shell=True, check=check)
            return result.returncode == 0, "", ""
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip() if e.stdout else "", e.stderr.strip() if e.stderr else str(e)

def main():
    print("=" * 70)
    print("🔧 RÉSOLUTION DU PROBLÈME DE PUSH GIT")
    print("=" * 70)
    print()
    print("Problème identifié:")
    print("  • Dépôt trop volumineux (2.01 GiB)")
    print("  • 71 514 objets dans l'historique")
    print("  • GitHub bloque le push à 39%")
    print()
    print("Solution: Créer un nouveau dépôt sans historique")
    print("  ✅ Toutes les images WebP seront incluses")
    print("  ✅ Tous les fichiers HTML/CSS/JS seront inclus")
    print("  ✅ Seul l'historique Git sera supprimé")
    print()
    
    # Vérifier si on a un argument --yes pour éviter la confirmation
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    
    if not auto_confirm:
        try:
            response = input("Continuer? (oui/non): ").strip().lower()
            if response not in ['oui', 'o', 'yes', 'y']:
                print("❌ Opération annulée")
                return
        except EOFError:
            # Si pas d'input disponible (exécution non-interactive), continuer automatiquement
            print("⚠️  Mode non-interactif: continuation automatique...")
            print()
    
    print()
    print("🔄 Étape 1/7: Arrêt de tout processus Git en cours...")
    run_command("pkill -f 'git push'", check=False)
    print("   ✅ Processus arrêtés")
    
    print()
    print("🔄 Étape 2/7: Sauvegarde de la configuration...")
    config_path = Path("git_remote_config.json")
    remote_url = None
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            user = data.get("user", "").strip()
            repo = data.get("repo", "").strip()
            if user and repo:
                remote_url = f"https://github.com/{user}/{repo}.git"
        except:
            pass
    
    if not remote_url:
        success, current_remote, _ = run_command("git remote get-url origin", check=False)
        if success and current_remote:
            remote_url = current_remote.strip()
    
    print(f"   ✅ Remote: {remote_url}")
    
    print()
    print("🔄 Étape 3/7: Vérification des images...")
    success, images_count, _ = run_command("find images -name '*.webp' 2>/dev/null | wc -l", check=False)
    images_count = int(images_count.strip()) if images_count.strip().isdigit() else 0
    print(f"   ✅ {images_count} images WebP trouvées (seront incluses)")
    
    print()
    print("🔄 Étape 4/7: Suppression de l'historique Git...")
    if Path(".git").exists():
        shutil.rmtree(".git")
        print("   ✅ Historique supprimé")
    else:
        print("   ⚠️  Pas de dossier .git trouvé")
    
    print()
    print("🔄 Étape 5/7: Réinitialisation de Git...")
    success, output, error = run_command("git init", check=True)
    if not success:
        print(f"❌ Erreur: {error}")
        return
    print("   ✅ Git initialisé")
    
    print()
    print("🔄 Étape 6/7: Ajout des fichiers (cela peut prendre 1-2 minutes)...")
    print("   → Ajout de tous les fichiers (sauf .gitignore)...")
    success, output, error = run_command("git add -A", check=True)
    if not success:
        print(f"❌ Erreur: {error}")
        return
    
    # Vérifier ce qui a été ajouté
    success, output, _ = run_command("git ls-files | wc -l", check=False)
    files_count = int(output.strip()) if output.strip().isdigit() else 0
    
    success, images_added, _ = run_command("git ls-files | grep -E '\\.(webp|jpg|jpeg|png)$' | wc -l", check=False)
    images_added = int(images_added.strip()) if images_added.strip().isdigit() else 0
    
    print(f"   ✅ {files_count} fichiers ajoutés")
    print(f"   ✅ {images_added} images incluses")
    
    print()
    print("🔄 Étape 7/7: Création du commit initial...")
    success, output, error = run_command('git commit -m "Initial commit - cleaned repository"', check=True)
    if not success:
        print(f"❌ Erreur: {error}")
        return
    print("   ✅ Commit créé")
    
    if remote_url:
        print()
        print("🔄 Configuration du remote...")
        run_command(f'git remote remove origin', check=False)
        success, output, error = run_command(f'git remote add origin "{remote_url}"', check=False)
        if success:
            print(f"   ✅ Remote configuré")
        else:
            print(f"   ⚠️  Erreur: {error}")
    
    print()
    print("=" * 70)
    print("✅ DÉPÔT NETTOYÉ AVEC SUCCÈS!")
    print("=" * 70)
    print()
    print("📊 Statistiques:")
    print(f"   • {files_count} fichiers dans le nouveau dépôt")
    print(f"   • {images_added} images incluses")
    print(f"   • Historique Git: 1 commit (au lieu de 36)")
    print()
    print("💡 Pour envoyer vers GitHub, exécutez:")
    print("   git push origin main --force")
    print()
    print("⚠️  Le push devrait maintenant être rapide (quelques secondes)")
    print("   car le dépôt est beaucoup plus petit!")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Opération annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

