# Configuration Cloudflare Pages avec domaine personnalisé

## Étapes pour associer votre domaine à Cloudflare Pages

### 1. Dans Cloudflare Pages
1. Allez dans **Cloudflare Dashboard** → **Pages**
2. Sélectionnez votre projet (rvtravelshop)
3. Allez dans **Custom domains**
4. Cliquez sur **Set up a custom domain**
5. Entrez votre domaine (ex: `rvtravelshop.com`)
6. Cloudflare vous donnera un **CNAME target** (ex: `rvtravelshop.pages.dev`)

### 2. Dans Cloudflare DNS
1. Allez dans **DNS** → **Records**
2. **Supprimez** ou **modifiez** les enregistrements existants qui pointent vers le plan gratuit :
   - Si vous avez un enregistrement **A** ou **CNAME** pour `@` (racine)
   - Si vous avez un enregistrement **CNAME** pour `www`

3. **Ajoutez/modifiez** les enregistrements pour pointer vers Pages :
   - **Pour la racine (`@`)** :
     - Type: **CNAME**
     - Name: `@`
     - Target: `rvtravelshop.pages.dev` (ou le CNAME target donné par Pages)
     - Proxy: **Proxied** (nuage orange activé)
   
   - **Pour www** :
     - Type: **CNAME**
     - Name: `www`
     - Target: `rvtravelshop.pages.dev` (ou le CNAME target donné par Pages)
     - Proxy: **Proxied** (nuage orange activé)

### 3. Vérification
- Attendez quelques minutes pour la propagation DNS
- Vérifiez dans Cloudflare Pages que le domaine est **Active**
- Testez votre site sur votre domaine

## Notes importantes
- **Proxy activé** (nuage orange) : Utilise le CDN Cloudflare
- **Proxy désactivé** (nuage gris) : DNS seulement
- Pour Pages, utilisez **Proxy activé** (recommandé)


