# 🔧 Guide : Configurer uni-ion.com sur Cloudflare et Hostinger

## 🎯 Objectif

Ajouter votre domaine personnalisé `uni-ion.com` (Hostinger) à votre site Cloudflare Pages existant (`makita-6kq.pages.dev`).

**⚠️ IMPORTANT :** Vous n'avez PAS besoin de créer un nouveau site ! On ajoute simplement le domaine au site existant. Aucun fichier à copier !

## 📋 Étapes détaillées

### ÉTAPE 1 : Ajouter le domaine dans Cloudflare

1. **Allez sur Cloudflare Dashboard**
   - URL : https://dash.cloudflare.com
   - Connectez-vous à votre compte

2. **Ajouter le site**
   - Cliquez sur **"Add a site"** (en haut à droite)
   - Entrez : `uni-ion.com`
   - Cliquez sur **"Add site"**

3. **Choisir le plan**
   - Sélectionnez le plan **Free** (gratuit)
   - Cliquez sur **"Continue"**

4. **Cloudflare scanne votre domaine**
   - Cloudflare va détecter automatiquement les enregistrements DNS existants
   - Cela peut prendre 1-2 minutes

5. **Obtenir les serveurs DNS Cloudflare** ⚠️ IMPORTANT
   - Après le scan, Cloudflare vous affichera **2 serveurs DNS**
   - Ils ressemblent à :
     ```
     dante.ns.cloudflare.com
     gwen.ns.cloudflare.com
     ```
   - **Notez ces 2 serveurs DNS !** Vous en aurez besoin pour Hostinger

### ÉTAPE 2 : Changer les DNS sur Hostinger

1. **Allez sur votre compte Hostinger**
   - Connectez-vous à https://hpanel.hostinger.com
   - Ou via votre interface Hostinger habituelle

2. **Accéder à la gestion du domaine**
   - Allez dans **"Domains"** (ou **"Domaines"**)
   - Cliquez sur **"Gérer"** pour `uni-ion.com`
   - Ou cherchez **"DNS"** ou **"Nameservers"**

3. **Modifier les serveurs DNS**
   - Cherchez la section **"Nameservers"** ou **"Serveurs DNS"**
   - Remplacez les serveurs DNS actuels par ceux de Cloudflare :
     ```
     dante.ns.cloudflare.com
     gwen.ns.cloudflare.com
     ```
   - Cliquez sur **"Sauvegarder"** ou **"Save"**

4. **Confirmation**
   - Hostinger vous confirmera que les DNS ont été changés
   - **Note** : La propagation DNS peut prendre 24-48h (parfois moins)

### ÉTAPE 3 : Configurer les DNS dans Cloudflare

1. **Dans Cloudflare Dashboard**
   - Allez dans votre domaine `uni-ion.com`
   - Cliquez sur **"DNS"** dans le menu de gauche
   - Cliquez sur **"Records"**

2. **Supprimer les enregistrements inutiles** (optionnel)
   - Cloudflare a peut-être importé des enregistrements depuis Hostinger
   - Vous pouvez supprimer ceux qui ne sont pas nécessaires

3. **Ajouter un enregistrement CNAME** (si pas déjà fait)
   - Cliquez sur **"Add record"**
   - **Type** : `CNAME`
   - **Name** : `@` (ou laissez vide pour la racine)
   - **Target** : `makita-6kq.pages.dev`
   - **Proxy status** : Proxied (orange cloud) ✅
   - Cliquez sur **"Save"**

   **Note** : Cloudflare Pages peut créer cet enregistrement automatiquement à l'étape suivante.

### ÉTAPE 4 : Connecter le domaine à votre site Cloudflare Pages existant

**⚠️ IMPORTANT :** Vous n'avez PAS besoin de créer un nouveau site ! On ajoute simplement le domaine au site existant.

1. **Dans Cloudflare Dashboard**
   - Allez dans **"Pages"** (menu de gauche)
   - Sélectionnez votre projet **`makita`** (votre site existant)

2. **Ajouter un domaine personnalisé**
   - Cliquez sur l'onglet **"Custom domains"**
   - Cliquez sur **"Set up a custom domain"**
   - Entrez : `uni-ion.com`
   - Cliquez sur **"Add domain"**

