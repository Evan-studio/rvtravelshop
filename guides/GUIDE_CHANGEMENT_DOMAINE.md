# 🔄 Guide : Changer le domaine du site

## 📋 Étapes complètes

### ÉTAPE 1 : Changer le domaine dans les CSV ⚠️ IMPORTANT

Modifiez `site.domain` dans **tous** les fichiers `translations.csv` :

**Fichiers à modifier :**
- `translations.csv` (racine)
- `fr/translations.csv`
- `de/translations.csv`
- `es/translations.csv`
- `pt/translations.csv`

**Ligne à modifier :**
```csv
site.domain,Domaine du site (URL de base),https://ANCIEN-DOMAINE.com/,https://ANCIEN-DOMAINE.com/
```

**Remplacer par :**
```csv
site.domain,Domaine du site (URL de base),https://NOUVEAU-DOMAINE.com/,https://NOUVEAU-DOMAINE.com/
```

### ÉTAPE 2 : Générer toutes les pages + Mettre à jour les domaines

```bash
python3 generate_all_languages_with_domain_update.py
```

Ce script va :
- ✅ Régénérer toutes les pages HTML
- ✅ Mettre à jour toutes les URLs avec le nouveau domaine depuis les CSV

### ÉTAPE 3 : Régénérer les sitemaps

```bash
python3 generate_sitemaps.py
```

Ce script va :
- ✅ Générer tous les sitemaps avec le nouveau domaine depuis les CSV

### ÉTAPE 4 : Déployer (optionnel)

```bash
python3 update_github_auto.py "Update: Changement domaine vers NOUVEAU-DOMAINE.com"
```

## ✅ Résumé rapide

1. **Changer `site.domain` dans tous les CSV** ⚠️
2. `python3 generate_all_languages_with_domain_update.py`
3. `python3 generate_sitemaps.py`
4. (Optionnel) `python3 update_github_auto.py`

## 🎯 C'est tout !

Ces 2 scripts suffisent, **MAIS** il faut d'abord changer le domaine dans les CSV.

## 💡 Astuce

Pour vérifier que le domaine est bien changé dans les CSV :

```bash
grep "site.domain" translations.csv fr/translations.csv de/translations.csv es/translations.csv pt/translations.csv
```

Tous doivent afficher le nouveau domaine.

