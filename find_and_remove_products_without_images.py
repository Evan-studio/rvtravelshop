#!/usr/bin/env python3
"""
Script pour trouver les produits qui ont des pages HTML mais pas d'images
et les supprimer des CSV et des pages HTML.
"""

import csv
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / 'CSV' / 'all_products.csv'
PRODUCTS_HTML_DIR = BASE_DIR / 'page_html' / 'products'
IMAGES_DIR = BASE_DIR / 'images' / 'products'

CSV_FILES = [
    BASE_DIR / 'CSV' / 'all_products.csv',
    BASE_DIR / 'fr' / 'CSV' / 'all_products.csv',
    BASE_DIR / 'de' / 'CSV' / 'all_products.csv',
]

def detect_delimiter(file_path):
    """Détecte automatiquement le séparateur CSV."""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','

def find_products_with_html_but_no_images():
    """Trouve les produits qui ont des pages HTML mais pas d'images."""
    products_to_remove = []
    
    if not CSV_FILE.exists():
        print(f"❌ Fichier CSV non trouvé: {CSV_FILE}")
        return products_to_remove
    
    delimiter = detect_delimiter(CSV_FILE)
    
    print("🔍 Recherche des produits avec page HTML mais SANS images...")
    print("-" * 70)
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            product_id = row.get('product_id', '').strip()
            if not product_id:
                continue
            
            # Vérifier si la page HTML existe
            html_file = PRODUCTS_HTML_DIR / f'produit-{product_id}.html'
            has_html = html_file.exists()
            
            # Vérifier si le dossier d'images existe et contient des images
            image_dir = IMAGES_DIR / product_id
            has_images = False
            if image_dir.exists():
                # Vérifier s'il y a des fichiers image
                image_files = list(image_dir.glob('*.webp')) + \
                             list(image_dir.glob('*.jpg')) + \
                             list(image_dir.glob('*.jpeg')) + \
                             list(image_dir.glob('*.png'))
                has_images = len(image_files) > 0
            
            if has_html and not has_images:
                products_to_remove.append({
                    'product_id': product_id,
                    'name': row.get('name', row.get('titre', ''))[:60]
                })
                print(f"  ❌ {product_id}: page HTML existe mais pas d'images")
    
    print()
    print(f"✅ {len(products_to_remove)} produits trouvés")
    print()
    
    return [p['product_id'] for p in products_to_remove]

def remove_products_from_csv(csv_file, product_ids_to_remove):
    """Supprime les produits spécifiés d'un fichier CSV."""
    if not csv_file.exists():
        return 0
    
    delimiter = detect_delimiter(csv_file)
    
    products = []
    removed_count = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        fieldnames = reader.fieldnames
        
        for row in reader:
            product_id = row.get('product_id', '').strip()
            if product_id not in product_ids_to_remove:
                products.append(row)
            else:
                removed_count += 1
    
    if removed_count > 0:
        backup_file = csv_file.with_suffix(csv_file.suffix + '.backup_before_remove_no_images')
        if not backup_file.exists():
            shutil.copy2(csv_file, backup_file)
        
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(products)
    
    return removed_count

def remove_product_pages(product_ids, lang_dir=None):
    """Supprime les pages HTML des produits spécifiés."""
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
    print("🗑️  SUPPRESSION DES PRODUITS AVEC PAGE HTML MAIS SANS IMAGES")
    print("=" * 70)
    print()
    
    # 1. Trouver les produits
    product_ids_to_remove = find_products_with_html_but_no_images()
    
    if not product_ids_to_remove:
        print("✅ Tous les produits avec des pages HTML ont des images!")
        return True
    
    print(f"📊 {len(product_ids_to_remove)} produits à supprimer")
    print()
    
    # 2. Supprimer des CSV
    print("📝 Suppression des produits dans les CSV...")
    print("-" * 70)
    
    total_removed_from_csv = 0
    for csv_file in CSV_FILES:
        if csv_file.exists():
            removed = remove_products_from_csv(csv_file, product_ids_to_remove)
            total_removed_from_csv += removed
            lang_name = csv_file.parent.name if csv_file.parent.name != 'CSV' else 'racine'
            print(f"  ✅ {lang_name}/CSV/all_products.csv: {removed} produits supprimés")
        else:
            print(f"  ⚠️  {csv_file}: fichier non trouvé")
    
    print()
    
    # 3. Supprimer les pages HTML
    print("🗑️  Suppression des pages HTML...")
    print("-" * 70)
    
    lang_dirs = [None, BASE_DIR / 'fr', BASE_DIR / 'de']
    total_removed_pages = 0
    
    for lang_dir in lang_dirs:
        lang_name = lang_dir.name if lang_dir else 'racine'
        removed = remove_product_pages(product_ids_to_remove, lang_dir)
        total_removed_pages += removed
        if removed > 0:
            print(f"  ✅ {lang_name}: {removed} pages supprimées")
    
    print()
    
    # 4. Résumé
    print("=" * 70)
    print("✅ SUPPRESSION TERMINÉE!")
    print("=" * 70)
    print()
    print(f"📊 Résumé:")
    print(f"   • Produits trouvés: {len(product_ids_to_remove)}")
    print(f"   • Produits supprimés des CSV: {total_removed_from_csv}")
    print(f"   • Pages HTML supprimées: {total_removed_pages}")
    print()
    print("💡 Prochaines étapes:")
    print("   1. Supprimer de Git: git rm page_html/products/produit-*.html (pour les produits supprimés)")
    print("   2. Pousser vers GitHub: python3 update_github_auto.py")
    print()

if __name__ == '__main__':
    main()


