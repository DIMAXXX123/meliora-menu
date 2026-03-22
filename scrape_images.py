from playwright.sync_api import sync_playwright
import json, time, re

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://meliora-restaurant.com', wait_until='networkidle')
    time.sleep(5)
    
    # Scroll through entire page
    for i in range(20):
        page.evaluate(f'window.scrollTo(0, {i * 800})')
        time.sleep(0.3)
    time.sleep(3)
    
    # Get ALL images
    images = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('img')).map(img => ({
            src: img.src || img.dataset.src || '',
            alt: img.alt || '',
            w: img.naturalWidth,
            h: img.naturalHeight
        })).filter(i => i.src.length > 10)
    }''')
    
    print('=== IMAGES ===')
    for img in images:
        print(json.dumps(img))
    print(f'Total: {len(images)}')
    
    # Get full HTML and find image URLs
    html = page.content()
    urls = re.findall(r'https?://[^\s\"\'>]+\.(?:jpg|jpeg|png|webp|avif)', html)
    unique_urls = sorted(set(urls))
    print('\n=== IMAGE URLs IN HTML ===')
    for u in unique_urls:
        print(u)
    print(f'Total unique: {len(unique_urls)}')
    
    # Check for lazy loaded / data attributes
    lazy = page.evaluate('''() => {
        const els = document.querySelectorAll('[data-src], [data-bg], [loading="lazy"]');
        return Array.from(els).map(el => ({
            tag: el.tagName,
            dataSrc: el.dataset.src || '',
            src: el.src || '',
            alt: el.alt || ''
        }))
    }''')
    print('\n=== LAZY LOADED ===')
    for l in lazy:
        print(json.dumps(l))
    
    # Check network requests for image files
    # Try clicking on menu items to trigger image loads
    page.evaluate('window.scrollTo(0, 0)')
    time.sleep(1)
    
    browser.close()
