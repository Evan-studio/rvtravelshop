# 🔧 Changer les DNS sur Hostinger

## ✅ Oui, c'est exactement ça !

Vous devez changer les serveurs DNS sur Hostinger pour pointer vers Cloudflare.

## 📋 Étapes précises

### 1. Allez sur votre compte Hostinger

- Connectez-vous à https://hpanel.hostinger.com
- Ou via votre interface Hostinger habituelle

### 2. Accédez à la gestion du domaine

- Allez dans **"Domains"** (ou **"Domaines"**)
- Cliquez sur **"Gérer"** pour `uni-ion.com`
- Ou cherchez **"DNS"** ou **"Nameservers"** dans le menu

### 3. Modifiez les serveurs DNS

1. Cherchez la section **"Nameservers"** ou **"Serveurs DNS"**
2. Vous verrez probablement quelque chose comme :
   ```
   ns1.dns-parking.com
   ns2.dns-parking.com
   ```
   (ou d'autres serveurs Hostinger)

3. **Remplacez-les par les serveurs Cloudflare :**
   ```
   julio.ns.cloudflare.com
   serenity.ns.cloudflare.com
   ```

4. Cliquez sur **"Sauvegarder"** ou **"Save"**

### 4. Confirmation

- Hostinger vous confirmera que les DNS ont été changés
- Vous verrez un message de confirmation

## ⏰ Délai

- **Propagation DNS** : 24-48h (parfois 1-2h seulement)
- Pendant ce temps, le site peut être inaccessible ou pointer vers l'ancien serveur

## ✅ Vérification

Après quelques heures, vous pouvez vérifier la propagation DNS :
- https://www.whatsmydns.net/#NS/uni-ion.com
- Entrez `uni-ion.com` et vérifiez que les serveurs DNS affichés sont ceux de Cloudflare

## ⚠️ Important

Une fois les DNS changés :
- ✅ Hostinger ne gère plus les DNS (c'est Cloudflare qui gère maintenant)
- ✅ Vous devez configurer les DNS dans Cloudflare, pas Hostinger
- ✅ Le domaine restera enregistré chez Hostinger, mais les DNS sont gérés par Cloudflare

## 📝 Résumé

**Serveurs DNS à mettre sur Hostinger :**
```
julio.ns.cloudflare.com
serenity.ns.cloudflare.com
```

C'est tout ! ✅

