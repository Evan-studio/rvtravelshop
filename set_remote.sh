#!/bin/bash
# Script pour pointer le remote Git vers un dépôt GitHub.
# Modifie simplement les variables ci-dessous, puis lance : ./set_remote.sh

set -e

# Renseigne ton compte et le nom du dépôt
GITHUB_USER="ton-compte"
REPO_NAME="sport4all"

echo "🚀 Mise à jour du remote origin vers https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

# Supprimer l'ancien origin s'il existe
git remote remove origin 2>/dev/null || true

# Ajouter le nouveau origin
git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

# Afficher le résultat
git remote -v

echo "✅ Remote mis à jour."




