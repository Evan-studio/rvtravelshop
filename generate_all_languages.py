#!/usr/bin/env python3
"""
Script master pour régénérer TOUT le site dans toutes les langues.

Ce script exécute dans l'ordre pour chaque langue :
1. update_index_template.py - Met à jour index.html
2. generate_and_check_menu_footer_pages.py - Génère les pages catégories et légales
3. generate_all_product_pages.py - Génère toutes les pages produits

Usage:
    python3 generate_all_languages.py
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Configuration des langues
LANGUAGES = [
    {
        'code': 'en',
        'name': 'Anglais',
        'script': BASE_DIR / 'generate_all_en.py',
        'dir': BASE_DIR
    },
    {
        'code': 'fr',
        'name': 'Français',
        'script': BASE_DIR / 'fr' / 'scripts' / 'generate_all_fr.py',
        'dir': BASE_DIR / 'fr'
    },
    {
        'code': 'de',
        'name': 'Allemand',
        'script': BASE_DIR / 'de' / 'scripts' / 'generate_all_de.py',
        'dir': BASE_DIR / 'de'
    },
    {
        'code': 'es',
        'name': 'Espagnol',
        'script': BASE_DIR / 'es' / 'scripts' / 'generate_all_es.py',
        'dir': BASE_DIR / 'es'
    },
    {
        'code': 'pt',
        'name': 'Portugais',
        'script': BASE_DIR / 'pt' / 'scripts' / 'generate_all_pt.py',
        'dir': BASE_DIR / 'pt'
    }
]

def run_script(script_path, lang_name):
    """Exécute un script de génération."""
    if not script_path.exists():
        print(f"  ⚠️  Script non trouvé: {script_path}")
        return False
    
    try:
        print(f"  📄 Exécution de {script_path.name}...")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"  ✅ {lang_name} - Terminé avec succès")
            return True
        else:
            print(f"  ❌ {lang_name} - Erreur:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"  ❌ {lang_name} - Exception: {e}")
        return False

def main():
    """Fonction principale."""
    print("=" * 70)
    print("🌍 RÉGÉNÉRATION COMPLÈTE DU SITE - TOUTES LES LANGUES")
    print("=" * 70)
    print()
    
    success_count = 0
    total_count = len(LANGUAGES)
    
    for lang in LANGUAGES:
        print(f"\n{'=' * 70}")
        print(f"🌐 {lang['name'].upper()} ({lang['code']})")
        print(f"{'=' * 70}")
        
        if run_script(lang['script'], lang['name']):
            success_count += 1
        else:
            print(f"  ⚠️  Échec pour {lang['name']}")
    
    print()
    print("=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    print(f"✅ Réussi: {success_count}/{total_count}")
    print(f"❌ Échoué: {total_count - success_count}/{total_count}")
    print()
    
    if success_count == total_count:
        print("🎉 Toutes les langues ont été régénérées avec succès !")
        print()
        print("📝 Prochaines étapes:")
        print("  1. Régénérer les sitemaps: python3 generate_sitemaps.py")
        print("  2. Vérifier les fichiers générés")
        print("  3. Déployer: python3 update_github_auto.py")
    else:
        print("⚠️  Certaines langues ont échoué. Vérifiez les erreurs ci-dessus.")
        sys.exit(1)

if __name__ == '__main__':
    main()

