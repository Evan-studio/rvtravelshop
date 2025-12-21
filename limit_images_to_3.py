#!/usr/bin/env python3
"""
Script pour limiter les images à 3 par produit (image_1, image_2, image_3).
Supprime les images image_4, image_5, image_6, etc.
"""

from pathlib import Path
import shutil

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / 'images' / 'products'
BACKUP_DIR = BASE_DIR / 'images' / 'products_backup_before_limit'

def limit_images_to_3():
    """Limite les images à 3 par produit."""
    print("=" * 70)
    print("🖼️  LIMITATION DES IMAGES À 3 PAR PRODUIT")
    print("=" * 70)
    print()
    
    if not IMAGES_DIR.exists():
        print(f"❌ Dossier non trouvé: {IMAGES_DIR}")
        return False
    
    # Créer une sauvegarde
    print("💾 Création d'une sauvegarde...")
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    shutil.copytree(IMAGES_DIR, BACKUP_DIR)
    print(f"✅ Sauvegarde créée: {BACKUP_DIR.name}/")
    print()
    
    # Parcourir les dossiers produits
    print("🔍 Analyse des images...")
    total_removed = 0
    products_modified = 0
    
    for product_dir in sorted(IMAGES_DIR.iterdir()):
        if not product_dir.is_dir():
            continue
        
        # Chercher toutes les images
        images_to_remove = []
        images_to_keep = []
        
        for i in range(1, 20):  # Chercher jusqu'à image_20
            for ext in ['webp', 'jpg', 'jpeg', 'png']:
                img_file = product_dir / f'image_{i}.{ext}'
                if img_file.exists():
                    if i <= 3:
                        images_to_keep.append(img_file)
                    else:
                        images_to_remove.append(img_file)
                    break
        
        # Supprimer les images au-delà de 3
        if images_to_remove:
            for img_file in images_to_remove:
                img_file.unlink()
                total_removed += 1
            products_modified += 1
            product_id = product_dir.name
            print(f"  ✅ {product_id}: {len(images_to_keep)} images gardées, {len(images_to_remove)} supprimées")
    
    print()
    print("=" * 70)
    print("✅ LIMITATION TERMINÉE!")
    print("=" * 70)
    print()
    print(f"📊 Statistiques:")
    print(f"   ✅ Produits modifiés: {products_modified}")
    print(f"   🗑️  Images supprimées: {total_removed}")
    print()
    print(f"💾 Sauvegarde disponible dans: {BACKUP_DIR.name}/")
    print()
    print("💡 Pour restaurer les images originales:")
    print(f"   rm -rf {IMAGES_DIR.name}/")
    print(f"   mv {BACKUP_DIR.name} {IMAGES_DIR.name}")
    print()
    
    return True

if __name__ == '__main__':
    limit_images_to_3()

