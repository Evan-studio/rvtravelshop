#!/usr/bin/env python3
"""
Script pour préparer les fichiers à uploader sur Hostinger
Crée un dossier avec tous les fichiers nécessaires
"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'hostinger_upload'

def main():
    """Prépare les fichiers pour Hostinger."""
    print("=" * 70)
    print("📦 PRÉPARATION DES FICHIERS POUR HOSTINGER")
    print("=" * 70)
    print()
    
    # Créer le dossier de sortie
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()
    
    files_to_copy = [
        # Sitemaps
        'sitemap.xml',
        'sitemap-all.xml',
        'sitemap-en.xml',
        'sitemap-fr.xml',
        'sitemap-de.xml',
        'sitemap-es.xml',
        'sitemap-pt.xml',
        
        # Configuration
        'robots.txt',
        '_headers',
        
        # Pages principales
        'index.html',
    ]
    
    print("📋 Copie des fichiers...")
    copied = 0
    
    for file_name in files_to_copy:
        source = BASE_DIR / file_name
        if source.exists():
            dest = OUTPUT_DIR / file_name
            shutil.copy2(source, dest)
            print(f"  ✅ {file_name}")
            copied += 1
        else:
            print(f"  ⚠️  {file_name} (non trouvé)")
    
    # Copier les dossiers de langue
    print()
    print("📁 Copie des dossiers de langue...")
    lang_dirs = ['fr', 'de', 'es', 'pt']
    
    for lang_dir in lang_dirs:
        source_dir = BASE_DIR / lang_dir
        if source_dir.exists():
            dest_dir = OUTPUT_DIR / lang_dir
            shutil.copytree(source_dir, dest_dir, ignore=shutil.ignore_patterns(
                '*.py', '*.pyc', '__pycache__', 'CSV', 'scripts', '*.template'
            ))
            print(f"  ✅ {lang_dir}/")
    
    # Copier les images (optionnel, peut être déjà sur Hostinger)
    print()
    print("🖼️  Copie des images...")
    images_dir = BASE_DIR / 'images'
    if images_dir.exists():
        dest_images = OUTPUT_DIR / 'images'
        shutil.copytree(images_dir, dest_images)
        print(f"  ✅ images/")
    
    # Copier page_html de la racine
    print()
    print("📄 Copie des pages HTML de la racine...")
    page_html_dir = BASE_DIR / 'page_html'
    if page_html_dir.exists():
        dest_page_html = OUTPUT_DIR / 'page_html'
        shutil.copytree(page_html_dir, dest_page_html)
        print(f"  ✅ page_html/")
    
    print()
    print("=" * 70)
    print(f"✅ TERMINÉ ! {copied} fichier(s) copié(s)")
    print("=" * 70)
    print()
    print(f"📁 Dossier créé : {OUTPUT_DIR}")
    print()
    print("📤 Prochaines étapes :")
    print("  1. Compressez le dossier 'hostinger_upload' en ZIP")
    print("  2. Uploadez sur Hostinger via FTP ou cPanel")
    print("  3. Testez le sitemap : https://votre-domaine.com/sitemap-all.xml")
    print("  4. Soumettez dans Google Search Console")
    print()

if __name__ == '__main__':
    main()

