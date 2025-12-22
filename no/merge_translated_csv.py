#!/usr/bin/env python3
"""
Script pour reformer le CSV complet à partir des 4 parties traduites.
Lit les fichiers depuis le dossier 'translated' et crée le CSV complet.
"""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / 'translated'
OUTPUT_FILE = BASE_DIR / 'CSV' / 'all_products_translated.csv'
BACKUP_FILE = BASE_DIR / 'CSV' / 'all_products.csv.backup_before_merge'
ORIGINAL_FILE = BASE_DIR / 'CSV' / 'all_products.csv'
NUM_PARTS = 4

def merge_csv_for_language(lang_dir=None):
    """Reforme le CSV complet à partir des 4 parties traduites pour une langue donnée.
    
    Args:
        lang_dir: Dossier de langue (Path). Si None, utilise BASE_DIR.
    
    Returns:
        bool: True si succès, False sinon
    """
    if lang_dir is None:
        lang_dir = BASE_DIR
    
    input_dir = lang_dir / 'translated'
    output_file = lang_dir / 'CSV' / 'all_products_translated.csv'
    backup_file = lang_dir / 'CSV' / 'all_products.csv.backup_before_merge'
    original_file = lang_dir / 'CSV' / 'all_products.csv'

def detect_delimiter(file_path):
    """Détecte automatiquement le séparateur CSV."""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','

def merge_csv_for_language(lang_dir=None):
    """Reforme le CSV complet à partir des 4 parties traduites pour une langue donnée.
    
    Args:
        lang_dir: Dossier de langue (Path). Si None, utilise BASE_DIR.
    
    Returns:
        bool: True si succès, False sinon
    """
    if lang_dir is None:
        lang_dir = BASE_DIR
    
    input_dir = lang_dir / 'translated'
    output_file = lang_dir / 'CSV' / 'all_products_translated.csv'
    backup_file = lang_dir / 'CSV' / 'all_products.csv.backup_before_merge'
    original_file = lang_dir / 'CSV' / 'all_products.csv'
    
    print("=" * 70)
    print(f"🔗 FUSION DES 4 PARTIES TRADUITES")
    print(f"   Langue: {lang_dir.name}")
    print("=" * 70)
    print()
    
    if not input_dir.exists():
        print(f"❌ Dossier non trouvé: {input_dir}")
        print(f"   Créez le dossier '{input_dir.name}' et placez-y les 4 fichiers traduits")
        return False
    
    # Vérifier que tous les fichiers existent
    missing_files = []
    part_files = []
    
    for part_num in range(1, NUM_PARTS + 1):
        part_file = input_dir / f'all_products_part{part_num}.csv'
        if not part_file.exists():
            missing_files.append(part_file.name)
        else:
            part_files.append(part_file)
    
    if missing_files:
        print(f"❌ Fichiers manquants dans '{input_dir.name}/':")
        for f in missing_files:
            print(f"   • {f}")
        print()
        print("💡 Assurez-vous d'avoir tous les fichiers traduits dans le dossier 'translated'")
        return False
    
    print(f"✅ Tous les fichiers trouvés dans '{input_dir.name}/'")
    print()
    
    # Détecter le séparateur depuis le premier fichier
    delimiter = detect_delimiter(part_files[0])
    print(f"📊 Séparateur détecté: {'point-virgule (;)' if delimiter == ';' else 'virgule (,)'}")
    print()
    
    # Lire tous les fichiers et fusionner en combinant les données non-vides
    print("📖 Lecture des fichiers...")
    all_rows_dict = {}  # Dictionnaire indexé par original_row
    fieldnames = None
    
    for part_file in sorted(part_files):
        with open(part_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            if fieldnames is None:
                fieldnames = list(reader.fieldnames)
            elif list(reader.fieldnames) != fieldnames:
                print(f"⚠️  Attention: Les colonnes de {part_file.name} diffèrent des autres")
            
            rows = list(reader)
            data_count = 0
            empty_count = 0
            
            for idx, row in enumerate(rows, start=2):  # start=2 car ligne 1 = en-tête
                # Utiliser original_row si présent, sinon utiliser l'index de la ligne
                row_num = row.get('original_row', str(idx))
                
                # Vérifier si la ligne contient des données (au moins un champ non-vide sauf original_row)
                has_data = any(v.strip() for k, v in row.items() if k != 'original_row' and v and v.strip())
                
                if has_data:
                    # Cette ligne a des données, l'utiliser (remplace si déjà présent)
                    all_rows_dict[row_num] = row
                    data_count += 1
                elif row_num not in all_rows_dict:
                    # Ligne vide, garder une référence pour préserver l'ordre seulement si on a les lignes vides
                    # Si le fichier n'a pas de lignes vides (comme partie 1), on ignore les lignes vides
                    if len(rows) > 1000:  # Fichier avec lignes vides (plus de 1000 lignes)
                        all_rows_dict[row_num] = row
                        empty_count += 1
            
            print(f"  ✅ {part_file.name}: {data_count} lignes avec données, {empty_count} lignes vides")
    
    print()
    
    # Convertir le dictionnaire en liste triée par original_row
    print("🔄 Tri des lignes par numéro de ligne original...")
    try:
        all_rows = []
        for row_num in sorted(all_rows_dict.keys(), key=lambda x: int(x) if x.isdigit() else 0):
            row = all_rows_dict[row_num]
            # Ne garder que les lignes avec des données (ignorer les lignes vides)
            has_data = any(v.strip() for k, v in row.items() if k != 'original_row' and v)
            if has_data:
                all_rows.append(row)
        
        print(f"✅ {len(all_rows)} lignes avec données extraites et triées")
    except (ValueError, KeyError) as e:
        print(f"⚠️  Erreur lors du tri: {e}")
        # Fallback: utiliser toutes les lignes dans l'ordre
        all_rows = list(all_rows_dict.values())
        print("   Utilisation de toutes les lignes dans l'ordre des fichiers")
    
    print()
    
    # Supprimer la colonne original_row avant de sauvegarder
    # D'abord supprimer de toutes les lignes pour éviter les erreurs
    for row in all_rows:
        if 'original_row' in row:
            del row['original_row']
    
    # Ensuite supprimer de fieldnames
    if 'original_row' in fieldnames:
        fieldnames = [f for f in fieldnames if f != 'original_row']
        print("✅ Colonne 'original_row' supprimée du fichier final")
    else:
        print("ℹ️  Colonne 'original_row' absente (déjà supprimée ou non présente)")
    print()
    
    # Créer une sauvegarde du fichier original
    if original_file.exists():
        import shutil
        shutil.copy2(original_file, backup_file)
        print(f"💾 Sauvegarde créée: {backup_file.name}")
        print()
    
    # Sauvegarder le CSV fusionné
    print("💾 Création du CSV fusionné...")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(all_rows)
    
    print(f"✅ CSV fusionné créé: {output_file.name}")
    print()
    
    # Proposer de remplacer le fichier original
    print("=" * 70)
    print("✅ FUSION TERMINÉE!")
    print("=" * 70)
    print()
    print(f"📁 Fichier créé: {output_file.name}")
    print()
    print("💡 Pour remplacer le fichier original:")
    print(f"   cp {output_file.name} {original_file.name}")
    print()
    print("⚠️  Le fichier original a été sauvegardé dans:")
    print(f"   {backup_file.name}")
    print()
    
    return True

def merge_csv():
    """Fonction wrapper pour compatibilité avec l'appel direct."""
    return merge_csv_for_language()

if __name__ == '__main__':
    merge_csv()

