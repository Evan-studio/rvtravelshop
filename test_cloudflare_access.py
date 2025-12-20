#!/usr/bin/env python3
"""
Script pour tester si Cloudflare bloque l'accès aux sitemaps et pages
Usage: python3 test_cloudflare_access.py [domaine]
"""

import sys
import requests
from urllib.parse import urlparse

# Couleurs
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'

def print_info(msg): print(f"{Colors.BLUE}ℹ️  {msg}{Colors.NC}")
def print_success(msg): print(f"{Colors.GREEN}✅ {msg}{Colors.NC}")
def print_warning(msg): print(f"{Colors.YELLOW}⚠️  {msg}{Colors.NC}")
def print_error(msg): print(f"{Colors.RED}❌ {msg}{Colors.NC}")
def print_header(msg): print(f"{Colors.CYAN}{msg}{Colors.NC}")

def test_url(url, user_agent="Mozilla/5.0"):
    """Teste l'accessibilité d'une URL avec un user-agent spécifique."""
    try:
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*'
        }
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        return response.status_code, response.headers.get('Content-Type', ''), response.headers
    except Exception as e:
        return None, None, str(e)

def main():
    """Fonction principale."""
    domain = sys.argv[1] if len(sys.argv) > 1 else "makita-6kq.pages.dev"
    domain = domain.rstrip('/').replace('https://', '').replace('http://', '')
    
    print("=" * 70)
    print_header("🔍 TEST D'ACCESSIBILITÉ CLOUDFLARE")
    print("=" * 70)
    print()
    print_info(f"Domaine: https://{domain}")
    print()
    
    # URLs à tester
    test_urls = [
        f"https://{domain}/sitemap-all.xml",
        f"https://{domain}/sitemap.xml",
        f"https://{domain}/robots.txt",
        f"https://{domain}/",
        f"https://{domain}/page_html/categories/1",
        f"https://{domain}/fr/",
        f"https://{domain}/fr/page_html/products/produit-1005009517477968",
    ]
    
    # User-agents à tester
    user_agents = {
        "Navigateur standard": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Googlebot-Image": "Googlebot-Image/1.0",
        "Bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        "Crawler générique": "Mozilla/5.0 (compatible; SemrushBot/7~bl; +http://www.semrush.com/bot.html)"
    }
    
    print_header("📋 TEST 1: Accessibilité avec différents user-agents")
    print("-" * 70)
    
    for url in test_urls[:3]:  # Tester seulement les sitemaps d'abord
        print()
        print_info(f"URL: {url}")
        
        for ua_name, ua_string in user_agents.items():
            status, content_type, headers = test_url(url, ua_string)
            
            if status == 200:
                print_success(f"  {ua_name}: OK (HTTP {status})")
            elif status == 403:
                print_error(f"  {ua_name}: BLOQUÉ (HTTP 403 - Forbidden)")
            elif status == 404:
                print_warning(f"  {ua_name}: Non trouvé (HTTP 404)")
            elif status:
                print_warning(f"  {ua_name}: HTTP {status}")
            else:
                print_error(f"  {ua_name}: Erreur de connexion")
    
    print()
    print_header("📋 TEST 2: Vérification des headers Cloudflare")
    print("-" * 70)
    
    url = f"https://{domain}/sitemap-all.xml"
    status, content_type, headers = test_url(url, "Googlebot")
    
    if headers and isinstance(headers, dict):
        print_info("Headers détectés:")
        cloudflare_headers = {k: v for k, v in headers.items() if 'cf-' in k.lower() or 'cloudflare' in k.lower()}
        
        if cloudflare_headers:
            for key, value in cloudflare_headers.items():
                print(f"  {key}: {value}")
        else:
            print_warning("Aucun header Cloudflare détecté (peut être normal pour Cloudflare Pages)")
        
        # Vérifier les headers de sécurité
        security_headers = ['x-content-type-options', 'content-type', 'cache-control']
        print()
        print_info("Headers de sécurité:")
        for header in security_headers:
            value = headers.get(header, 'Non défini')
            if value != 'Non défini':
                print_success(f"  {header}: {value}")
            else:
                print_warning(f"  {header}: Non défini")
    
    print()
    print_header("📋 TEST 3: Test d'accessibilité des pages référencées")
    print("-" * 70)
    
    # Tester quelques pages du sitemap
    page_urls = [
        f"https://{domain}/page_html/categories/1",
        f"https://{domain}/fr/",
        f"https://{domain}/fr/page_html/products/produit-1005009517477968",
    ]
    
    accessible = 0
    for url in page_urls:
        status, content_type, _ = test_url(url, "Googlebot")
        if status == 200:
            print_success(f"{url} → Accessible")
            accessible += 1
        elif status == 403:
            print_error(f"{url} → BLOQUÉ (403)")
        else:
            print_warning(f"{url} → HTTP {status}")
    
    print()
    print_info(f"Résultat: {accessible}/{len(page_urls)} pages accessibles")
    
    # Résumé final
    print()
    print("=" * 70)
    if accessible == len(page_urls):
        print_success("✅ TOUTES LES PAGES SONT ACCESSIBLES")
        print()
        print_info("💡 Si XML-Sitemaps.com dit toujours 'empty', le problème vient peut-être de:")
        print("   1. L'outil XML-Sitemaps.com lui-même (limitation de leur crawler)")
        print("   2. Essayez de soumettre directement dans Google Search Console")
        print("   3. Google devrait pouvoir lire le sitemap correctement")
    else:
        print_warning("⚠️  CERTAINES PAGES SONT BLOQUÉES")
        print()
        print_info("💡 Actions à faire:")
        print("   1. Vérifiez les règles de sécurité Cloudflare")
        print("   2. Créez une règle firewall pour autoriser les crawlers")
        print("   3. Vérifiez qu'aucune règle ne bloque les fichiers XML")
    print("=" * 70)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test annulé")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

