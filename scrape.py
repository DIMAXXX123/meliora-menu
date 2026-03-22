from playwright.sync_api import sync_playwright
import json, time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://meliora-restaurant.com', wait_until='networkidle')
    time.sleep(5)
    # Scroll to bottom to load all images
    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(3)
    # Get all images
    images = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('img')).map(img => ({
            src: img.src,
            alt: img.alt || '',
            width: img.naturalWidth,
            height: img.naturalHeight,
            className: img.className || '',
            parentText: img.parentElement ? img.parentElement.textContent.trim().substring(0, 100) : ''
        })).filter(i => i.width > 50)
    }''')
    print(json.dumps(images, indent=2))
    browser.close()
