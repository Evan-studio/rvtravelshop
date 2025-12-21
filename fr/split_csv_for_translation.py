#!/usr/bin/env python3
"""
Script pour diviser un CSV en 4 parties pour la traduction dans Google Sheets.
Crée un dossier 'to_translate' avec les 4 fichiers CSV.
"""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / 'CSV' / 'all_products.csv'
OUTPUT_DIR = BASE_DIR / 'to_translate'
NUM_PARTS = 4

def split_csv_for_language(lang_dir=None):
    """Divise le CSV en 4 parties pour une langue donnée.
    
    Args:
        lang_dir: Dossier de langue (Path). Si None, utilise BASE_DIR.
    """
    if lang_dir is None:
        lang_dir = BASE_DIR
    
    csv_file = lang_dir / 'CSV' / 'all_products.csv'
    output_dir = lang_dir / 'to_translate'

def detect_delimiter(file_path):
    """Détecte automatiquement le séparateur CSV."""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','

def split_csv_for_language(lang_dir=None):
    """Divise le CSV en 4 parties pour une langue donnée.
    
    Args:
        lang_dir: Dossier de langue (Path). Si None, utilise BASE_DIR.
    
    Returns:
        bool: True si succès, False sinon
    """
    if lang_dir is None:
        lang_dir = BASE_DIR
    
    csv_file = lang_dir / 'CSV' / 'all_products.csv'
    output_dir = lang_dir / 'to_translate'
    
    print("=" * 70)
    print(f"✂️  DIVISION DU CSV EN 4 PARTIES POUR LA TRADUCTION")
    print(f"   Langue: {lang_dir.name}")
    print("=" * 70)
    print()
    
    if not csv_file.exists():
        print(f"❌ Fichier CSV non trouvé: {csv_file}")
        return False
    
    # Détecter le séparateur
    delimiter = detect_delimiter(csv_file)
    print(f"📊 Séparateur détecté: {'point-virgule (;)' if delimiter == ';' else 'virgule (,)'}")
    print()
    
    # Lire le CSV
    print("📖 Lecture du CSV...")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    
    total_rows = len(rows)
    print(f"✅ {total_rows} lignes lues (sans l'en-tête)")
    print()
    
    # Ajouter la colonne original_row à la FIN pour ne pas décaler les autres colonnes
    if 'original_row' not in fieldnames:
        fieldnames.append('original_row')
    
    # Ajouter le numéro de ligne original à chaque ligne (commence à 2 car ligne 1 = en-tête)
    for idx, row in enumerate(rows, start=2):
        row['original_row'] = str(idx)
    
    print("✅ Colonne 'original_row' ajoutée pour conserver l'ordre des lignes")
    print()
    
    # Calculer la taille de chaque partie
    rows_per_part = total_rows // NUM_PARTS
    remainder = total_rows % NUM_PARTS
    
    print(f"📊 Division en {NUM_PARTS} parties:")
    print(f"   • {NUM_PARTS - remainder} partie(s) avec {rows_per_part} lignes")
    if remainder > 0:
        print(f"   • {remainder} partie(s) avec {rows_per_part + 1} lignes")
    print()
    
    # Créer le dossier de sortie
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    print(f"📁 Dossier créé: {output_dir.name}/")
    print()
    
    # Créer une ligne vide (tous les champs vides sauf original_row)
    empty_row = {field: '' for field in fieldnames}
    
    # Diviser et sauvegarder
    print("💾 Création des fichiers avec lignes vides...")
    start_idx = 0
    
    for part_num in range(1, NUM_PARTS + 1):
        # Calculer la fin de cette partie
        if part_num <= remainder:
            end_idx = start_idx + rows_per_part + 1
        else:
            end_idx = start_idx + rows_per_part
        
        output_file = output_dir / f'all_products_part{part_num}.csv'
        
        # Créer le fichier complet avec lignes vides
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            
            # Lignes vides avant la partie
            for i in range(start_idx):
                empty_row_copy = empty_row.copy()
                empty_row_copy['original_row'] = str(i + 2)  # +2 car ligne 1 = en-tête, commence à 2
                writer.writerow(empty_row_copy)
            
            # Lignes avec données pour cette partie
            part_rows = rows[start_idx:end_idx]
            writer.writerows(part_rows)
            
            # Lignes vides après la partie
            for i in range(end_idx, total_rows):
                empty_row_copy = empty_row.copy()
                empty_row_copy['original_row'] = str(i + 2)  # +2 car ligne 1 = en-tête, commence à 2
                writer.writerow(empty_row_copy)
        
        data_lines = len(part_rows)
        empty_before = start_idx
        empty_after = total_rows - end_idx
        print(f"  ✅ Partie {part_num}: {empty_before} lignes vides + {data_lines} lignes données + {empty_after} lignes vides → {output_file.name}")
        start_idx = end_idx
    
    print()
    print("=" * 70)
    print("✅ DIVISION TERMINÉE!")
    print("=" * 70)
    print()
    print(f"📁 Fichiers créés dans: {output_dir.name}/")
    print(f"   • all_products_part1.csv")
    print(f"   • all_products_part2.csv")
    print(f"   • all_products_part3.csv")
    print(f"   • all_products_part4.csv")
    print()
    print("💡 Étapes suivantes:")
    print("   1. Ouvrez chaque fichier dans Google Sheets")
    print("   2. Les lignes vides préservent la position originale des données")
    print("   3. Les formules (comme GOOGLETRANSLATE) fonctionneront correctement")
    print("   4. Traduisez les colonnes nécessaires")
    print("   5. Téléchargez les fichiers traduits dans le dossier 'translated'")
    print("   6. Exécutez merge_translated_csv.py pour reformer le CSV complet")
    print()
    
    return True

def split_csv():
    """Fonction wrapper pour compatibilité avec l'appel direct."""
    return split_csv_for_language()

if __name__ == '__main__':
    split_csv()

