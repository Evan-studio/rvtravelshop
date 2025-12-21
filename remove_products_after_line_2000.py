#!/usr/bin/env python3
"""
Script pour supprimer tous les produits qui dépassent la ligne 2000 dans le CSV,
ainsi que leurs dossiers d'images et pages HTML associées.
"""

import csv
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / 'CSV' / 'all_products.csv'
IMAGES_DIR = BASE_DIR / 'images' / 'products'
MAX_LINES = 2000  # Garder seulement les 2000 premiers produits

def detect_delimiter(file_path):
    """Détecte automatiquement le séparateur CSV."""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','

def find_language_directories():
    """Trouve tous les dossiers de langues."""
    lang_dirs = []
    for item in BASE_DIR.iterdir():
        if item.is_dir() and len(item.name) == 2 and item.name.isalpha():
            lang_dirs.append(item)
    return lang_dirs

def remove_products_after_line(csv_file, max_lines):
    """Supprime les produits après la ligne max_lines et retourne les product_id supprimés."""
    if not csv_file.exists():
        return []
    
    delimiter = detect_delimiter(csv_file)
    products_to_keep = []
    products_to_remove = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        fieldnames = reader.fieldnames
        
        for line_num, row in enumerate(reader, start=2):  # start=2 car ligne 1 = header
            if line_num <= max_lines + 1:  # +1 car on compte la ligne header
                products_to_keep.append(row)
            else:
                product_id = row.get('product_id', '').strip()
                if product_id:
                    products_to_remove.append(product_id)
    
    if products_to_remove:
        # Créer une sauvegarde
        backup_file = csv_file.with_suffix(csv_file.suffix + '.backup_before_remove_after_2000')
        if not backup_file.exists():
            shutil.copy2(csv_file, backup_file)
        
        # Réécrire le CSV avec seulement les produits à garder
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(products_to_keep)
    
    return products_to_remove

def remove_product_images(product_ids):
    """Supprime les dossiers d'images des produits spécifiés."""
    removed_count = 0
    
    for product_id in product_ids:
        product_image_dir = IMAGES_DIR / str(product_id)
        if product_image_dir.exists():
            try:
                shutil.rmtree(product_image_dir)
                removed_count += 1
            except Exception as e:
                print(f"  ⚠️  Erreur lors de la suppression de {product_id}: {e}")
    
    return removed_count

def remove_product_html_pages(product_ids, lang_dir=None):
    """Supprime les pages HTML des produits spécifiés pour une langue donnée."""
    if lang_dir:
        products_dir = lang_dir / 'page_html' / 'products'
    else:
        products_dir = BASE_DIR / 'page_html' / 'products'
    
    if not products_dir.exists():
        return 0
    
    removed_count = 0
    for product_id in product_ids:
        page_file = products_dir / f'produit-{product_id}.html'
        if page_file.exists():
            page_file.unlink()
            removed_count += 1
    
    return removed_count

def main():
    print("=" * 70)
    print("🗑️  SUPPRESSION DES PRODUITS APRÈS LA LIGNE 2000")
    print("=" * 70)
    print()
    
    if not CSV_FILE.exists():
        print(f"❌ Fichier CSV non trouvé: {CSV_FILE}")
        return False
    
    # Compter le nombre total de produits avant suppression
    delimiter = detect_delimiter(CSV_FILE)
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        total_before = sum(1 for _ in reader)
    
    print(f"📊 Produits dans le CSV avant suppression: {total_before}")
    print(f"📊 Produits à garder (lignes 2-{MAX_LINES + 1}): {MAX_LINES}")
    print(f"📊 Produits à supprimer: {max(0, total_before - MAX_LINES)}")
    print()
    
    # 1. Supprimer les produits des CSV
    print("📝 Suppression des produits dans les CSV...")
    print("-" * 70)
    
    # Traiter le CSV racine
    products_to_remove = remove_products_after_line(CSV_FILE, MAX_LINES)
    print(f"  ✅ racine/CSV/all_products.csv: {len(products_to_remove)} produits supprimés")
    
    # Traiter les CSV de langues
    lang_dirs = find_language_directories()
    for lang_dir in lang_dirs:
        lang_csv = lang_dir / 'CSV' / 'all_products.csv'
        if lang_csv.exists():
            removed = remove_products_after_line(lang_csv, MAX_LINES)
            print(f"  ✅ {lang_dir.name}/CSV/all_products.csv: {len(removed)} produits supprimés")
    
    print()
    
    if not products_to_remove:
        print("✅ Aucun produit à supprimer!")
        return True
    
    print(f"📊 Total de produits à supprimer: {len(products_to_remove)}")
    print()
    
    # 2. Supprimer les pages HTML
    print("🗑️  Suppression des pages HTML...")
    print("-" * 70)
    
    total_removed_pages = 0
    
    # Racine
    removed_root = remove_product_html_pages(products_to_remove)
    total_removed_pages += removed_root
    if removed_root > 0:
        print(f"  ✅ racine: {removed_root} pages supprimées")
    
    # Langues
    for lang_dir in lang_dirs:
        removed_lang = remove_product_html_pages(products_to_remove, lang_dir)
        total_removed_pages += removed_lang
        if removed_lang > 0:
            print(f"  ✅ {lang_dir.name}: {removed_lang} pages supprimées")
    
    print()
    
    # 3. Supprimer les dossiers d'images
    print("🖼️  Suppression des dossiers d'images...")
    print("-" * 70)
    removed_images = remove_product_images(products_to_remove)
    print(f"  ✅ {removed_images} dossiers d'images supprimés")
    print()
    
    # 4. Vérifier le nombre final
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        total_after = sum(1 for _ in reader)
    
    print("=" * 70)
    print("✅ SUPPRESSION TERMINÉE!")
    print("=" * 70)
    print()
    print(f"📊 Résumé:")
    print(f"   • Produits avant: {total_before}")
    print(f"   • Produits après: {total_after}")
    print(f"   • Produits supprimés: {len(products_to_remove)}")
    print(f"   • Pages HTML supprimées: {total_removed_pages}")
    print(f"   • Dossiers d'images supprimés: {removed_images}")
    print()
    print("💡 Prochaines étapes:")
    print("   1. Supprimer de Git: git rm page_html/products/produit-*.html (pour les produits supprimés)")
    print("   2. Régénérer les pages: python3 generate_all_languages_with_domain_update.py")
    print("   3. Pousser vers GitHub: python3 update_github_auto.py")
    print()

if __name__ == '__main__':
    main()

