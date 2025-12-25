# Résolution de l'erreur 403 : access_denied

## Problème
L'application OAuth est en mode test et seuls les testeurs approuvés peuvent y accéder.

## Solution : Ajouter votre compte comme testeur

### Étapes :

1. **Allez dans Google Cloud Console**
   - https://console.cloud.google.com/
   - Sélectionnez le projet : `upload-youtube-481709` (ou le projet correspondant à votre Client ID)

2. **Accédez à l'écran de consentement OAuth**
   - Menu latéral → **APIs & Services** → **OAuth consent screen**
   - Ou directement : https://console.cloud.google.com/apis/credentials/consent

3. **Ajoutez des utilisateurs de test**
   - Dans la section **Test users** (Utilisateurs de test)
   - Cliquez sur **+ ADD USERS**
   - Entrez votre adresse email Google (celle que vous utilisez pour YouTube)
   - Cliquez sur **ADD**

4. **Vérifiez les scopes**
   - Assurez-vous que le scope `https://www.googleapis.com/auth/youtube.upload` est présent
   - Si ce n'est pas le cas, ajoutez-le dans **Scopes**

5. **Réessayez l'authentification**
   - Relancez le script `auto_upload_videos.py`
   - L'authentification devrait maintenant fonctionner

## Alternative : Publier l'application (pour un accès public)

Si vous voulez que n'importe qui puisse utiliser l'application :
1. Dans l'écran de consentement OAuth, cliquez sur **PUBLISH APP**
2. **ATTENTION** : Cela nécessite une vérification par Google si vous utilisez des scopes sensibles
3. Pour YouTube upload, Google peut demander une vérification de sécurité

## Note importante
- En mode test, vous pouvez avoir jusqu'à 100 utilisateurs de test
- Chaque utilisateur doit être ajouté manuellement
- Les tokens expirent après 7 jours en mode test (mais peuvent être rafraîchis)


