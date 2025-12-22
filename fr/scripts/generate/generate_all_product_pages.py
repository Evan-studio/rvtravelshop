#!/usr/bin/env python3
"""
Script pour générer toutes les pages produit en HTML statique.

Ce script lit les produits depuis all_products.csv et génère une page HTML
statique pour chaque produit, sans JavaScript. Les pages sont générées avec
le menu et footer depuis translations.csv.

Usage:
    python3 scripts/generate/generate_all_product_pages.py
"""

import csv
import re
import random
import unicodedata
import json
from datetime import datetime
from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).parent.parent.parent
TRANSLATIONS_CSV = BASE_DIR / 'translations.csv'
PRODUCTS_CSV = BASE_DIR / 'CSV' / 'all_products.csv'
TEMPLATE_PRODUCT = BASE_DIR / 'page_html' / 'templates' / 'produit.html'
PRODUCTS_DIR = BASE_DIR / 'page_html' / 'products'

def slugify(text):
    """Convertit un texte en slug (minuscules, tirets, sans accents)."""
    if not text:
        return ''
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = unicodedata.normalize('NFD', slug)
    slug = slug.encode('ascii', 'ignore').decode('ascii')
    slug = slug.strip('-')
    return slug

def detect_language_code():
    """Détecte le code de langue depuis le nom du dossier (fr, de, es, etc.)."""
    base_name = BASE_DIR.name.lower()
    # Si le nom du dossier est une langue (2 lettres), c'est la langue cible
    if len(base_name) == 2 and base_name.isalpha():
        return base_name
    # Sinon, par défaut anglais
    return 'en'

def load_translations_from_csv():
    """Charge toutes les traductions depuis translations.csv (colonne détectée automatiquement)."""
    translations = {}
    
    if not TRANSLATIONS_CSV.exists():
        print(f"❌ Fichier non trouvé: {TRANSLATIONS_CSV}")
        return translations
    
    # Détecter la langue du dossier
    lang_code = detect_language_code()
    
    try:
        with open(TRANSLATIONS_CSV, 'r', encoding='utf-8') as f:
            # Détecter automatiquement le séparateur (virgule ou point-virgule)
            first_line = f.readline()
            f.seek(0)
            delimiter = ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','
            reader = csv.DictReader(f, delimiter=delimiter)
            fieldnames = reader.fieldnames
            
            # Chercher la colonne de langue : {lang_code}_auto en priorité, puis {lang_code}, puis 'en'
            lang_col = None
            if f'{lang_code}_auto' in fieldnames:
                lang_col = f'{lang_code}_auto'
            elif lang_code in fieldnames:
                lang_col = lang_code
            else:
                lang_col = 'en'  # Fallback sur anglais
            
            for row in reader:
                key = row.get('key', '').strip()
                if key:
                    # Utiliser la colonne détectée
                    value = row.get(lang_col, '').strip()
                    # Ignorer les formules (commencent par =) et les cellules vides
                    if value and not value.startswith('='):
                        translations[key] = value
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du CSV: {e}")
        return translations
    
    return translations

def get_translation(key, translations, default=''):
    """Récupère une traduction depuis le dictionnaire."""
    return translations.get(key, default)

def update_favicon_absolute(html, translations):
    """Met à jour la favicon avec une URL absolue pour que Google la trouve."""
    domain = get_translation('site.domain', translations, 'https://rvtravelshop.com')
    domain = domain.rstrip('/') if domain else 'https://rvtravelshop.com'
    favicon_url = f"{domain}/images/favicon/favicon.ico"
    
    # Supprimer toutes les anciennes balises favicon
    html = re.sub(
        r'<link rel="(icon|shortcut icon|apple-touch-icon)"[^>]*>',
        '',
        html,
        flags=re.IGNORECASE
    )
    
    # Ajouter toutes les balises favicon nécessaires pour Google (comme PrestaShop)
    favicon_tags = f'''<link rel="icon" type="image/vnd.microsoft.icon" href="{escape_html_attr(favicon_url)}">
<link rel="shortcut icon" type="image/x-icon" href="{escape_html_attr(favicon_url)}">
<link rel="icon" type="image/x-icon" href="{escape_html_attr(favicon_url)}">
<link rel="apple-touch-icon" href="{escape_html_attr(favicon_url)}">'''
    
    # Insérer après <title> ou après <head>
    if re.search(r'</title>', html):
        html = re.sub(
            r'(</title>)',
            r'\1\n' + favicon_tags,
            html,
            count=1
        )
    elif re.search(r'<head[^>]*>', html):
        html = re.sub(
            r'(<head[^>]*>)',
            r'\1\n' + favicon_tags,
            html,
            count=1
        )
    
    return html

