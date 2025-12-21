#!/usr/bin/env python3
"""
Script pour préparer les fichiers pour le déploiement Cloudflare Pages.
Copie seulement les fichiers nécessaires dans un dossier 'dist' pour respecter
la limite de 20,000 fichiers de Cloudflare Pages.
"""

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
DIST_DIR = BASE_DIR / 'dist'

# Extensions de fichiers à inclure
INCLUDE_EXTENSIONS = {
    '.html', '.css', '.js', '.json',
    '.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
    '.xml', '.txt', '.webmanifest',
    '.woff', '.woff2', '.ttf', '.eot', '.otf'
}

# Extensions à exclure explicitement
EXCLUDE_EXTENSIONS = {
    '.csv', '.py', '.pyc', '.pyo', '.pyd', '.log', '.md'
}

# Fichiers spécifiques à inclure (même sans extension)
INCLUDE_FILES = {
    'robots.txt', '_headers', '_redirects', 'favicon.ico'
}

# Dossiers à copier complètement
# NOTE: Les dossiers de langue (fr/, de/, etc.) sont exclus pour respecter la limite de 20,000 fichiers
# Les langues peuvent être ajoutées plus tard si nécessaire
INCLUDE_DIRS = {
    'images', 'page_html'
    # 'fr', 'de', 'es', 'it', 'pt', 'nl', 'ru', 'pl'  # Exclus temporairement
}

# Dossiers à exclure
EXCLUDE_DIRS = {
    'scripts', 'guides', 'APPLI:SCRIPT aliexpress', 'sauv',
    '__pycache__', '.git', 'node_modules', '.vscode', '.idea',
    'upload youtube', 'dist', '.git', 'CSV'
}

# Fichiers/dossiers à exclure même s'ils matchent les critères
EXCLUDE_PATTERNS = {
    '*.py', '*.pyc', '*.pyo', '*.pyd',
    '*.log', '*.backup', '*.backup*',
    '.DS_Store', '.gitignore', '.gitattributes'
}

def should_include_file(file_path: Path) -> bool:
    """Détermine si un fichier doit être inclus."""
    # Vérifier les patterns d'exclusion
    for pattern in EXCLUDE_PATTERNS:
        if file_path.match(pattern) or file_path.name.startswith('.'):
            return False
    
    # Exclure les extensions interdites
    if file_path.suffix.lower() in EXCLUDE_EXTENSIONS:
        return False
    
    # Exclure les fichiers CSV
    if file_path.suffix.lower() == '.csv':
        return False
    
    # Exclure les fichiers dans les dossiers CSV
    if 'CSV' in file_path.parts:
        return False
    
    # Vérifier l'extension
    if file_path.suffix.lower() in INCLUDE_EXTENSIONS:
        return True
    
    # Vérifier les noms de fichiers spécifiques
    if file_path.name in INCLUDE_FILES:
        return True
    
    return False

def should_include_dir(dir_path: Path) -> bool:
    """Détermine si un dossier doit être inclus."""
    dir_name = dir_path.name
    
    # Exclure les dossiers spécifiques
    if dir_name in EXCLUDE_DIRS:
        return False
    
    # Inclure les dossiers de langue et images
    if dir_name in INCLUDE_DIRS:
        return True
    
    # Exclure les dossiers cachés
    if dir_name.startswith('.'):
        return False
    
    return True

def copy_file(source: Path, dest: Path):
    """Copie un fichier en préservant la structure."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)

def prepare_deployment():
    """Prépare le dossier de déploiement."""
    print("=" * 70)
    print("📦 PRÉPARATION DU DÉPLOIEMENT CLOUDFLARE PAGES")
    print("=" * 70)
    print()
    
    # Nettoyer le dossier dist
    if DIST_DIR.exists():
        print("🧹 Nettoyage du dossier dist/...")
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir()
    print("✅ Dossier dist/ créé")
    print()
    
    # Compteurs
    files_copied = 0
    files_skipped = 0
    dirs_skipped = 0
    
    print("📋 Copie des fichiers nécessaires...")
    print()
    
    # Parcourir tous les fichiers
    for item in BASE_DIR.rglob('*'):
        # Ignorer le dossier dist lui-même
        if item == DIST_DIR or DIST_DIR in item.parents:
            continue
        
        # Ignorer .git
        if '.git' in item.parts:
            continue
        
        # Traiter les fichiers
        if item.is_file():
            # Vérifier si le dossier parent doit être inclus
            relative_path = item.relative_to(BASE_DIR)
            parent_dir = relative_path.parts[0] if len(relative_path.parts) > 1 else ''
            
            # Exclure les dossiers parents interdits
            if parent_dir in EXCLUDE_DIRS:
                files_skipped += 1
                continue
            
            # Exclure les fichiers dans les dossiers CSV des langues
            if 'CSV' in relative_path.parts:
                files_skipped += 1
                continue
            
            # Vérifier si le fichier doit être inclus
            if should_include_file(item):
                dest_file = DIST_DIR / relative_path
                copy_file(item, dest_file)
                files_copied += 1
                if files_copied % 1000 == 0:
                    print(f"  ✅ {files_copied} fichiers copiés...")
            else:
                files_skipped += 1
    
    print()
    print("=" * 70)
    print("✅ PRÉPARATION TERMINÉE!")
    print("=" * 70)
    print()
    print(f"📊 Statistiques:")
    print(f"   ✅ Fichiers copiés: {files_copied}")
    print(f"   ⏭️  Fichiers ignorés: {files_skipped}")
    print()
    print(f"📁 Dossier de déploiement: {DIST_DIR}")
    print()
    print("💡 Configuration Cloudflare Pages:")
    print("   1. Allez dans Settings > Builds & deployments")
    print("   2. Build output directory: dist")
    print("   3. Root directory: / (ou vide)")
    print("   4. Build command: python3 prepare_cloudflare_deploy.py")
    print()
    
    return files_copied

if __name__ == '__main__':
    files_count = prepare_deployment()
    if files_count > 20000:
        print("⚠️  ATTENTION: Le nombre de fichiers ({}) dépasse encore la limite de 20,000".format(files_count))
        print("   Il faudra exclure plus de fichiers ou optimiser les images")
    else:
        print("✅ Le nombre de fichiers ({}) est sous la limite de 20,000".format(files_count))

