#!/usr/bin/env python3
"""
Script pour trouver les produits liés aux voitures (pas aux vans/camping-cars)
dans all_products.csv.

Mots-clés recherchés:
- sièges électriques (electric seat, power seat)
- feux arrière (rear light, tail light, brake light)
- phares avant (headlight, front light)
- amortisseurs (shock absorber, damper)
- Marques de voiture (cayenne, bmw, mercedes, audi, etc.)
- Mais exclure les vans (VW T5, T6, etc.)
"""

import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
PRODUCTS_CSV = BASE_DIR / 'CSV' / 'all_products.csv'
OUTPUT_CSV = BASE_DIR / 'CSV' / 'products_voiture_auto.csv'

# Mots-clés pour identifier les produits auto/voiture
CAR_KEYWORDS = [
    # Sièges électriques
    r'\belectric\s+seat\b',
    r'\bpower\s+seat\b',
    r'\belectronic\s+seat\b',
    r'\bseat\s+electric\b',
    r'siege\s+electrique',
    
    # Feux arrière
    r'\brear\s+light\b',
    r'\btail\s+light\b',
    r'\bbrake\s+light\b',
    r'\bstop\s+light\b',
    r'feu\s+arriere',
    r'feu\s+stop',
    
    # Phares avant
    r'\bheadlight\b',
    r'\bhead\s+light\b',
    r'\bfront\s+light\b',
    r'\bheadlamp\b',
    r'phare\s+avant',
    
    # Amortisseurs
    r'\bshock\s+absorber\b',
    r'\bdamper\b',
    r'\bstrut\b',
    r'amortisseur',
    
    # Autres pièces auto
    r'\bcar\s+door\b',
    r'\bcar\s+mirror\b',
    r'\brearview\s+mirror\b',
    r'\bcar\s+window\b',
    r'\bcar\s+wheel\b',
    r'\bcar\s+rim\b',
    r'\bcar\s+tyre\b',
    r'\bcar\s+tire\b',
    r'\bcar\s+engine\b',
    r'\bcar\s+exhaust\b',
    r'\bcar\s+bumper\b',
    r'\bcar\s+grille\b',
    r'\bcar\s+spoiler\b',
    r'\bcar\s+hood\b',
    r'\bcar\s+trunk\b',
    r'\bcar\s+body\b',
    r'\bcar\s+panel\b',
    r'\bcar\s+frame\b',
    r'\bcar\s+chassis\b',
]

# Marques de voiture (pas de vans)
CAR_BRANDS = [
    r'\bcayenne\b',
    r'\bbmw\b',
    r'\bmercedes\b',
    r'\baudi\b',
    r'\bvolkswagen\b',
    r'\bvw\b',
    r'\bporsche\b',
    r'\bferrari\b',
    r'\blamborghini\b',
    r'\bmclaren\b',
    r'\bmaserati\b',
    r'\brolls\s+royce\b',
    r'\bbentley\b',
    r'\baston\s+martin\b',
    r'\bjaguar\b',
    r'\bland\s+rover\b',
    r'\brange\s+rover\b',
    r'\bmini\s+cooper\b',
    r'\bmini\s+cooper\b',
    r'\bford\s+mustang\b',
    r'\bford\s+focus\b',
    r'\bford\s+fiesta\b',
    r'\bchevrolet\b',
    r'\bcorvette\b',
    r'\bcamaro\b',
    r'\bchrysler\b',
    r'\bdodge\b',
    r'\bjeep\s+cherokee\b',
    r'\bjeep\s+grand\s+cherokee\b',
    r'\bjeep\s+wrangler\b',
    r'\btoyota\s+corolla\b',
    r'\btoyota\s+camry\b',
    r'\btoyota\s+prius\b',
    r'\bhonda\s+civic\b',
    r'\bhonda\s+accord\b',
    r'\bnissan\s+altima\b',
    r'\bnissan\s+sentra\b',
    r'\bmazda\b',
    r'\bsubaru\b',
    r'\bhyundai\b',
    r'\bkia\b',
    r'\bvolvo\b',
    r'\bsaab\b',
    r'\bopel\b',
    r'\brenault\b',
    r'\bpeugeot\b',
    r'\bcitroen\b',
    r'\bfiat\b',
    r'\balfa\s+romeo\b',
    r'\blancia\b',
    r'\bseat\b',
    r'\bskoda\b',
    r'\bgenesis\b',
    r'\binfiniti\b',
    r'\bacura\b',
    r'\blexus\b',
]