def escape_html_attr(text):
    """Échappe les caractères spéciaux pour les attributs HTML."""
    if not text:
        return ""
    return escape(text).replace('"', '&quot;')

def escape_html_content(text):
    """Échappe les caractères spéciaux pour le contenu HTML (mais préserve le HTML existant)."""
    if not text:
        return ""
    # Ne pas échapper si c'est déjà du HTML valide
    # On laisse le HTML tel quel, mais on échappe les caractères dangereux dans les attributs
    return text

def get_menu_items_from_csv(translations, page_type='product'):
    """
    Lit le CSV et retourne la liste des éléments du menu.
    page_type: 'product' (depuis page_html/products/)
    """
    menu_items = []
    
    # Home (depuis footer.link.home)
    home_text = get_translation('footer.link.home', translations, 'Home')
    menu_items.append({'text': home_text, 'url': '../../'})
    
    # Toutes les catégories (menu.*) - utiliser des numéros (1, 2, 3...)
    menu_keys = [k for k in translations.keys() if k.startswith('menu.') and k != 'home.en']
    menu_keys_sorted = sorted(menu_keys)
    
    for index, menu_key in enumerate(menu_keys_sorted, start=1):
        menu_name = translations.get(menu_key, '')
        if not menu_name:
            continue
        
        # Utiliser le numéro comme slug (1, 2, 3, etc.)
        category_number = str(index)
        
        # Depuis page_html/products/, les catégories sont dans ../categories/
        menu_items.append({'text': menu_name, 'url': f"../categories/{category_number}.html"})
    
    return menu_items

def get_footer_items_from_csv(translations, page_type='product'):
    """
    Lit le CSV et retourne la liste des éléments du footer.
    Home est TOUJOURS en premier.
    page_type: 'product' (depuis page_html/products/)
    """
    footer_items = []
    
    # 1. Home EN PREMIER
    home_key = None
    sitemap_key = None
    legal_keys = []
    
    footer_keys = [k for k in translations.keys() if k.startswith('footer.link.')]
    for footer_key in footer_keys:
        if 'home' in footer_key:
            home_key = footer_key
        elif 'sitemap' in footer_key:
            sitemap_key = footer_key
        else:
            legal_keys.append(footer_key)
    
    # Ajouter Home en premier
    if home_key:
        home_text = translations.get(home_key, '')
        if home_text:
            footer_items.append({'text': home_text, 'url': '../../'})
    
    # 2. Sitemap en deuxième
    if sitemap_key:
        sitemap_text = translations.get(sitemap_key, '')
        if sitemap_text:
            footer_items.append({'text': sitemap_text, 'url': '../../sitemap.xml'})
    
    # 3. Pages légales ensuite (triées)
    for footer_key in sorted(legal_keys):
        text = translations.get(footer_key, '')
        if not text:
            continue
        
        legal_slug = footer_key.replace('footer.link.', '')
        footer_items.append({'text': text, 'url': f"../legal/{legal_slug}.html"})
    
    return footer_items

def generate_menu_html(menu_items):
    """Génère le HTML du menu depuis la liste des items."""
    menu_html = []
    for item in menu_items:
        menu_text = item["text"].upper()  # Menu en majuscule
        menu_html.append(f'<li><a href="{item["url"]}">{escape_html_attr(menu_text)}</a></li>')
    return '\n'.join(menu_html)

