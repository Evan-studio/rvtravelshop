# ✅ Checklist après déploiement

## ⏰ Attendre 5-10 minutes

Cloudflare Pages met quelques minutes à déployer les modifications depuis GitHub.

## 🔍 Vérifications à faire (après 10 minutes)

### 1. Vérifier le Content-Type

```bash
curl -I https://makita-6kq.pages.dev/sitemap-all.xml | grep -i content-type
```

**Résultat attendu :** `content-type: application/xml`

### 2. Vérifier que le sitemap est accessible

```bash
curl -I https://makita-6kq.pages.dev/sitemap-all.xml
```

**Résultat attendu :** `HTTP/2 200`

### 3. Vérifier le nombre d'URLs

```bash
curl -s https://makita-6kq.pages.dev/sitemap-all.xml | grep -c "<url>"
```

**Résultat attendu :** `512`

## 📊 Dans Google Search Console

### Après 1-2 heures

1. Allez sur https://search.google.com/search-console
2. Menu "Sitemaps"
3. Vérifiez le statut de `sitemap-all.xml` ou `sitemap.xml`
4. Le statut devrait changer de "Impossible de vérifier" à "Réussi"

### Vérifier "Couverture"

Même si le sitemap dit "Impossible de vérifier", vérifiez :
1. Menu "Couverture" (à gauche)
2. Regardez le nombre de pages "Valides"
3. Si vous voyez des pages, c'est bon signe !

## ✅ Si tout est OK

- Content-Type : `application/xml` ✅
- Sitemap accessible : HTTP 200 ✅
- 512 URLs détectées ✅
- Statut Google : "Réussi" (après 1-2h) ✅

## ❌ Si problème persiste

1. Vérifiez que le fichier `_headers` est bien à la racine du projet
2. Vérifiez la configuration Build output dans Cloudflare Pages
3. Attendez encore 10-15 minutes (parfois ça prend plus de temps)
4. Testez avec le script : `python3 diagnose_google_error.py makita-6kq.pages.dev`

## 📝 Notes

- Le fichier `_headers` doit être dans le **Build output directory**
- Si Build output = `/` ou vide → `_headers` à la racine ✅
- Format : 2 espaces d'indentation (pas de tabs)

