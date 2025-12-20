#!/bin/bash

# Script de vérification des sitemaps sur Cloudflare
# Usage: ./check_sitemaps.sh [votre-domaine.com]

set -e

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

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

print_header() {
    echo -e "${CYAN}$1${NC}"
}

# Récupérer le domaine
if [ -z "$1" ]; then
    # Essayer de récupérer le domaine depuis translations.csv
    if [ -f "translations.csv" ]; then
        domain=$(grep "site.domain" translations.csv | cut -d',' -f2 | tr -d ' ' | head -1)
        if [ -z "$domain" ]; then
            domain="makita-6kq.pages.dev"
        fi
    else
        domain="makita-6kq.pages.dev"
    fi
    print_warning "Domaine non fourni, utilisation par défaut: $domain"
    echo ""
    echo "💡 Pour utiliser un autre domaine: ./check_sitemaps.sh votre-domaine.com"
    echo ""
else
    domain="$1"
fi

# Nettoyer le domaine (enlever https:// et /)
domain=$(echo "$domain" | sed 's|https\?://||' | sed 's|/$||')

echo "=========================================="
print_header "🔍 VÉRIFICATION DES SITEMAPS"
echo "=========================================="
echo ""
print_info "Domaine: https://$domain"
echo ""

# Fonction pour vérifier une URL
check_url() {
    local url="$1"
    local name="$2"
    
    echo -n "  Vérification de $name... "
    
    # Vérifier si l'URL est accessible
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null || echo "000")
    
    if [ "$response" = "200" ]; then
        # Vérifier le Content-Type
        content_type=$(curl -s -I "$url" | grep -i "content-type" | cut -d':' -f2 | tr -d ' ' || echo "")
        
        # Vérifier la taille
        size=$(curl -s "$url" | wc -c)
        size_kb=$((size / 1024))
        
        if echo "$content_type" | grep -qi "xml"; then
            print_success "OK (${size_kb}KB, $content_type)"
            return 0
        else
            print_warning "Accessible mais Content-Type incorrect: $content_type"
            return 1
        fi
    elif [ "$response" = "000" ]; then
        print_error "Timeout ou erreur de connexion"
        return 1
    else
        print_error "Erreur HTTP: $response"
        return 1
    fi
}

# Fonction pour compter les URLs dans un sitemap
count_urls() {
    local url="$1"
    local count=$(curl -s "$url" 2>/dev/null | grep -c "<url>" || echo "0")
    echo "$count"
}

# Fonction pour vérifier la validité XML
check_xml_validity() {
    local url="$1"
    local xml_content=$(curl -s "$url" 2>/dev/null)
    
    if echo "$xml_content" | grep -q "<?xml"; then
        # Vérifier les balises de base
        if echo "$xml_content" | grep -q "<urlset\|<sitemapindex"; then
            return 0
        else
            return 1
        fi
    else
        return 1
    fi
}

# Liste des sitemaps à vérifier
sitemaps=(
    "sitemap.xml:sitemap index"
    "sitemap-en.xml:sitemap anglais"
    "sitemap-fr.xml:sitemap français"
    "sitemap-de.xml:sitemap allemand"
    "sitemap-es.xml:sitemap espagnol"
    "sitemap-pt.xml:sitemap portugais"
)

print_header "📋 1. VÉRIFICATION DE L'ACCESSIBILITÉ"
echo "----------------------------------------"

all_ok=true
accessible_sitemaps=()

for sitemap_info in "${sitemaps[@]}"; do
    sitemap_file=$(echo "$sitemap_info" | cut -d':' -f1)
    sitemap_name=$(echo "$sitemap_info" | cut -d':' -f2)
    url="https://$domain/$sitemap_file"
    
    if check_url "$url" "$sitemap_name"; then
        accessible_sitemaps+=("$url")
    else
        all_ok=false
    fi
done

echo ""

# Vérifier le sitemap index
print_header "📊 2. ANALYSE DU SITEMAP INDEX"
echo "----------------------------------------"

sitemap_index_url="https://$domain/sitemap.xml"
if check_url "$sitemap_index_url" "sitemap index" > /dev/null 2>&1; then
    sitemap_count=$(curl -s "$sitemap_index_url" | grep -c "<sitemap>" || echo "0")
    print_info "Nombre de sitemaps référencés: $sitemap_count"
    
    # Lister les sitemaps référencés
    echo ""
    print_info "Sitemaps référencés dans l'index:"
    curl -s "$sitemap_index_url" | grep "<loc>" | sed 's|.*<loc>\(.*\)</loc>.*|\1|' | while read -r ref_url; do
        echo "  - $ref_url"
    done
else
    print_error "Le sitemap index n'est pas accessible"
    all_ok=false
fi

echo ""

# Vérifier le nombre d'URLs dans chaque sitemap
print_header "🔢 3. COMPTAGE DES URLs"
echo "----------------------------------------"

for sitemap_info in "${sitemaps[@]}"; do
    sitemap_file=$(echo "$sitemap_info" | cut -d':' -f1)
    sitemap_name=$(echo "$sitemap_info" | cut -d':' -f2)
    url="https://$domain/$sitemap_file"
    
    if [[ " ${accessible_sitemaps[@]} " =~ " ${url} " ]]; then
        count=$(count_urls "$url")
        if [ "$count" -gt 0 ]; then
            print_success "$sitemap_name: $count URL(s)"
        else
            print_warning "$sitemap_name: Aucune URL trouvée"
        fi
    fi
done

echo ""

# Vérifier la validité XML
print_header "✅ 4. VALIDITÉ XML"
echo "----------------------------------------"

for sitemap_info in "${sitemaps[@]}"; do
    sitemap_file=$(echo "$sitemap_info" | cut -d':' -f1)
    sitemap_name=$(echo "$sitemap_info" | cut -d':' -f2)
    url="https://$domain/$sitemap_file"
    
    if [[ " ${accessible_sitemaps[@]} " =~ " ${url} " ]]; then
        if check_xml_validity "$url"; then
            print_success "$sitemap_name: XML valide"
        else
            print_error "$sitemap_name: XML invalide ou malformé"
            all_ok=false
        fi
    fi
done

echo ""

# Vérifier les headers HTTP
print_header "🌐 5. VÉRIFICATION DES HEADERS HTTP"
echo "----------------------------------------"

sitemap_index_url="https://$domain/sitemap.xml"
content_type=$(curl -s -I "$sitemap_index_url" 2>/dev/null | grep -i "content-type" | cut -d':' -f2 | tr -d ' ' || echo "non trouvé")

if echo "$content_type" | grep -qi "xml"; then
    print_success "Content-Type correct: $content_type"
else
    print_warning "Content-Type: $content_type (devrait être application/xml)"
    print_info "💡 Vérifiez que le fichier _headers est bien déployé sur Cloudflare"
fi

echo ""

# Résumé final
echo "=========================================="
if [ "$all_ok" = true ]; then
    print_success "✅ TOUS LES SITEMAPS SONT ACCESSIBLES ET VALIDES"
else
    print_warning "⚠️  CERTAINS SITEMAPS ONT DES PROBLÈMES"
fi
echo "=========================================="
echo ""

# Liens utiles
print_header "🔗 LIENS UTILES"
echo "----------------------------------------"
echo "  • Sitemap index: https://$domain/sitemap.xml"
echo "  • Google Search Console: https://search.google.com/search-console"
echo "  • Validateur XML: https://www.xml-sitemaps.com/validate-xml-sitemap.html"
echo "  • Testeur de sitemap: https://www.xml-sitemaps.com/sitemap-validator.html"
echo ""

