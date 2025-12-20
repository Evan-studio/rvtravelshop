#!/bin/bash
# Script pour installer Git LFS et configurer le dépôt

echo "=============================================================================="
echo "🔧 INSTALLATION ET CONFIGURATION DE GIT LFS"
echo "=============================================================================="
echo ""

# Vérifier si Homebrew est installé
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew n'est pas installé"
    echo ""
    echo "💡 Pour installer Homebrew:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo "🔄 Installation de Git LFS via Homebrew..."
brew install git-lfs

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation"
    exit 1
fi

echo "✅ Git LFS installé"
echo ""

echo "🔄 Configuration de Git LFS..."
git lfs install

echo ""
echo "🔄 Configuration pour les images WebP..."
git lfs track "*.webp"

echo ""
echo "🔄 Ajout de .gitattributes..."
git add .gitattributes

echo ""
echo "=============================================================================="
echo "✅ GIT LFS CONFIGURÉ!"
echo "=============================================================================="
echo ""
echo "💡 Maintenant, vous devez:"
echo "   1. Migrer les images existantes vers LFS:"
echo "      git lfs migrate import --include='*.webp' --everything"
echo ""
echo "   2. Puis push vers GitHub:"
echo "      git push origin main --force"
echo ""