def generate_footer_html(footer_items, translations):
    """Génère le HTML du footer depuis la liste des items."""
    footer_links_html = []
    for item in footer_items:
        footer_links_html.append(f'<a href="{item["url"]}">{escape_html_attr(item["text"])}</a>')
    
    contact_text = get_translation('footer.contact', translations, 'Contact us:')
    copyright_text = get_translation('footer.copyright', translations, '© 2024 AliExpress Affiliate. All rights reserved.')
    contact_email = get_translation('site.contact.email', translations, 'contact@naturehike-shop.com')
    
    footer_html = f'''<div class="footer-links">
{chr(10).join(footer_links_html)}
</div>
<p>{escape_html_attr(contact_text)} <a href="mailto:{escape_html_attr(contact_email)}">{escape_html_attr(contact_email)}</a></p>
<p>{escape_html_attr(copyright_text)}</p>'''
    
    return footer_html

def extract_images_from_csv(image_paths_str, product_id):
    """Extrait les 3 premières images depuis le CSV et les convertit en chemins relatifs.
    Vérifie que les fichiers existent réellement avant de les ajouter."""
    if not image_paths_str:
        return []
    
    # Nettoyer le product_id (enlever l'apostrophe si présente)
    clean_product_id = str(product_id).strip().lstrip("'")
    
    # Déterminer le chemin de base pour vérifier l'existence des fichiers
    # Si BASE_DIR est un dossier de langue (ex: fr/), remonter à la racine
    root_dir = BASE_DIR
    if len(BASE_DIR.name) == 2 and BASE_DIR.name.isalpha():
        root_dir = BASE_DIR.parent
    
    images_dir = root_dir / 'images' / 'products' / clean_product_id
    
    images = image_paths_str.split('|')
    result = []
    
    for i, img_path in enumerate(images):
        if i >= 3:  # Limiter aux 3 premières images
            break
        img_path = img_path.strip()
        if not img_path:
            continue
        
        # Extraire le nom du fichier (image_1.jpg, image_2.jpg, etc.)
        filename = Path(img_path).name
        
        # Vérifier que le fichier existe réellement
        image_file = images_dir / filename
        if not image_file.exists():
            # Essayer avec différentes extensions
            found = False
            for ext in ['.webp', '.jpg', '.jpeg', '.png']:
                alt_file = images_dir / f"{Path(filename).stem}{ext}"
                if alt_file.exists():
                    filename = alt_file.name
                    found = True
                    break
            if not found:
                continue  # Passer cette image si elle n'existe pas
        
        # Chemin relatif depuis page_html/products/ vers images/products/
        # Les images sont dans le dossier parent, donc ../../../images/
        relative_path = f"../../../images/products/{clean_product_id}/{filename}"
        result.append(relative_path)
    
    return result if result else [f"../../../images/products/{clean_product_id}/image_1.jpg"]

def get_reviews_count(product_id):
    """Génère le nombre d'avis (même système que pages catégorie)."""
    if not product_id:
        return random.randint(15, 150)
    
    try:
        # Nettoyer le product_id et extraire les 6 derniers chiffres
        clean_id = str(product_id).strip().lstrip("'").replace('.', '').replace('E+', '').replace('e+', '')
        if clean_id and len(clean_id) >= 6:
            last_6 = int(clean_id[-6:])
        else:
            last_6 = None
    except (ValueError, AttributeError):
        last_6 = None
    random.seed(last_6)
    reviews_count = random.randint(15, 150)
    random.seed()  # Réinitialiser le seed
    return reviews_count

