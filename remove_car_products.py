#!/usr/bin/env python3
"""
Script pour supprimer les 202 produits liés aux voitures de all_products.csv
pour toutes les langues (racine, fr, de, etc.).
"""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent
CAR_PRODUCTS_CSV = BASE_DIR / 'CSV' / 'products_voiture_auto.csv'

def detect_delimiter(file_path):
    """Détecte automatiquement le séparateur CSV."""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','

def load_car_product_ids():
    """Charge les product_id des produits auto/voiture à supprimer."""
    product_ids = set()
    
    if not CAR_PRODUCTS_CSV.exists():
        print(f"❌ Fichier non trouvé: {CAR_PRODUCTS_CSV}")
        return product_ids
    
    delimiter = detect_delimiter(CAR_PRODUCTS_CSV)
    
    with open(CAR_PRODUCTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            product_id = row.get('product_id', '').strip()
            if product_id:
                product_ids.add(product_id)
    
    return product_ids

def remove_products_from_csv(csv_file, product_ids_to_remove):
    """Supprime les produits spécifiés d'un fichier CSV."""
    if not csv_file.exists():
        print(f"  ⚠️  Fichier non trouvé: {csv_file}")
        return 0
    
    delimiter = detect_delimiter(csv_file)
    
    # Lire tous les produits
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
    
    # Écrire le CSV sans les produits supprimés
    if removed_count > 0:
        backup_file = csv_file.with_suffix(csv_file.suffix + '.backup_before_remove_cars')
        if not backup_file.exists():
            import shutil
            shutil.copy2(csv_file, backup_file)
            print(f"  💾 Sauvegarde créée: {backup_file.name}")
        
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(products)
    
    return removed_count

def remove_product_pages(product_ids_to_remove, lang_dir=None):
    """Supprime les pages HTML des produits spécifiés."""
    if lang_dir:
        products_dir = lang_dir / 'page_html' / 'products'
    else:
        products_dir = BASE_DIR / 'page_html' / 'products'
    
    if not products_dir.exists():
        return 0
    
    removed_count = 0
    for product_id in product_ids_to_remove:
        page_file = products_dir / f'produit-{product_id}.html'
        if page_file.exists():
            page_file.unlink()
            removed_count += 1
    
    return removed_count

def remove_product_images(product_ids_to_remove):
    """Supprime les dossiers d'images des produits spécifiés."""
    images_dir = BASE_DIR / 'images' / 'products'
    
    if not images_dir.exists():
        return 0
    
    removed_count = 0
    for product_id in product_ids_to_remove:
        product_image_dir = images_dir / str(product_id)
        if product_image_dir.exists():
            import shutil
            shutil.rmtree(product_image_dir)
            removed_count += 1
    
    return removed_count

def main():
    print("=" * 70)
    print("🗑️  SUPPRESSION DES PRODUITS AUTO/VOITURE")
    print("=" * 70)
    print()
    
    # 1. Charger les product_id à supprimer
    print("📖 Chargement des produits auto/voiture à supprimer...")
    product_ids_to_remove = load_car_product_ids()
    print(f"✅ {len(product_ids_to_remove)} produits identifiés")
    print()
    
    if not product_ids_to_remove:
        print("❌ Aucun produit à supprimer")
        return False
    
    # 2. Supprimer des CSV (racine, fr, de, etc.)
    print("📝 Suppression des produits dans les CSV...")
    print("-" * 70)
    
    csv_files = [
        BASE_DIR / 'CSV' / 'all_products.csv',
        BASE_DIR / 'fr' / 'CSV' / 'all_products.csv',
        BASE_DIR / 'de' / 'CSV' / 'all_products.csv',
    ]
    
    total_removed_from_csv = 0
    for csv_file in csv_files:
        if csv_file.exists():
            removed = remove_products_from_csv(csv_file, product_ids_to_remove)
            total_removed_from_csv += removed
            print(f"  ✅ {csv_file.parent.name}/CSV/all_products.csv: {removed} produits supprimés")
        else:
            print(f"  ⚠️  {csv_file.parent.name}/CSV/all_products.csv: fichier non trouvé")
    
    print()
    
    # 3. Supprimer les pages HTML (racine, fr, de)
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
    
    # 4. Supprimer les images
    print("🖼️  Suppression des images...")
    removed_images = remove_product_images(product_ids_to_remove)
    print(f"  ✅ {removed_images} dossiers d'images supprimés")
    print()
    
    # 5. Résumé
    print("=" * 70)
    print("✅ SUPPRESSION TERMINÉE!")
    print("=" * 70)
    print()
    print(f"📊 Résumé:")
    print(f"   • Produits supprimés des CSV: {total_removed_from_csv}")
    print(f"   • Pages HTML supprimées: {total_removed_pages}")
    print(f"   • Dossiers d'images supprimés: {removed_images}")
    print()
    print("💡 Prochaines étapes:")
    print("   1. Régénérer les pages: python3 generate_all_languages_with_domain_update.py")
    print("   2. Supprimer de Git: git rm page_html/products/produit-*.html (pour les produits supprimés)")
    print("   3. Pousser vers GitHub: python3 update_github_auto.py")
    print()

if __name__ == '__main__':
    main()

