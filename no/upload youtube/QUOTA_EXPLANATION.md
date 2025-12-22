# Quota YouTube vs Utilisateurs OAuth

## Quota YouTube (par compte)

**Chaque compte YouTube a son propre quota :**
- Compte standard : **6 uploads par jour**
- Compte YouTube Partner : Quota plus élevé (variable)
- Le quota est lié au **compte YouTube**, pas à l'application OAuth

## Utilisateurs de test OAuth

**Ajouter plusieurs utilisateurs de test dans Google Cloud Console :**
- Permet à plusieurs personnes de s'authentifier avec l'application
- **Chaque utilisateur garde son propre quota YouTube**
- Si vous avez 3 utilisateurs de test :
  - Utilisateur 1 : 6 uploads/jour sur sa chaîne
  - Utilisateur 2 : 6 uploads/jour sur sa chaîne
  - Utilisateur 3 : 6 uploads/jour sur sa chaîne
  - **Total : 18 uploads/jour (mais sur 3 chaînes différentes)**

## Important

- Le quota est **par compte YouTube**, pas par application
- Ajouter des utilisateurs de test ne multiplie pas le quota d'un seul compte
- Si vous voulez uploader plus de 6 vidéos/jour sur **une seule chaîne**, vous devez :
  1. Devenir YouTube Partner (quota plus élevé)
  2. Attendre 24h entre les uploads
  3. Utiliser plusieurs comptes YouTube (chaque compte = 6 uploads/jour)

## Exemple concret

- Vous avez 1 compte YouTube : **6 uploads/jour max**
- Vous ajoutez 10 utilisateurs de test dans OAuth : **Toujours 6 uploads/jour sur votre chaîne**
- Les 10 utilisateurs peuvent uploader sur **leurs propres chaînes** (6 chacun)

