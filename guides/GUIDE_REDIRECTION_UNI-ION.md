# 🔄 Guide : Rediriger uni-ion.com vers Cloudflare Pages

## 📋 Étapes simplifiées

### ÉTAPE 1 : Changer le domaine dans les CSV

Modifiez `site.domain` dans **tous** les fichiers `translations.csv` :

**Fichiers à modifier :**
- `translations.csv` (racine)
- `fr/translations.csv`
- `de/translations.csv`
- `es/translations.csv`
- `pt/translations.csv`

**Ligne à modifier :**
```csv
site.domain,Domaine du site (URL de base),https://makita-6kq.pages.dev/,https://makita-6kq.pages.dev/
```

**Remplacer par :**
```csv
site.domain,Domaine du site (URL de base),https://uni-ion.com/,https://uni-ion.com/
```

### ÉTAPE 2 : Lancer les scripts de mise à jour automatique

Vos scripts existants vont mettre à jour toutes les URLs automatiquement :

```bash
# Pour la racine (en)
python3 scripts/generate/update_domain_urls.py

# Pour chaque langue (si nécessaire)
python3 fr/scripts/generate/update_domain_urls.py
python3 de/scripts/generate/update_domain_urls.py
python3 es/scripts/generate/update_domain_urls.py
python3 pt/scripts/generate/update_domain_urls.py
```

### ÉTAPE 3 : Régénérer les sitemaps

```bash
python3 generate_sitemaps.py
```

Les sitemaps utiliseront automatiquement le nouveau domaine depuis `translations.csv`.

### ÉTAPE 4 : Configurer Cloudflare

#### 4.1 Ajouter le domaine dans Cloudflare

1. Allez sur https://dash.cloudflare.com
2. Cliquez sur **"Add a site"**
3. Entrez : `uni-ion.com`
4. Choisissez le plan **Free**
5. Cloudflare va scanner votre domaine

#### 4.2 Obtenir les serveurs DNS Cloudflare

Cloudflare vous donnera 2 serveurs DNS, par exemple :
```
dante.ns.cloudflare.com
gwen.ns.cloudflare.com
```

**Notez-les !**

#### 4.3 Changer les DNS sur Hostinger

1. Allez sur votre compte Hostinger
2. **Domains** > **Gérer** pour `uni-ion.com`
3. Cherchez **"Nameservers"** ou **"Serveurs DNS"**
4. Remplacez par les serveurs Cloudflare
5. Sauvegardez

**⏰ Délai** : 24-48h pour la propagation DNS

#### 4.4 Configurer les DNS dans Cloudflare

1. Dans Cloudflare Dashboard > `uni-ion.com` > **DNS** > **Records**
2. Supprimez les enregistrements existants (sauf ceux nécessaires)
3. Ajoutez un **CNAME** :
   - **Type** : `CNAME`
   - **Name** : `@` (ou laissez vide pour la racine)
   - **Target** : `makita-6kq.pages.dev`
   - **Proxy status** : Proxied (orange cloud) ✅

**Note** : Cloudflare Pages peut aussi créer cet enregistrement automatiquement.

#### 4.5 Connecter le domaine à Cloudflare Pages

1. Cloudflare Dashboard > **Pages** > Votre projet `makita`
2. **Custom domains** > **"Set up a custom domain"**
3. Entrez : `uni-ion.com`
4. Cliquez sur **"Add domain"**
5. Cloudflare va créer automatiquement l'enregistrement CNAME

**⏰ Attendez** que le statut passe à "Active"

### ÉTAPE 5 : Déployer

```bash
python3 update_github_auto.py "Update: Changement domaine vers uni-ion.com"
```

### ÉTAPE 6 : Vérifier (après 24-48h)

```bash
# Vérifier l'accessibilité
curl -I https://uni-ion.com/sitemap-all.xml

# Vérifier le nombre d'URLs
curl -s https://uni-ion.com/sitemap-all.xml | grep -c "<url>"
```

### ÉTAPE 7 : Soumettre dans Google Search Console

1. Ajoutez une nouvelle propriété : `uni-ion.com`
2. Vérifiez la propriété (via DNS)
3. Soumettez le sitemap : `sitemap-all.xml`
4. Comparez avec `makita-6kq.pages.dev` après 24-48h

## ✅ Checklist

- [ ] Domaine changé dans tous les `translations.csv`
- [ ] Scripts `update_domain_urls.py` lancés
- [ ] Sitemaps régénérés avec `generate_sitemaps.py`
- [ ] Domaine ajouté dans Cloudflare
- [ ] DNS changés sur Hostinger
- [ ] Domaine connecté à Cloudflare Pages
- [ ] Statut "Active" dans Cloudflare Pages
- [ ] Déployé sur GitHub
- [ ] Site accessible sur https://uni-ion.com
- [ ] Sitemap accessible sur https://uni-ion.com/sitemap-all.xml
- [ ] Soumis dans Google Search Console

## 💡 Avantages d'un domaine personnalisé

- ✅ Plus professionnel
- ✅ Meilleur pour le SEO
- ✅ Plus de contrôle sur les DNS
- ✅ Peut résoudre les problèmes de sitemap avec Cloudflare Pages

