# 🔄 Guide : Rediriger uni-ion.com vers Cloudflare Pages

## 🎯 Objectif

Rediriger votre domaine `uni-ion.com` (Hostinger) vers Cloudflare Pages pour tester si Google enregistre mieux les sitemaps avec un domaine personnalisé.

## 📋 Étapes détaillées

### ÉTAPE 1 : Ajouter le domaine dans Cloudflare

1. Allez sur https://dash.cloudflare.com
2. Cliquez sur **"Add a site"** (en haut à droite)
3. Entrez : `uni-ion.com`
4. Cliquez sur **"Add site"**
5. Choisissez le plan **Free** (gratuit)
6. Cloudflare va scanner votre domaine

### ÉTAPE 2 : Obtenir les serveurs DNS de Cloudflare

Après l'ajout, Cloudflare vous donnera **2 serveurs DNS** qui ressemblent à :
```
dante.ns.cloudflare.com
gwen.ns.cloudflare.com
```

**⚠️ IMPORTANT : Notez ces 2 serveurs DNS !**

### ÉTAPE 3 : Changer les DNS sur Hostinger

1. Allez sur votre compte Hostinger
2. Allez dans **Domains** > **Gérer** pour `uni-ion.com`
3. Cherchez **"Nameservers"** ou **"Serveurs DNS"**
4. Remplacez les serveurs DNS actuels par ceux de Cloudflare :
   ```
   dante.ns.cloudflare.com
   gwen.ns.cloudflare.com
   ```
5. Sauvegardez

**⏰ Délai** : La propagation DNS prend 24-48h (parfois moins)

### ÉTAPE 4 : Configurer les DNS dans Cloudflare

1. Dans Cloudflare Dashboard, allez dans votre domaine `uni-ion.com`
2. Allez dans **DNS** > **Records**
3. Ajoutez les enregistrements suivants :

#### Enregistrement A (pour la racine)
- **Type** : `A`
- **Name** : `@` (ou `uni-ion.com`)
- **IPv4 address** : `192.0.2.1` (temporaire, sera remplacé)
- **Proxy status** : Proxied (orange cloud) ✅

#### Enregistrement CNAME (pour Cloudflare Pages)
- **Type** : `CNAME`
- **Name** : `@` (ou `uni-ion.com`)
- **Target** : `makita-6kq.pages.dev`
- **Proxy status** : Proxied (orange cloud) ✅

**Note** : Vous ne pouvez pas avoir A et CNAME pour `@` en même temps. Utilisez **CNAME** uniquement.

### ÉTAPE 5 : Connecter le domaine à Cloudflare Pages

1. Dans Cloudflare Dashboard, allez dans **Pages**
2. Sélectionnez votre projet `makita`
3. Allez dans **Custom domains**
4. Cliquez sur **"Set up a custom domain"**
5. Entrez : `uni-ion.com`
6. Cliquez sur **"Add domain"**
7. Cloudflare va vérifier la configuration DNS

**⏰ Attendez** que le statut passe à "Active" (peut prendre quelques minutes)

### ÉTAPE 6 : Mettre à jour les sitemaps avec le nouveau domaine

Une fois le domaine actif, mettez à jour les sitemaps :

1. Modifiez le fichier `translations.csv` à la racine pour changer le domaine
2. Ou modifiez directement dans les dossiers de langue (`fr/translations.csv`, etc.)
3. Changez `site.domain` de `makita-6kq.pages.dev` vers `uni-ion.com`
4. Régénérez les sitemaps :
   ```bash
   python3 generate_sitemaps.py
   ```
5. Déployez :
   ```bash
   python3 update_github_auto.py "Update: Changement domaine vers uni-ion.com"
   ```

### ÉTAPE 7 : Vérifier que tout fonctionne

Après 24-48h (propagation DNS), testez :

```bash
# Vérifier l'accessibilité
curl -I https://uni-ion.com/sitemap-all.xml

# Vérifier le Content-Type
curl -I https://uni-ion.com/sitemap-all.xml | grep content-type

# Vérifier le nombre d'URLs
curl -s https://uni-ion.com/sitemap-all.xml | grep -c "<url>"
```

### ÉTAPE 8 : Soumettre dans Google Search Console

1. Allez sur https://search.google.com/search-console
2. Ajoutez une nouvelle propriété : `uni-ion.com`
3. Vérifiez la propriété (via DNS ou fichier HTML)
4. Une fois vérifié, allez dans **Sitemaps**
5. Soumettez : `sitemap-all.xml` ou `sitemap.xml`
6. Attendez 24-48h et comparez avec `makita-6kq.pages.dev`

## 🔍 Vérifications importantes

### Vérifier la propagation DNS

Utilisez un outil en ligne :
- https://www.whatsmydns.net/#CNAME/uni-ion.com
- Entrez `uni-ion.com` et vérifiez que ça pointe vers Cloudflare

### Vérifier que le domaine fonctionne

1. Ouvrez https://uni-ion.com dans votre navigateur
2. Le site devrait s'afficher (même contenu que makita-6kq.pages.dev)
3. Testez : https://uni-ion.com/sitemap-all.xml

## ⚠️ Points importants

1. **Propagation DNS** : Peut prendre 24-48h
2. **SSL/TLS** : Cloudflare génère automatiquement un certificat SSL (gratuit)
3. **Cache** : Cloudflare peut mettre en cache, purgez si besoin
4. **DNS** : Une fois changé, Hostinger ne gère plus les DNS (c'est Cloudflare qui gère)

## 📊 Comparaison après test

Après 48h, comparez dans Google Search Console :
- `makita-6kq.pages.dev` (sous-domaine Cloudflare)
- `uni-ion.com` (domaine personnalisé)

Si `uni-ion.com` fonctionne mieux, c'est que Cloudflare Pages a des limitations avec les sous-domaines `.pages.dev`.

## 🆘 Si ça ne fonctionne pas

1. Vérifiez que les DNS sont bien propagés (whatsmydns.net)
2. Vérifiez que le domaine est "Active" dans Cloudflare Pages
3. Vérifiez que les sitemaps utilisent le bon domaine
4. Attendez 24-48h (propagation DNS)

## ✅ Checklist

- [ ] Domaine ajouté dans Cloudflare
- [ ] Serveurs DNS Cloudflare notés
- [ ] DNS changés sur Hostinger
- [ ] Enregistrements DNS configurés dans Cloudflare
- [ ] Domaine connecté à Cloudflare Pages
- [ ] Statut "Active" dans Cloudflare Pages
- [ ] Sitemaps régénérés avec uni-ion.com
- [ ] Site accessible sur https://uni-ion.com
- [ ] Sitemap accessible sur https://uni-ion.com/sitemap-all.xml
- [ ] Soumis dans Google Search Console
- [ ] Attendu 24-48h pour les résultats

