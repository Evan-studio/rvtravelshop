# 📤 Scripts de mise à jour GitHub

Deux scripts sont disponibles pour faciliter les mises à jour vers GitHub :

## 🚀 Scripts disponibles

### 1. `update_github.sh` (avec confirmation)
Script interactif qui demande confirmation avant de pousser vers GitHub.

**Utilisation :**
```bash
./update_github.sh
```

ou avec un message personnalisé :
```bash
./update_github.sh "Mon message de commit"
```

**Fonctionnalités :**
- ✅ Affiche les fichiers modifiés
- ✅ Demande un message de commit (ou utilise un message par défaut)
- ✅ Demande confirmation avant le push
- ✅ Affiche les détails du commit

### 2. `update_github_auto.sh` (automatique)
Script qui pousse automatiquement sans demander de confirmation.

**Utilisation :**
```bash
./update_github_auto.sh
```

ou avec un message personnalisé :
```bash
./update_github_auto.sh "Correction des sitemaps"
```

**Fonctionnalités :**
- ✅ Affiche les fichiers modifiés
- ✅ Utilise un message par défaut ou celui fourni
- ✅ Push automatique vers GitHub
- ✅ Plus rapide pour les mises à jour fréquentes

## 📝 Exemples d'utilisation

### Mise à jour simple avec message par défaut
```bash
./update_github.sh
# Appuyez sur Entrée pour le message par défaut
# Tapez 'o' pour confirmer le push
```

### Mise à jour avec message personnalisé
```bash
./update_github.sh "Ajout de nouvelles fonctionnalités SEO"
```

### Mise à jour rapide (automatique)
```bash
./update_github_auto.sh "Fix: Correction bug sitemap"
```

## ⚙️ Ce que font les scripts

1. ✅ Vérifient qu'on est dans un dépôt Git
2. ✅ Détectent les fichiers modifiés
3. ✅ Ajoutent tous les fichiers (`git add -A`)
4. ✅ Créent un commit avec votre message
5. ✅ Poussent vers GitHub (`git push origin main`)

## 🔍 Vérification

Après l'exécution, vous pouvez vérifier sur GitHub :
- https://github.com/Evan-studio/makita

## 💡 Astuce

Pour rendre les scripts encore plus faciles à utiliser, vous pouvez créer un alias dans votre `.zshrc` ou `.bashrc` :

```bash
alias update-github='cd "/Users/terrybauer/Documents/site affiliation/Makita" && ./update_github_auto.sh'
```

Ensuite, depuis n'importe où, vous pouvez simplement taper :
```bash
update-github "Mon message"
```