def generate_product_page_html(product, translations):
    """Génère le HTML complet d'une page produit."""
    
    # Charger le template
    if not TEMPLATE_PRODUCT.exists():
        print(f"❌ Template non trouvé: {TEMPLATE_PRODUCT}")
        return None
    
    with open(TEMPLATE_PRODUCT, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Récupérer les données du produit
    product_id = product.get('id', '')
    # Utiliser 'name' en priorité, puis 'title', puis 'titre' comme fallback
    name = product.get('name', '') or product.get('title', '') or product.get('titre', '') or 'Product'
    title = name  # Utiliser 'name' comme titre principal
    description_short = product.get('description_short', '')
    description_long = product.get('description') or product.get('description_long', '')
    affiliate_link = product.get('affiliate_link') or product.get('affiliate_links', '')
    price = product.get('price', '')
    meta_title = product.get('meta_title', '') or title
    meta_description = product.get('meta_description', '') or description_short or 'Discover this AliExpress product'
    
    # Extraire les images
    image_paths_str = product.get('image_paths', '')
    images = extract_images_from_csv(image_paths_str, product_id)
    # Nettoyer le product_id (enlever l'apostrophe si présente)
    clean_product_id = str(product_id).strip().lstrip("'")
    main_image = images[0] if images else f"../../../images/products/{clean_product_id}/image_1.jpg"
    
    # Récupérer l'URL YouTube si elle existe
    youtube_url = product.get('youtube_url', '').strip() if product.get('youtube_url') else ''
    has_youtube = bool(youtube_url)
    
    # Extraire l'ID YouTube depuis l'URL
    youtube_id = ''
    if has_youtube:
        match = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\s]+)', youtube_url)
        if match:
            youtube_id = match.group(1)
    
    # Nombre d'avis (même système que pages catégorie)
    reviews_count = get_reviews_count(product_id)
    
    # Menu et footer
    menu_items = get_menu_items_from_csv(translations, page_type='product')
    footer_items = get_footer_items_from_csv(translations, page_type='product')
    menu_html = generate_menu_html(menu_items)
    footer_html = generate_footer_html(footer_items, translations)
    
    # 1. Mettre à jour le lang
    lang_code = detect_language_code()
    html = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang_code}"', html)
    html = re.sub(r"<html lang='[^']*'", f'<html lang="{lang_code}"', html)
    
    # 2. Mettre à jour les meta tags
    html = re.sub(r'<title>.*?</title>', f'<title>{escape_html_attr(meta_title)}</title>', html)
    html = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{escape_html_attr(meta_description)}">', html)
    
    # 2.5. Générer les hreflang et canonical corrects pour la page produit
    domain = get_translation('site.domain', translations, 'https://esport4all.com')
    if domain:
        domain = domain.rstrip('/')
    
    # Construire l'URL de cette page produit
    product_filename = f'produit-{clean_product_id}.html'
    if lang_code == 'en':
        canonical_url = f'{domain}/page_html/products/{product_filename}'
    else:
        canonical_url = f'{domain}/{lang_code}/page_html/products/{product_filename}'
    
    # Générer les hreflang pour toutes les langues disponibles
    # Détecter les langues disponibles depuis la racine du projet
    # Si BASE_DIR est un dossier de langue (ex: fr/), remonter à la racine
    root_dir = BASE_DIR
    if len(BASE_DIR.name) == 2 and BASE_DIR.name.isalpha():
        # On est dans un dossier de langue, remonter à la racine
        root_dir = BASE_DIR.parent
    
    available_languages = []
    if (root_dir / 'index.html').exists():
        available_languages.append(('en', ''))
    
    for item in root_dir.iterdir():
        if (item.is_dir() and not item.name.startswith('.') and 
            item.name not in ['APPLI:SCRIPT aliexpress', 'scripts', 'config', 'images', 'page_html', 
                              'upload_cloudflare', 'sauv', 'CSV', '__pycache__', '.git', 'node_modules', 'upload youtube', 'dist'] and
            (item / 'index.html').exists()):
            lang = item.name.lower()
            available_languages.append((lang, f'/{lang}'))
    
    # Générer les hreflang
    hreflang_links = []
    for lang, path in available_languages:
        if lang == 'en':
            hreflang_url = f'{domain}/page_html/products/{product_filename}'
        else:
            hreflang_url = f'{domain}/{lang}/page_html/products/{product_filename}'
        hreflang_links.append(f'<link rel="alternate" hreflang="{lang}" href="{hreflang_url}" />')
    
    # Ajouter x-default (vers la langue principale)
    hreflang_links.append(f'<link rel="alternate" hreflang="x-default" href="{domain}/page_html/products/{product_filename}" />')
    
    hreflang_html = '\n'.join(hreflang_links)
    canonical_tag = f'<link rel="canonical" href="{canonical_url}" />'
    
    # Supprimer TOUS les canonical et hreflang existants
    html = re.sub(
        r'<link rel="canonical"[^>]*/>\s*',
        '',
        html
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\s*',
        '',
        html
    )
    
    # Ajouter le canonical et les hreflang ensemble (canonical en premier)
    hreflang_section = canonical_tag + '\n' + hreflang_html + '\n'
    
    # Trouver où insérer (après le meta description, avant le style)
    if re.search(r'<meta name="description"', html):
        html = re.sub(
            r'(<meta name="description"[^>]*>)',
            r'\1\n' + hreflang_section,
            html
        )
    elif re.search(r'</title>', html):
        html = re.sub(
            r'(</title>)',
            r'\1\n' + hreflang_section,
            html
        )
    
    # 3. Modifier le CSS des thumbnails pour limiter à 3 colonnes maximum
    # Remplacer repeat(4,1fr) par repeat(3,1fr) pour éviter les espaces vides
    html = re.sub(
        r'grid-template-columns:repeat\(4,1fr\)',
        'grid-template-columns:repeat(3,1fr)',
        html
    )
    
    # 4. Mettre à jour la favicon avec URL absolue
    html = update_favicon_absolute(html, translations)
    
    # 5. Mettre à jour le logo (chemin relatif)
    # Le template peut avoir un logo vide ou avec href
    html = re.sub(
        r'<a[^>]*class="logo"[^>]*>.*?</a>',
        f'<a href="../../" class="logo" id="logo"><img src="../../../images/logo/logo.webp" alt="Logo"></a>',
        html,
        flags=re.DOTALL
    )
    
    # 6. Remplacer le menu
    html = re.sub(
        r'<ul class="menu"[^>]*>.*?</ul>',
        f'<ul class="menu" id="menu">\n{menu_html}\n</ul>',
        html,
        flags=re.DOTALL
    )
    
    # 7. Générer le contenu du produit (remplacer le div product-container)
    product_content = f'''<div class="product-header">
<div class="product-images">
<img src="{main_image}" alt="{escape_html_attr(title)}" class="main-image" id="main-image">
'''
    
    # Ajouter la vidéo YouTube si elle existe
    if has_youtube and youtube_id:
        product_content += f'<iframe id="main-video" class="main-video" style="display:none;width:100%;aspect-ratio:1;border:none;border-radius:8px;" src="https://www.youtube.com/embed/{youtube_id}" allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture" allowfullscreen></iframe>\n'
    
    # Ajouter les miniatures si plusieurs images ou vidéo YouTube
    # Comportement identique au site parent : afficher les miniatures si plus d'1 image OU si vidéo YouTube
    if len(images) > 1 or has_youtube:
        product_content += '<div class="thumbnails">\n'
        # Ajouter toutes les images disponibles
        for idx, img in enumerate(images):
            active_class = 'active' if idx == 0 else ''
            product_content += f'<img src="{img}" alt="Image {idx+1}" class="thumbnail {active_class}" onclick="showImage(\'{img}\',event)">\n'
        # Ajouter la vidéo YouTube si elle existe (après les images)
        if has_youtube:
            product_content += f'<div class="thumbnail-video" onclick="showVideo(event)"><img src="{main_image}" alt="Vidéo"></div>\n'
        product_content += '</div>\n'
    
    product_content += '</div>\n'
    product_content += '<div class="product-info">\n'
    product_content += f'<h1>{escape_html_attr(title)}</h1>\n'
    
    if price:
        product_content += f'<div class="product-price">{escape_html_attr(price)}</div>\n'
    
    if description_short:
        # Nettoyer le HTML de description_short (supprimer les h1, h2, etc.)
        desc_clean = description_short
        # Supprimer les balises h1-h6
        desc_clean = re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>', '', desc_clean, flags=re.DOTALL)
        product_content += f'<div class="description-short">{desc_clean}</div>\n'
    
    # Avis (étoiles + nombre)
    product_content += f'''<div class="product-rating" style="margin:1rem 0;display:flex;align-items:center;gap:0.5rem;">
<span class="product-stars" style="color:#ffc107;font-size:1.2rem;">★★★★★</span>
<span class="product-reviews" style="color:#666;font-size:0.9rem;">({reviews_count})</span>
</div>
'''
    
    if affiliate_link:
        button_text = get_translation('button.view_on_aliexpress', translations, 'View on AliExpress')
        product_content += f'<a href="{escape_html_attr(affiliate_link)}" class="cta-button" target="_blank" rel="noopener noreferrer">{escape_html_attr(button_text)}</a>\n'
    
    product_content += '</div>\n'
    product_content += '</div>\n'
    
    # Description longue
    if description_long:
        # Supprimer les h1, h2, etc. de la description longue
        desc_long_clean = description_long
        desc_long_clean = re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>', '', desc_long_clean, flags=re.DOTALL)
        if desc_long_clean.strip():
            product_content += f'<div class="description-long">{desc_long_clean}</div>\n'
    
    # Remplacer le contenu product-container (remplacer seulement le contenu intérieur)
    html = re.sub(
        r'<div id="product-container"[^>]*>.*?</div>',
        product_content,
        html,
        flags=re.DOTALL
    )
    
    # 6.5. Ajouter le markup schema.org VideoObject si vidéo YouTube présente
    if has_youtube and youtube_id:
        domain = get_translation('site.domain', translations, 'https://esport4all.com')
        domain = domain.rstrip('/') if domain else 'https://esport4all.com'
        
        # Construire l'URL complète de la page produit
        lang_prefix = f'/{lang_code}/' if lang_code != 'en' else '/'
        page_url = f"{domain}{lang_prefix}page_html/products/produit-{clean_product_id}.html"
        
        # URL de la vidéo YouTube
        embed_url = f"https://www.youtube.com/embed/{youtube_id}"
        watch_url = f"https://www.youtube.com/watch?v={youtube_id}"
        
        # URL de la miniature (première image du produit, convertie en URL absolue)
        thumbnail_url = main_image
        if thumbnail_url.startswith('../../../'):
            # Convertir le chemin relatif en URL absolue
            thumbnail_url = f"{domain}{thumbnail_url.replace('../../../', '/')}"
        elif thumbnail_url.startswith('../'):
            # Convertir le chemin relatif en URL absolue
            thumbnail_url = f"{domain}{thumbnail_url.replace('../', '/')}"
        elif not thumbnail_url.startswith('http'):
            # Si c'est un chemin relatif simple
            thumbnail_url = f"{domain}/{thumbnail_url.lstrip('/')}"
        
        # Description pour la vidéo (utiliser description_short ou title)
        video_description = description_short if description_short else title
        # Nettoyer le HTML de la description
        video_description = re.sub(r'<[^>]+>', '', video_description)  # Supprimer les balises HTML
        video_description = video_description.strip()[:200]  # Limiter à 200 caractères
        
        # Date d'upload (utiliser la date actuelle)
        upload_date = datetime.now().strftime('%Y-%m-%d')
        
        # Créer le JSON-LD VideoObject
        video_schema = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": escape_html_attr(title),
            "description": escape_html_attr(video_description),
            "thumbnailUrl": thumbnail_url,
            "uploadDate": upload_date,
            "contentUrl": watch_url,
            "embedUrl": embed_url,
            "duration": "PT1M",  # Durée par défaut (1 minute), peut être ajustée si disponible
            "publisher": {
                "@type": "Organization",
                "name": "RV Travel Shop",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{domain}/images/logo/logo.webp"
                }
            }
        }
        
        # Convertir en JSON
        video_schema_json = json.dumps(video_schema, indent=2, ensure_ascii=False)
        
        # Insérer le schema dans le <head>
        schema_script = f'<script type="application/ld+json">\n{video_schema_json}\n</script>'
        
        # Insérer juste avant </head>
        if re.search(r'</head>', html):
            html = re.sub(
                r'(</head>)',
                schema_script + '\n\\1',
                html,
                count=1
            )
        else:
            # Si pas de </head>, insérer avant </body>
            html = re.sub(
                r'(</body>)',
                schema_script + '\n\\1',
                html,
                count=1
            )
    
    # 7. Remplacer le footer
    html = re.sub(
        r'<footer>.*?</footer>',
        f'<footer>\n{footer_html}\n</footer>',
        html,
        flags=re.DOTALL
    )
    
    # 8. Ajouter le JavaScript minimal pour les images (showImage) et vidéos (showVideo)
    js_code = '''<script>
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const menu = document.getElementById('menu');
    if (menuToggle && menu) {
        menuToggle.addEventListener('click', function() {
            menu.classList.toggle('active');
        });
    }
    
    window.showImage = function(imgSrc, evt) {
        const mainImg = document.getElementById('main-image');
        const mainVid = document.getElementById('main-video');
        if (mainImg) {
            mainImg.src = imgSrc;
            mainImg.style.display = 'block';
        }
        if (mainVid) {
            mainVid.style.display = 'none';
        }
        document.querySelectorAll('.thumbnail,.thumbnail-video').forEach(t => t.classList.remove('active'));
        if (evt && evt.target) {
            evt.target.closest('.thumbnail,.thumbnail-video')?.classList.add('active');
        }
    };
    
    window.showVideo = function(evt) {
        const mainImg = document.getElementById('main-image');
        const mainVid = document.getElementById('main-video');
        if (mainImg) {
            mainImg.style.display = 'none';
        }
        if (mainVid) {
            mainVid.style.display = 'block';
        }
        document.querySelectorAll('.thumbnail,.thumbnail-video').forEach(t => t.classList.remove('active'));
        if (evt && evt.target) {
            evt.target.closest('.thumbnail-video')?.classList.add('active');
        }
    };
});
</script>'''
    
    # Remplacer tout le script existant par le nouveau
    html = re.sub(
        r'<script>.*?</script>',
        js_code,
        html,
        flags=re.DOTALL
    )
    
    return html