# Mots-clés à exclure (vans/camping-cars)
EXCLUDE_KEYWORDS = [
    r'\bvw\s+t[456]\b',
    r'\bvolkswagen\s+t[456]\b',
    r'\btransporter\s+t[456]\b',
    r'\bvan\s+t[456]\b',
    r'\bmultivan\b',
    r'\brv\b',
    r'\bmotorhome\b',
    r'\bcamper\b',
    r'\bcampervan\b',
    r'\bcamping\s+car\b',
    r'\btrailer\b',
    r'\bcaravan\b',
    r'\bhiace\b',
    r'\bcoaster\b',
    r'\bsprinter\b',
    r'\bcrafter\b',
    r'\bmaster\b',
    r'\btrafic\b',
    r'\bducato\b',
    r'\bboxer\b',
    r'\bjumper\b',
    r'\bvivaro\b',
    r'\bmovano\b',
    r'\bdaily\b',
    r'\bdoblo\b',
    r'\bkangoo\b',
    r'\bpartner\b',
    r'\bberlingo\b',
    r'\btransit\s+van\b',
    r'\bpromaster\b',
    r'\bsavana\b',
    r'\bexpress\b',
]

def detect_delimiter(file_path):
    """Détecte automatiquement le séparateur CSV."""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        return ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','

def contains_car_keyword(text):
    """Vérifie si le texte contient un mot-clé de voiture."""
    if not text:
        return False
    
    text_lower = text.lower()
    
    # Vérifier les mots-clés d'exclusion d'abord
    for exclude_pattern in EXCLUDE_KEYWORDS:
        if re.search(exclude_pattern, text_lower, re.IGNORECASE):
            return False
    
    # Vérifier les mots-clés de voiture
    for keyword_pattern in CAR_KEYWORDS:
        if re.search(keyword_pattern, text_lower, re.IGNORECASE):
            return True
    
    # Vérifier les marques de voiture
    for brand_pattern in CAR_BRANDS:
        if re.search(brand_pattern, text_lower, re.IGNORECASE):
            return True
    
    return False

def find_car_products():
    """Trouve les produits liés aux voitures dans le CSV."""
    if not PRODUCTS_CSV.exists():
        print(f"❌ Fichier non trouvé: {PRODUCTS_CSV}")
        return False
    
    delimiter = detect_delimiter(PRODUCTS_CSV)
    
    car_products = []
    
    print("=" * 70)
    print("🔍 RECHERCHE DE PRODUITS AUTO/VOITURE")
    print("=" * 70)
    print()
    print("📖 Lecture du CSV...")
    
    with open(PRODUCTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        fieldnames = reader.fieldnames
        
        for row in reader:
            product_id = row.get('product_id', '').strip()
            if not product_id:
                continue
            
            # Vérifier dans titre, name, description_short
            titre = row.get('titre', '').strip()
            name = row.get('name', '').strip()
            description_short = row.get('description_short', '').strip()
            
            # Combiner tous les textes pour la recherche
            all_text = f"{titre} {name} {description_short}"
            
            if contains_car_keyword(all_text):
                car_products.append(row)
    
    print(f"✅ {len(car_products)} produits auto/voiture trouvés")
    print()
    
    if not car_products:
        print("ℹ️  Aucun produit auto/voiture trouvé")
        return False
    
    # Écrire le CSV de sortie
    print(f"💾 Écriture dans {OUTPUT_CSV.name}...")
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(car_products)
    
    print(f"✅ {len(car_products)} produits sauvegardés")
    print()
    
    # Afficher quelques exemples
    print("📋 Exemples de produits trouvés:")
    print("-" * 70)
    for i, product in enumerate(car_products[:10], 1):
        name = product.get('name', '') or product.get('titre', '')
        print(f"{i}. {name[:80]}")
    if len(car_products) > 10:
        print(f"... et {len(car_products) - 10} autres produits")
    print()
    
    print("=" * 70)
    print("✅ TERMINÉ!")
    print("=" * 70)
    print()
    print(f"📁 Fichier créé: {OUTPUT_CSV}")
    print()
    
    return True

if __name__ == '__main__':
    find_car_products()

