#!/usr/bin/env python3
"""
Script complet pour changer le domaine du site.

Ce script :
1. Vérifie que le domaine est bien changé dans tous les CSV
2. Lance generate_all_languages_with_domain_update.py
3. Lance generate_sitemaps.py

Usage:
    python3 change_domain_complete.py [NOUVEAU_DOMAINE]
    
Si NOUVEAU_DOMAINE n'est pas fourni, le script vérifie juste que le domaine est cohérent dans tous les CSV.
"""

import csv
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

CSV_FILES = [
    BASE_DIR / 'translations.csv',
    BASE_DIR / 'fr' / 'translations.csv',
    BASE_DIR / 'de' / 'translations.csv',
    BASE_DIR / 'es' / 'translations.csv',
    BASE_DIR / 'pt' / 'translations.csv',
]

def get_domain_from_csv(csv_file):
    """Récupère le domaine depuis un CSV."""
    if not csv_file.exists():
        return None
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row.get('key', '').strip()
                if key == 'site.domain':
                    # Prendre la première colonne non-vide (après 'key' et 'description')
                    for col in row.keys():
                        if col not in ['key', 'description']:
                            domain = row.get(col, '').strip()
                            if domain and not domain.startswith('='):
                                return domain.rstrip('/')
    except Exception as e:
        print(f"  ⚠️  Erreur lecture {csv_file.name}: {e}")
    
    return None

def check_domains():
    """Vérifie que tous les CSV ont le même domaine."""
    print("=" * 70)
    print("🔍 VÉRIFICATION DES DOMAINES DANS LES CSV")
    print("=" * 70)
    print()
    
    domains = {}
    for csv_file in CSV_FILES:
        domain = get_domain_from_csv(csv_file)
        if domain:
            domains[csv_file.name] = domain
            print(f"  ✅ {csv_file.name}: {domain}")
        else:
            print(f"  ⚠️  {csv_file.name}: domaine non trouvé")
    
    if not domains:
        print("\n❌ Aucun domaine trouvé dans les CSV")
        return False
    
    # Vérifier que tous les domaines sont identiques
    unique_domains = set(domains.values())
    if len(unique_domains) == 1:
        domain = list(unique_domains)[0]
        print(f"\n✅ Tous les CSV utilisent le même domaine: {domain}")
        return True
    else:
        print(f"\n⚠️  ATTENTION: Les CSV ont des domaines différents!")
        for csv_name, domain in domains.items():
            print(f"  - {csv_name}: {domain}")
        print("\n⚠️  Corrigez les CSV avant de continuer.")
        return False

def main():
    """Fonction principale."""
    if len(sys.argv) > 1:
        new_domain = sys.argv[1]
        print(f"⚠️  Ce script ne modifie pas automatiquement les CSV.")
        print(f"    Modifiez manuellement 'site.domain' dans tous les CSV avant de continuer.")
        print(f"    Nouveau domaine souhaité: {new_domain}")
        print()
        return
    
    # Vérifier les domaines
    if not check_domains():
        print("\n❌ Vérification échouée. Corrigez les CSV avant de continuer.")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("🚀 LANCEMENT DE LA GÉNÉRATION COMPLÈTE")
    print("=" * 70)
    print()
    
    # Étape 1: Générer toutes les pages + mettre à jour les domaines
    print("📄 Étape 1: Génération des pages + Mise à jour des domaines...")
    print()
    result1 = subprocess.run(
        [sys.executable, str(BASE_DIR / 'generate_all_languages_with_domain_update.py')],
        cwd=BASE_DIR
    )
    
    if result1.returncode != 0:
        print("\n❌ Échec de la génération")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print()
    
    # Étape 2: Régénérer les sitemaps
    print("📄 Étape 2: Régénération des sitemaps...")
    print()
    result2 = subprocess.run(
        [sys.executable, str(BASE_DIR / 'generate_sitemaps.py')],
        cwd=BASE_DIR
    )
    
    if result2.returncode != 0:
        print("\n❌ Échec de la génération des sitemaps")
        sys.exit(1)
    
    print()
    print("=" * 70)
    print("✅ TERMINÉ !")
    print("=" * 70)
    print()
    print("📝 Prochaine étape (optionnelle):")
    print("   python3 update_github_auto.py \"Update: Changement domaine\"")
    print()

if __name__ == '__main__':
    main()

