# 🔧 Configuration DNS Cloudflare pour uni-ion.com

## 📋 Enregistrements DNS actuels détectés

Cloudflare a détecté vos enregistrements DNS existants. Voici ce qu'il faut faire :

## ✅ À GARDER (ne pas toucher)

### Enregistrements CAA
- **Tous les 12 enregistrements CAA** : ✅ **GARDER**
- Ces enregistrements sont nécessaires pour les certificats SSL
- Laissez-les en **DNS only** (nuage gris)

### Enregistrements NS
- Les 2 enregistrements NS seront automatiquement remplacés quand vous changerez les nameservers sur Hostinger
- Ne les supprimez pas maintenant

## ❌ À SUPPRIMER ou MODIFIER

### 1. Enregistrements A (pointant vers Hostinger)

**À SUPPRIMER :**
- `A` - `ftp` → `77.37.36.46` (si vous n'utilisez pas FTP)
- `A` - `uni-ion.com` → `77.37.76.97` (Proxied) ❌ **SUPPRIMER**
- `A` - `uni-ion.com` → `92.112.198.12` (Proxied) ❌ **SUPPRIMER**

**Pourquoi ?** Ces enregistrements pointent vers les serveurs Hostinger. On va les remplacer par un CNAME pointant vers Cloudflare Pages.

### 2. Enregistrements AAAA (IPv6)

**À SUPPRIMER :**
- `AAAA` - `uni-ion.com` → `2a02:4780:4f:f004:da4c:54f5:52da:4429` (Proxied) ❌ **SUPPRIMER**
- `AAAA` - `uni-ion.com` → `2a02:4780:4e:e8b7:80c6:1ac9:4093:106d` (Proxied) ❌ **SUPPRIMER**

**Pourquoi ?** Cloudflare Pages n'utilise pas d'enregistrements AAAA directs. Le CNAME gérera tout.

### 3. Enregistrement CNAME www

**À MODIFIER :**
- `CNAME` - `www` → `www.uni-ion.com.cdn.hstgr.net` (Proxied) ❌ **MODIFIER**

**Nouveau contenu :**
- `CNAME` - `www` → `makita-6kq.pages.dev` (Proxied) ✅

## ✅ À AJOUTER

### CNAME pour la racine (@)

**À AJOUTER :**
- **Type** : `CNAME`
- **Name** : `@` (ou `uni-ion.com`)
- **Target** : `makita-6kq.pages.dev`
- **Proxy status** : **Proxied** (nuage orange) ✅
- **TTL** : Auto

**Note :** Cloudflare Pages peut créer cet enregistrement automatiquement quand vous connectez le domaine. Mais vous pouvez aussi le créer manuellement.

## 📝 Étapes à suivre dans Cloudflare

### Étape 1 : Supprimer les anciens enregistrements

1. Dans **DNS > Records**
2. Supprimez les enregistrements suivants (cliquez sur **Delete**) :
   - `A` - `ftp` → `77.37.36.46` (si pas utilisé)
   - `A` - `uni-ion.com` → `77.37.76.97`
   - `A` - `uni-ion.com` → `92.112.198.12`
   - `AAAA` - `uni-ion.com` → `2a02:4780:4f:f004:da4c:54f5:52da:4429`
   - `AAAA` - `uni-ion.com` → `2a02:4780:4e:e8b7:80c6:1ac9:4093:106d`

### Étape 2 : Modifier le CNAME www

1. Trouvez l'enregistrement `CNAME` - `www`
2. Cliquez sur **Edit**
3. Changez le **Content** de `www.uni-ion.com.cdn.hstgr.net` vers `makita-6kq.pages.dev`
4. Assurez-vous que **Proxy status** est **Proxied** (nuage orange)
5. Cliquez sur **Save**

### Étape 3 : Ajouter le CNAME pour la racine

**Option A : Créer manuellement**
1. Cliquez sur **Add record**
2. **Type** : `CNAME`
3. **Name** : `@` (ou laissez vide)
4. **Target** : `makita-6kq.pages.dev`
5. **Proxy status** : **Proxied** (nuage orange) ✅
6. Cliquez sur **Save**

**Option B : Laisser Cloudflare Pages le créer**
- Quand vous connecterez le domaine dans Cloudflare Pages (étape suivante), il créera automatiquement cet enregistrement

## ⚠️ Important

1. **Ne supprimez PAS les enregistrements CAA** - ils sont nécessaires pour SSL
2. **Ne supprimez PAS les NS maintenant** - ils seront remplacés automatiquement
3. **Gardez le CNAME www** mais modifiez-le pour pointer vers Cloudflare Pages

## ✅ Résultat final attendu

Après configuration, vous devriez avoir :

```
Type    Name          Content                    Proxy
----    ----          -------                     -----
CNAME   @             makita-6kq.pages.dev       Proxied ✅
CNAME   www           makita-6kq.pages.dev       Proxied ✅
CAA     uni-ion.com   (12 enregistrements)       DNS only ✅
NS      uni-ion.com   (sera remplacé auto)       DNS only
```

## 🎯 Prochaine étape

Une fois les DNS configurés :
1. Changez les nameservers sur Hostinger (vers ceux de Cloudflare)
2. Connectez le domaine dans Cloudflare Pages (Pages > makita > Custom domains)

## 📝 Note sur l'email

Cloudflare vous a averti qu'il n'y a pas d'enregistrement MX. Si vous utilisez l'email avec `@uni-ion.com`, vous devrez ajouter un enregistrement MX après avoir configuré le domaine pour le web.

