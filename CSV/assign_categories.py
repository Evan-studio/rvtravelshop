#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour assigner automatiquement les catégories aux produits
basé sur l'analyse des mots-clés dans les titres.
"""

import csv
import os
from pathlib import Path

# Définition des catégories avec leurs mots-clés
CATEGORIES = {
    1: {
        'name': 'Truck Camper',
        'keywords': ['truck camper', 'pickup camper', 'pickup truck', 'ute', 'canopy camper', 
                     'slide-in camper', 'overland camper', 'truck bed', '4x4 camper', 
                     'off-road camper', 'pickup', 'truck canopy']
    },
    2: {
        'name': 'Rooftop Tent',
        'keywords': ['rooftop tent', 'roof top tent', 'hard shell tent', 'pop-up tent', 
                     'popup tent', 'clamshell', 'roof tent']
    },
    3: {
        'name': 'RV Interior',
        'keywords': ['refrigerator', 'fridge', 'air conditioner', 'heater', 'bed lift', 
                     'rv seat', 'kitchen', 'toilet', 'shower', 'sink', 'interior', 
                     'appliance', 'stove', 'cooker', 'water heater', 'generator', 
                     'furnace', 'ac unit', 'cooling']
    },
    4: {
        'name': 'RV Exterior',
        'keywords': ['awning', 'storm band', 'tie down', 'wind resistant', 'exterior', 
                     'ladder', 'rack', 'bike carrier', 'rear rack', 'tire rack', 
                     'back rack', 'bumper', 'step']
    },
    5: {
        'name': 'Van Equipment',
        'keywords': ['van', 'sprinter', 'transporter', 'van conversion', 'camper van', 
                     'van equipment', 'van interior', 't5', 't6', 'transit', 'promaster']
    },
    6: {
        'name': 'Auto Parts',
        'keywords': ['compressor', 'tire inflator', 'diagnostic', 'tool', 'programmer', 
                     'key programming', 'jump starter', 'auto parts', 'car parts', 
                     'scanner', 'obd', 'code reader']
    },
    7: {
        'name': 'RV Accessories',
        'keywords': ['rv', 'motorhome', 'caravan', 'camping', 'camper', 'overland']
    }
}

def assign_category(title):
    """
    Assigne une catégorie à un produit basé sur son titre.
    Utilise un système de priorité : les catégories plus spécifiques sont vérifiées en premier.
    """
    if not title:
        return 7  # Catégorie par défaut
    
    title_lower = title.lower()
    
    # Vérifier les catégories dans l'ordre de priorité (1-6, puis 7 comme catch-all)
    for cat_id in range(1, 7):
        cat_data = CATEGORIES[cat_id]
        for keyword in cat_data['keywords']:
            if keyword in title_lower:
                return cat_id
    
    # Si aucune catégorie spécifique n'est trouvée, utiliser la catégorie générale
    return 7

def process_csv(input_file, output_file=None):
    """
    Traite le CSV et assigne les catégories.
    """
    if output_file is None:
        output_file = input_file
    
    # Créer une sauvegarde
    backup_file = input_file + '.backup'
    if not os.path.exists(backup_file):
        print(f"📋 Création d'une sauvegarde: {backup_file}")
        import shutil
        shutil.copy2(input_file, backup_file)
    
    # Lire le CSV
    rows = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            # Obtenir le titre
            title = row.get('titre', '') or row.get('name', '')
            
            # Assigner la catégorie
            category_id = assign_category(title)
            row['category_id'] = str(category_id)
            
            rows.append(row)
    
    # Écrire le CSV mis à jour
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    # Statistiques
    stats = {}
    for row in rows:
        cat_id = int(row['category_id'])
        cat_name = CATEGORIES[cat_id]['name']
        stats[cat_id] = stats.get(cat_id, {'name': cat_name, 'count': 0})
        stats[cat_id]['count'] += 1
    
    print(f"\n✅ Catégories assignées avec succès!")
    print(f"📊 Statistiques:\n")
    for cat_id in sorted(stats.keys()):
        print(f"  {cat_id}. {stats[cat_id]['name']}: {stats[cat_id]['count']} produits")
    
    print(f"\n💾 Fichier sauvegardé: {output_file}")
    print(f"💾 Sauvegarde: {backup_file}")

if __name__ == '__main__':
    csv_file = Path(__file__).parent / 'all_products.csv'
    
    if not csv_file.exists():
        print(f"❌ Erreur: Fichier {csv_file} introuvable!")
        exit(1)
    
    print(f"🚀 Début de l'assignation des catégories...")
    print(f"📁 Fichier: {csv_file}\n")
    
    process_csv(str(csv_file))

