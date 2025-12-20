# ✅ Ajouter le CNAME dans Cloudflare

## 🎯 Situation

Vous avez changé les nameservers sur Hostinger vers Cloudflare. Maintenant, **Cloudflare gère les DNS**, donc vous devez ajouter le CNAME dans **Cloudflare**, pas dans Hostinger.

## 📋 Étapes

### 1. Allez dans Cloudflare DNS

1. **Cloudflare Dashboard**
   - Allez dans votre domaine `uni-ion.com` (pas dans Pages)
   - Cliquez sur **"DNS"** dans le menu de gauche
   - Cliquez sur **"Records"**

### 2. Ajoutez le CNAME

1. Cliquez sur **"Add record"**

2. Remplissez :
   - **Type** : `CNAME`
   - **Name** : `@` (ou laissez vide, ou `uni-ion.com`)
   - **Target** : `makita-6kq.pages.dev`
   - **Proxy status** : **Proxied** (nuage orange) ✅
   - **TTL** : Auto

3. Cliquez sur **"Save"**

### 3. Vérifiez dans Cloudflare Pages

1. Retournez dans **Pages > makita > Custom domains**
2. Cliquez sur **"Check DNS records"** (ou attendez quelques secondes)
3. Cloudflare devrait détecter le CNAME et activer le domaine automatiquement

## ⚠️ Important

- **Name** : Utilisez `@` pour la racine (ou laissez vide)
- **Proxy status** : Doit être **Proxied** (nuage orange) ✅
- **Target** : Exactement `makita-6kq.pages.dev` (sans https://)

## ✅ Résultat

Après avoir ajouté le CNAME :
- Cloudflare Pages détectera automatiquement le CNAME
- Le statut passera à "Active"
- Le certificat SSL sera généré automatiquement (5-10 minutes)

## 🎯 Alternative : Laisser Cloudflare Pages le créer

Si vous préférez, vous pouvez aussi :
1. Ignorer cette étape
2. Cloudflare Pages créera automatiquement le CNAME quand vous cliquez sur "Check DNS records"

Mais il est plus rapide de le créer manuellement.

