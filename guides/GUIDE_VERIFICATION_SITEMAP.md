# 🔍 Guide de vérification des sitemaps sur Cloudflare

## Méthode 1 : Script automatique (Recommandé)

Utilisez le script de vérification que nous avons créé :

```bash
./check_sitemaps.sh
```

ou avec votre domaine :

```bash
./check_sitemaps.sh makita-6kq.pages.dev
```

Le script vérifie :
- ✅ Accessibilité des sitemaps
- ✅ Content-Type correct (application/xml)
- ✅ Validité XML
- ✅ Nombre d'URLs dans chaque sitemap
- ✅ Headers HTTP

## Méthode 2 : Vérification manuelle dans le navigateur

### 1. Vérifier le sitemap index
Ouvrez dans votre navigateur :
```
https://votre-domaine.com/sitemap.xml
```

**Ce que vous devez voir :**
- Un fichier XML bien formaté
- Des balises `<sitemap>` avec des `<loc>` pointant vers les autres sitemaps
- Pas d'erreur 404 ou 500

### 2. Vérifier les sitemaps individuels
Testez chaque sitemap :
```
https://votre-domaine.com/sitemap-en.xml
https://votre-domaine.com/sitemap-fr.xml
https://votre-domaine.com/sitemap-de.xml
https://votre-domaine.com/sitemap-es.xml
https://votre-domaine.com/sitemap-pt.xml
```

**Ce que vous devez voir :**
- Des balises `<url>` avec des `<loc>` contenant vos URLs
- Format XML valide
- Pas d'erreurs

## Méthode 3 : Vérification avec curl (Terminal)

### Vérifier l'accessibilité
```bash
curl -I https://votre-domaine.com/sitemap.xml
```

**Résultat attendu :**
```
HTTP/2 200
content-type: application/xml; charset=utf-8
```

### Vérifier le contenu
```bash
curl https://votre-domaine.com/sitemap.xml
```

### Compter les URLs
```bash
curl -s https://votre-domaine.com/sitemap-fr.xml | grep -c "<url>"
```

## Méthode 4 : Outils en ligne

### 1. XML Sitemap Validator
https://www.xml-sitemaps.com/validate-xml-sitemap.html

1. Entrez l'URL de votre sitemap : `https://votre-domaine.com/sitemap.xml`
2. Cliquez sur "Validate"
3. Vérifiez qu'il n'y a pas d'erreurs

### 2. Google Search Console
https://search.google.com/search-console

1. Connectez-vous à Google Search Console
2. Sélectionnez votre propriété
3. Allez dans "Sitemaps" dans le menu de gauche
4. Vérifiez le statut de votre sitemap :
   - ✅ **Réussi** : Le sitemap est valide et indexé
   - ⚠️ **Avertissements** : Vérifiez les détails
   - ❌ **Erreur** : Corrigez les problèmes indiqués

### 3. Testeur de sitemap
https://www.xml-sitemaps.com/sitemap-validator.html

## Méthode 5 : Vérification dans Cloudflare Pages

### 1. Vérifier le déploiement
1. Allez sur https://dash.cloudflare.com
2. Sélectionnez votre projet Pages
3. Vérifiez que le dernier déploiement est réussi
4. Vérifiez que le fichier `_headers` est bien présent

### 2. Vérifier les fichiers
Dans Cloudflare Pages :
- Le fichier `sitemap.xml` doit être à la racine
- Les fichiers `sitemap-*.xml` doivent être à la racine
- Le fichier `_headers` doit être à la racine

### 3. Tester l'URL
Dans l'onglet "Preview" ou directement sur votre domaine :
- Ouvrez `https://votre-domaine.com/sitemap.xml`
- Vérifiez que le fichier s'affiche correctement

## Méthode 6 : Vérification avec les outils développeur

### Dans Chrome/Firefox :
1. Ouvrez `https://votre-domaine.com/sitemap.xml`
2. Ouvrez les outils développeur (F12)
3. Allez dans l'onglet "Network"
4. Rechargez la page
5. Cliquez sur la requête `sitemap.xml`
6. Vérifiez les headers :
   - `Content-Type: application/xml; charset=utf-8`
   - `Status: 200 OK`

## Problèmes courants et solutions

### ❌ Erreur 404 - Sitemap non trouvé
**Solution :**
- Vérifiez que les fichiers sont bien à la racine du projet
- Vérifiez que le déploiement Cloudflare est réussi
- Vérifiez que les fichiers ne sont pas dans `.gitignore`

### ❌ Content-Type incorrect (text/html au lieu de application/xml)
**Solution :**
- Vérifiez que le fichier `_headers` est bien déployé
- Vérifiez que le fichier `_headers` contient les bonnes règles
- Redéployez le site sur Cloudflare

### ❌ Sitemap vide ou malformé
**Solution :**
- Relancez le script `generate_sitemaps.py`
- Vérifiez que les fichiers HTML existent bien
- Vérifiez les logs du script de génération

### ❌ Google ne peut pas lire le sitemap
**Solutions :**
1. Vérifiez que le sitemap est accessible publiquement (pas de protection par mot de passe)
2. Vérifiez le Content-Type avec les outils développeur
3. Testez l'URL dans Google Search Console
4. Vérifiez que le fichier `_headers` est bien configuré

## Checklist de vérification

Avant de soumettre à Google Search Console :

- [ ] Le sitemap index est accessible : `https://votre-domaine.com/sitemap.xml`
- [ ] Le Content-Type est `application/xml; charset=utf-8`
- [ ] Le XML est valide (pas d'erreurs de syntaxe)
- [ ] Tous les sitemaps référencés sont accessibles
- [ ] Les URLs dans les sitemaps sont valides et accessibles
- [ ] Le fichier `_headers` est bien déployé
- [ ] Le dernier déploiement Cloudflare est réussi

## Commandes rapides

```bash
# Vérification complète
./check_sitemaps.sh votre-domaine.com

# Vérification rapide d'un sitemap
curl -I https://votre-domaine.com/sitemap.xml

# Compter les URLs
curl -s https://votre-domaine.com/sitemap-fr.xml | grep -c "<url>"

# Voir le contenu
curl https://votre-domaine.com/sitemap.xml | head -20
```

## Support

Si vous rencontrez des problèmes :
1. Utilisez le script `check_sitemaps.sh` pour diagnostiquer
2. Vérifiez les logs de déploiement Cloudflare
3. Testez avec les outils en ligne mentionnés ci-dessus