3. **Vérification**
   - Cloudflare va vérifier que le domaine pointe bien vers Cloudflare
   - Si les DNS ne sont pas encore propagés, vous verrez un message d'attente
   - Le statut passera à **"Active"** une fois que tout est configuré

4. **Enregistrement CNAME automatique**
   - Cloudflare Pages créera automatiquement l'enregistrement CNAME nécessaire
   - Vous n'avez normalement pas besoin de le créer manuellement

**Résultat :** Votre site sera accessible à la fois sur :
- `https://makita-6kq.pages.dev` (ancien domaine, toujours actif)
- `https://uni-ion.com` (nouveau domaine personnalisé)

**Aucun fichier à copier !** Les deux domaines pointent vers le même site.

### ÉTAPE 5 : Vérifier la configuration

**Attendez 5-10 minutes** après avoir connecté le domaine, puis testez :

```bash
# Vérifier que le domaine fonctionne
curl -I https://uni-ion.com

# Vérifier le sitemap
curl -I https://uni-ion.com/sitemap-all.xml

# Vérifier le Content-Type
curl -I https://uni-ion.com/sitemap-all.xml | grep content-type
```

**Résultats attendus :**
- Le site devrait s'afficher sur `https://uni-ion.com`
- Le sitemap devrait être accessible
- Le Content-Type devrait être `application/xml`

## ⏰ Délais importants

- **Propagation DNS** : 24-48h (parfois 1-2h)
- **Activation Cloudflare Pages** : 5-10 minutes après connexion
- **SSL/TLS** : Généré automatiquement par Cloudflare (gratuit)

## 🔍 Vérifier la propagation DNS

Utilisez un outil en ligne pour vérifier :
- https://www.whatsmydns.net/#CNAME/uni-ion.com
- Entrez `uni-ion.com` et vérifiez que ça pointe vers Cloudflare

## ⚠️ Points importants

1. **Vous n'avez PAS besoin de créer un nouveau site Cloudflare Pages** :
   - On ajoute simplement le domaine personnalisé au site existant
   - Aucun fichier à copier ou déplacer
   - Les deux domaines (`makita-6kq.pages.dev` et `uni-ion.com`) pointent vers le même site

2. **Une fois les DNS changés sur Hostinger** :
   - Hostinger ne gère plus les DNS (c'est Cloudflare qui gère)
   - Vous devez configurer les DNS dans Cloudflare, pas Hostinger

3. **SSL/TLS** :
   - Cloudflare génère automatiquement un certificat SSL gratuit
   - HTTPS fonctionnera automatiquement

4. **Cache** :
   - Cloudflare peut mettre en cache
   - Si besoin, purgez le cache dans Cloudflare Dashboard > Caching > Purge Everything

5. **Sous-domaines** :
   - Si vous voulez `www.uni-ion.com`, ajoutez aussi un CNAME pour `www` pointant vers `makita-6kq.pages.dev`

## ✅ Checklist

- [ ] Domaine ajouté dans Cloudflare
- [ ] Serveurs DNS Cloudflare notés
- [ ] DNS changés sur Hostinger
- [ ] Enregistrement CNAME configuré dans Cloudflare (ou créé automatiquement)
- [ ] Domaine connecté à Cloudflare Pages
- [ ] Statut "Active" dans Cloudflare Pages
- [ ] Site accessible sur https://uni-ion.com
- [ ] Sitemap accessible sur https://uni-ion.com/sitemap-all.xml
- [ ] SSL/TLS actif (cadenas vert dans le navigateur)

## 🆘 Si ça ne fonctionne pas

1. **Vérifiez la propagation DNS** (whatsmydns.net)
2. **Vérifiez que le domaine est "Active" dans Cloudflare Pages**
3. **Attendez 24-48h** si les DNS viennent d'être changés
4. **Vérifiez les enregistrements DNS dans Cloudflare**
5. **Purgez le cache Cloudflare** si nécessaire

## 📝 Après configuration

Une fois que tout fonctionne :

1. **Soumettre le sitemap dans Google Search Console**
   - Créez une nouvelle propriété pour `uni-ion.com`
   - Soumettez : `https://uni-ion.com/sitemap-all.xml`

2. **Comparer avec l'ancien domaine**
   - Vérifiez si Google indexe mieux avec le domaine personnalisé
   - Comparez les résultats après 24-48h

