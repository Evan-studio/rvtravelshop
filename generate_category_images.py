#!/usr/bin/env python3
"""
Script pour générer les images de catégories (1.webp à 6.webp)
depuis les images des produits dans all_products.csv

- Trouve un produit aléatoire pour chaque catégorie (1-6)
- Prend la première image de ce produit
- Redimensionne et optimise pour le SEO Google
- Sauvegarde dans images/categories/{cat_id}.webp
"""

import csv
import random
import shutil
from pathlib import Path
from PIL import Image
import sys

BASE_DIR = Path(__file__).parent
PRODUCTS_CSV = BASE_DIR / 'CSV' / 'all_products.csv'
CATEGORIES_DIR = BASE_DIR / 'images' / 'categories'
IMAGES_PRODUCTS_DIR = BASE_DIR / 'images' / 'products'
IMAGES_BASE_DIR = BASE_DIR / 'APPLI:SCRIPT aliexpress' / 'APP IMPORT ALIEXPRESS' / 'images'

# Dimensions adaptées à l'affichage dans index.html (ratio 4/3 comme défini dans le CSS)
# Les images sont affichées avec aspect-ratio: 4/3 et minmax(180px, 1fr)
# On utilise 400x300px pour un bon compromis qualité/taille
CATEGORY_WIDTH = 400
CATEGORY_HEIGHT = 300

def detect_csv_delimiter(file_path):
    """Détecte automatiquement le séparateur CSV"""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','