def load_products_from_csv():
    """Charge tous les produits depuis all_products.csv (avec colonnes traduites si disponibles)."""
    products = []
    
    if not PRODUCTS_CSV.exists():
        print(f"⚠️  Fichier produits non trouvé: {PRODUCTS_CSV}")
        return products
    
    # Détecter la langue du dossier
    lang_code = detect_language_code()
    
    try:
        with open(PRODUCTS_CSV, 'r', encoding='utf-8') as f:
            # Détecter automatiquement le séparateur (virgule ou point-virgule)
            first_line = f.readline()
            f.seek(0)
            delimiter = ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','
            reader = csv.DictReader(f, delimiter=delimiter)
            fieldnames = reader.fieldnames
            
            # Chercher les colonnes traduites : {col}_{lang_code}_auto en priorité, puis {col}
            def get_translated_col(base_col):
                """Retourne la colonne traduite si disponible."""
                auto_col = f'{base_col}_{lang_code}_auto'
                if auto_col in fieldnames:
                    return auto_col
                elif base_col in fieldnames:
                    return base_col
                return None
            
            name_col = get_translated_col('name') or get_translated_col('titre')
            description_col = get_translated_col('description')
            description_short_col = get_translated_col('description_short')
            meta_title_col = get_translated_col('meta_title')
            meta_description_col = get_translated_col('meta_description')
            
            for row in reader:
                product_id = row.get('product_id', '').strip()
                if not product_id:
                    continue
                
                # Ne garder que les produits avec un lien d'affiliation
                affiliate_link = row.get('affiliate_links', '').strip()
                if not affiliate_link:
                    continue
                
                # Utiliser les colonnes traduites si disponibles
                titre = row.get('titre', '').strip() if 'titre' in fieldnames else ''
                name = row.get(name_col, '').strip() if name_col else ''
                title = name or titre or row.get('name', '').strip() or row.get('titre', '').strip()
                
                # Récupérer youtube_url
                youtube_url = row.get('youtube_url', '').strip() if 'youtube_url' in fieldnames else ''
                
                products.append({
                    'id': product_id,
                    'title': title,
                    'youtube_url': youtube_url,
                    'name': name or row.get('name', '').strip(),
                    'affiliate_link': affiliate_link,
                    'affiliate_links': affiliate_link,
                    'image_paths': row.get('image_paths', '').strip(),
                    'description': row.get(description_col, '').strip() if description_col else row.get('description', '').strip(),
                    'description_short': row.get(description_short_col, '').strip() if description_short_col else row.get('description_short', '').strip(),
                    'meta_title': row.get(meta_title_col, '').strip() if meta_title_col else row.get('meta_title', '').strip(),
                    'meta_description': row.get(meta_description_col, '').strip() if meta_description_col else row.get('meta_description', '').strip(),
                    'price': row.get('price', '').strip() if 'price' in fieldnames else '',
                })
    except Exception as e:
        print(f"⚠️  Erreur lors de la lecture des produits: {e}")
        import traceback
        traceback.print_exc()
        return products
    
    return products

