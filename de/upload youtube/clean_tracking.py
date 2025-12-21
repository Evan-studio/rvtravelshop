#!/usr/bin/env python3
"""
Script pour nettoyer le tracking des vidéos qui n'ont pas été réellement uploadées
(par exemple, si le quota a été dépassé mais que le tracking a été mis à jour)
"""

import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CSV_FILE = BASE_DIR / 'CSV' / 'all_products.csv'
TRACKING_FILE = Path(__file__).parent / 'upload_tracking.json'

def main():
    print("=" * 70)
    print("🧹 NETTOYAGE DU TRACKING YOUTUBE")
    print("=" * 70)
    print()
    
    # Charger le CSV
    print("📖 Chargement du CSV...")
    if not CSV_FILE.exists():
        print(f"❌ Fichier CSV non trouvé: {CSV_FILE}")
        return
    
    df = pd.read_csv(CSV_FILE)
    if 'youtube_url' not in df.columns:
        print("⚠️  Colonne youtube_url non trouvée dans le CSV")
        return
    
    # Récupérer les product_id qui ont vraiment un youtube_url
    real_uploaded = set(
        df.loc[
            df['youtube_url'].fillna('').astype(str).str.strip() != '',
            'product_id'
        ].astype(str)
    )
    print(f"✅ {len(real_uploaded)} vidéos réellement uploadées (dans le CSV)")
    print()
    
    # Charger le tracking
    print("📖 Chargement du tracking...")
    if not TRACKING_FILE.exists():
        print("⚠️  Fichier tracking non trouvé")
        return
    
    with open(TRACKING_FILE, 'r', encoding='utf-8') as f:
        tracking_data = json.load(f)
    
    uploads = tracking_data.get('uploads', {})
    tracking_ids = set()
    for k, v in uploads.items():
        if isinstance(k, str) and '_' in k:
            pid = k.split('_', 1)[1]
        else:
            pid = k
        if not pid and isinstance(v, dict):
            pid = v.get('product_id') or ''
        if pid:
            tracking_ids.add(str(pid))
    
    print(f"📊 {len(tracking_ids)} product_id dans le tracking")
    print()
    
    # Trouver les IDs dans le tracking mais pas dans le CSV
    false_positives = tracking_ids - real_uploaded
    print(f"🔍 {len(false_positives)} product_id dans le tracking mais PAS dans le CSV")
    print("   (probablement des fausses entrées)")
    print()
    
    if false_positives:
        print("📋 Liste des product_id à supprimer du tracking:")
        for pid in sorted(false_positives)[:20]:  # Afficher les 20 premiers
            print(f"   • {pid}")
        if len(false_positives) > 20:
            print(f"   ... et {len(false_positives) - 20} autres")
        print()
        
        response = input("Supprimer ces entrées du tracking? (oui/non): ").strip().lower()
        if response in ['oui', 'o', 'yes', 'y']:
            # Nettoyer le tracking
            cleaned_uploads = {}
            for pid in real_uploaded:
                cleaned_uploads[pid] = {"product_id": pid}
            
            tracking_data['uploads'] = cleaned_uploads
            
            # Sauvegarder
            with open(TRACKING_FILE, 'w', encoding='utf-8') as f:
                json.dump(tracking_data, f, indent=2, ensure_ascii=False)
            
            print()
            print(f"✅ Tracking nettoyé: {len(cleaned_uploads)} entrées conservées")
            print(f"   {len(false_positives)} fausses entrées supprimées")
        else:
            print("❌ Opération annulée")
    else:
        print("✅ Aucune fausse entrée trouvée - le tracking est propre!")

if __name__ == '__main__':
    main()