def load_products_by_category():
    """Charge les produits depuis all_products.csv et les groupe par catégorie"""
    products_by_category = {i: [] for i in range(1, 7)}
    
    if not PRODUCTS_CSV.exists():
        print(f"❌ Fichier non trouvé: {PRODUCTS_CSV}")
        return products_by_category
    
    delimiter = detect_csv_delimiter(PRODUCTS_CSV)
    
    try:
        with open(PRODUCTS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                try:
                    category_id = int(row.get('category_id', 0))
                    if 1 <= category_id <= 6:
                        product_id = row.get('product_id', '').strip()
                        image_paths = row.get('image_paths', '').strip()
                        if product_id and image_paths:
                            products_by_category[category_id].append({
                                'product_id': product_id,
                                'image_paths': image_paths
                            })
                except (ValueError, TypeError):
                    continue
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du CSV: {e}")
        return products_by_category
    
    return products_by_category

def extract_first_image_path(image_paths_str):
    """Extrait le premier chemin d'image depuis la chaîne image_paths"""
    if not image_paths_str:
        return None
    
    # Les images sont séparées par |
    images = image_paths_str.split('|')
    for img_path in images:
        img_path = img_path.strip()
        if img_path:
            # Convertir le chemin absolu en Path
            return Path(img_path)
    
    return None

def find_product_image(product_id, image_paths_str):
    """Trouve la première image d'un produit"""
    # Nettoyer le product_id
    clean_product_id = str(product_id).strip().lstrip("'")
    
    # 1. Essayer d'abord dans images/products/ (emplacement standard)
    product_dir = IMAGES_PRODUCTS_DIR / clean_product_id
    if product_dir.exists():
        # Chercher image_1.webp, image_1.jpg, etc.
        for ext in ['webp', 'jpg', 'jpeg', 'png']:
            for num in range(1, 10):
                img_file = product_dir / f'image_{num}.{ext}'
                if img_file.exists():
                    return img_file
    
    # 2. Essayer avec le chemin du CSV (chemin absolu)
    if image_paths_str:
        first_image = extract_first_image_path(image_paths_str)
        if first_image and first_image.exists():
            return first_image
    
    # 3. Essayer dans l'ancien emplacement
    product_dir = IMAGES_BASE_DIR / clean_product_id
    if product_dir.exists():
        for ext in ['webp', 'jpg', 'jpeg', 'png']:
            for num in range(1, 10):
                img_file = product_dir / f'image_{num}.{ext}'
                if img_file.exists():
                    return img_file
    
    return None

def resize_and_optimize_image(source_path, output_path, width=CATEGORY_WIDTH, height=CATEGORY_HEIGHT):
    """Redimensionne et optimise une image pour le SEO"""
    try:
        with Image.open(source_path) as img:
            # Convertir en RGB si nécessaire (pour les PNG avec transparence)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Créer un fond blanc
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculer les dimensions en gardant le ratio
            original_width, original_height = img.size
            ratio = min(width / original_width, height / original_height)
            
            # Redimensionner en gardant le ratio
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Créer une image de la taille cible avec fond blanc
            final_img = Image.new('RGB', (width, height), (255, 255, 255))
            
            # Centrer l'image redimensionnée
            x_offset = (width - new_width) // 2
            y_offset = (height - new_height) // 2
            final_img.paste(img_resized, (x_offset, y_offset))
            
            # Sauvegarder en WebP avec optimisation
            final_img.save(
                output_path,
                'WEBP',
                quality=85,  # Bon compromis qualité/taille
                method=6,     # Meilleure compression
                optimize=True
            )
            
            return True
    except Exception as e:
        print(f"      ❌ Erreur lors du traitement de l'image: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 70)
    print("🖼️  GÉNÉRATION DES IMAGES DE CATÉGORIES")
    print("=" * 70)
    print()
    
    # Créer le dossier categories s'il n'existe pas
    CATEGORIES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Dossier de sortie: {CATEGORIES_DIR}")
    print()
    
    # Charger les produits par catégorie
    print("📖 Chargement des produits depuis all_products.csv...")
    products_by_category = load_products_by_category()
    
    total_products = sum(len(products) for products in products_by_category.values())
    print(f"✅ {total_products} produits chargés")
    print()
    
    # Afficher le nombre de produits par catégorie
    for cat_id in range(1, 7):
        count = len(products_by_category[cat_id])
        print(f"   Catégorie {cat_id}: {count} produit(s)")
    print()
    
    # Générer les images pour chaque catégorie
    print("=" * 70)
    print("🔄 GÉNÉRATION DES IMAGES")
    print("=" * 70)
    print()
    
    success_count = 0
    failed_count = 0
    
    for cat_id in range(1, 7):
        print(f"📦 Catégorie {cat_id}...")
        
        products = products_by_category[cat_id]
        if not products:
            print(f"   ⚠️  Aucun produit trouvé pour la catégorie {cat_id}")
            failed_count += 1
            continue
        
        # Sélectionner un produit aléatoire
        selected_product = random.choice(products)
        product_id = selected_product['product_id']
        image_paths = selected_product['image_paths']
        
        print(f"   → Produit sélectionné: {product_id}")
        
        # Trouver la première image
        source_image = find_product_image(product_id, image_paths)
        
        if not source_image:
            print(f"   ❌ Aucune image trouvée pour le produit {product_id}")
            failed_count += 1
            continue
        
        if not source_image.exists():
            print(f"   ❌ Image introuvable: {source_image}")
            failed_count += 1
            continue
        
        print(f"   → Image source: {source_image.name}")
        
        # Chemin de sortie
        output_path = CATEGORIES_DIR / f"{cat_id}.webp"
        
        # Redimensionner et optimiser
        print(f"   → Redimensionnement ({CATEGORY_WIDTH}x{CATEGORY_HEIGHT}px)...")
        if resize_and_optimize_image(source_image, output_path):
            # Vérifier la taille du fichier
            file_size = output_path.stat().st_size / 1024  # KB
            print(f"   ✅ Image créée: {output_path.name} ({file_size:.1f} KB)")
            success_count += 1
        else:
            print(f"   ❌ Échec de la création de l'image")
            failed_count += 1
        
        print()
    
    # Résumé
    print("=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    print(f"✅ Images créées avec succès: {success_count}/6")
    print(f"❌ Échecs: {failed_count}/6")
    print()
    
    if success_count == 6:
        print("🎉 Toutes les images de catégories ont été générées avec succès!")
        print()
        print("💡 Les images sont optimisées pour l'affichage:")
        print(f"   • Dimensions: {CATEGORY_WIDTH}x{CATEGORY_HEIGHT}px (ratio 4/3)")
        print(f"   • Format: WebP")
        print(f"   • Qualité: 85%")
        print(f"   • Compression: Optimisée")
        print(f"   • Adapté à l'affichage dans index.html (aspect-ratio: 4/3)")
    else:
        print("⚠️  Certaines images n'ont pas pu être générées.")
        print("   Vérifiez que les produits ont des images valides.")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interruption par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

