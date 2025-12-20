#!/bin/bash

# Script de mise à jour automatique vers GitHub
# Usage: ./update_github.sh [message de commit]

set -e  # Arrêter en cas d'erreur

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier qu'on est dans un dépôt Git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Ce n'est pas un dépôt Git !"
    exit 1
fi

echo "=========================================="
echo "🚀 MISE À JOUR VERS GITHUB"
echo "=========================================="
echo ""

# Vérifier s'il y a des changements
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    print_warning "Aucun changement détecté. Rien à commiter."
    exit 0
fi

# Afficher le statut
print_info "Statut actuel du dépôt :"
git status --short
echo ""

# Demander le message de commit
if [ -z "$1" ]; then
    echo -n "📝 Message de commit (ou appuyez sur Entrée pour message par défaut): "
    read -r commit_message
    if [ -z "$commit_message" ]; then
        commit_message="Update: Mise à jour du site $(date +'%Y-%m-%d %H:%M')"
    fi
else
    commit_message="$1"
fi

# Ajouter tous les fichiers modifiés
print_info "Ajout des fichiers modifiés..."
git add -A

# Compter les fichiers
files_count=$(git diff --cached --name-only | wc -l | tr -d ' ')
if [ "$files_count" -eq 0 ]; then
    print_warning "Aucun fichier à commiter."
    exit 0
fi

print_success "$files_count fichier(s) ajouté(s)"

# Créer le commit
print_info "Création du commit..."
if git commit -m "$commit_message"; then
    print_success "Commit créé avec succès"
else
    print_error "Erreur lors de la création du commit"
    exit 1
fi

# Afficher les informations du commit
echo ""
print_info "Détails du commit :"
git log -1 --stat --oneline
echo ""

# Demander confirmation avant le push
echo -n "📤 Pousser vers GitHub ? (o/N): "
read -r confirm
if [[ ! "$confirm" =~ ^[oO]$ ]]; then
    print_warning "Push annulé. Vous pouvez le faire manuellement avec: git push"
    exit 0
fi

# Push vers GitHub
print_info "Envoi vers GitHub..."
if git push origin main; then
    print_success "✅ Mise à jour envoyée vers GitHub avec succès !"
    echo ""
    print_info "🌐 Dépôt: $(git remote get-url origin)"
else
    print_error "Erreur lors du push vers GitHub"
    exit 1
fi

echo ""
echo "=========================================="
print_success "TERMINÉ !"
echo "=========================================="

