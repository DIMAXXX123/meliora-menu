from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    page.goto("https://www.pexels.com/search/ramen/", wait_until='networkidle', timeout=30000)
    time.sleep(3)
    
    # Get page content length and all img tags
    result = page.evaluate('''() => {
        const imgs = Array.from(document.querySelectorAll('img')).map(img => ({
            src: (img.src || '').substring(0, 120),
            alt: (img.alt || '').substring(0, 50),
            loading: img.loading || '',
            cls: (img.className || '').substring(0, 50)
        }));
        return {
            title: document.title,
            bodyLen: document.body.innerHTML.length,
            imgCount: imgs.length,
            imgs: imgs.slice(0, 15)
        };
    }''')
    print(f"Title: {result['title']}")
    print(f"Body length: {result['bodyLen']}")
    print(f"Image count: {result['imgCount']}")
    for img in result['imgs']:
        print(f"  src={img['src']}")
        print(f"  alt={img['alt']} cls={img['cls']}")
        print()
    
    browser.close()