def main():
    """Fonction principale."""
    print("=" * 70)
    print("📦 GÉNÉRATION DE TOUTES LES PAGES PRODUIT (HTML STATIQUE)")
    print("=" * 70)
    
    # 1. Charger les traductions
    print("\n📖 Chargement des traductions depuis translations.csv...")
    translations = load_translations_from_csv()
    if not translations:
        print("❌ Aucune traduction trouvée")
        return False
    
    print(f"✅ {len(translations)} clés chargées")
    
    # 2. Charger les produits
    print("\n📦 Chargement des produits depuis all_products.csv...")
    products = load_products_from_csv()
    if not products:
        print("❌ Aucun produit trouvé")
        return False
    
    print(f"✅ {len(products)} produits chargés")
    
    # 3. Créer le dossier products si nécessaire
    PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 4. Générer chaque page produit
    print("\n🔄 Génération des pages produit...")
    print("-" * 70)
    
    success_count = 0
    error_count = 0
    
    for product in products:
        product_id = product.get('id', '')
        if not product_id:
            continue
        
        # Nettoyer le product_id (enlever l'apostrophe si présente) pour le nom de fichier
        clean_product_id = str(product_id).strip().lstrip("'")
        
        try:
            html = generate_product_page_html(product, translations)
            if html:
                output_file = PRODUCTS_DIR / f"produit-{clean_product_id}.html"
                output_file.write_text(html, encoding='utf-8')
                success_count += 1
                if success_count % 10 == 0:
                    print(f"  ✅ {success_count} pages générées...")
            else:
                error_count += 1
                print(f"  ❌ Erreur pour produit {product_id}")
        except Exception as e:
            error_count += 1
            print(f"  ❌ Erreur pour produit {product_id}: {e}")
    
    print("-" * 70)
    print(f"\n✅ {success_count} pages générées avec succès")
    if error_count > 0:
        print(f"⚠️  {error_count} erreurs")
    
    print(f"\n📁 Pages générées dans: {PRODUCTS_DIR}")
    
    # 5. Supprimer les pages orphelines (produits qui ne sont plus dans le CSV)
    print("\n🧹 Nettoyage des pages orphelines...")
    print("-" * 70)
    
    # Récupérer tous les product_id du CSV
    valid_product_ids = {str(p.get('id', '')).strip().lstrip("'") for p in products if p.get('id')}
    
    # Parcourir toutes les pages produits existantes
    orphaned_pages = []
    if PRODUCTS_DIR.exists():
        for page_file in PRODUCTS_DIR.glob('produit-*.html'):
            # Extraire le product_id du nom de fichier
            # Format: produit-{product_id}.html
            try:
                page_product_id = page_file.stem.replace('produit-', '').strip()
                # Nettoyer le product_id (enlever apostrophe si présente)
                clean_page_id = page_product_id.lstrip("'")
                
                if clean_page_id not in valid_product_ids:
                    orphaned_pages.append(page_file)
            except Exception as e:
                print(f"  ⚠️  Erreur lors de l'analyse de {page_file.name}: {e}")
    
    # Supprimer les pages orphelines
    if orphaned_pages:
        print(f"  📋 {len(orphaned_pages)} page(s) orpheline(s) trouvée(s)")
        for page_file in orphaned_pages:
            try:
                page_file.unlink()
                print(f"  🗑️  Supprimé: {page_file.name}")
            except Exception as e:
                print(f"  ⚠️  Erreur lors de la suppression de {page_file.name}: {e}")
        print(f"  ✅ {len(orphaned_pages)} page(s) orpheline(s) supprimée(s)")
    else:
        print("  ✅ Aucune page orpheline trouvée")
    
    print("\n💡 Pour régénérer toutes les pages après modification des produits,")
    print("   relancez simplement ce script.")
    
    return True

if __name__ == '__main__':
    main()

