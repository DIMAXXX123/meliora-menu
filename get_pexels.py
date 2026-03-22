from playwright.sync_api import sync_playwright
import json, time, re

searches = {
    "ramen": "ramen bowl",
    "miso_soup": "miso soup",
    "edamame": "edamame",
    "tuna_tartare": "tuna tartare",
    "tempura": "shrimp tempura",
    "tataki": "tuna sashimi sliced",
    "bao_buns": "bao buns",
    "gyoza": "gyoza dumplings",
    "bruschetta": "bruschetta tomato",
    "spring_roll": "spring rolls",
    "fried_chicken": "korean fried chicken",
    "green_curry": "green curry bowl",
    "beef_skewers": "beef skewers grilled",
    "gnocchi": "gnocchi cream",
    "katsu": "chicken katsu",
    "sushi_roll": "sushi roll plate",
    "nigiri": "nigiri salmon",
    "maki": "maki sushi",
    "udon": "udon noodles beef",
    "yakisoba": "yakisoba noodles",
    "glass_noodles": "glass noodles",
    "poke_bowl": "poke bowl",
    "avocado_salad": "avocado salad",
    "poached_eggs": "poached eggs toast",
    "shakshuka": "shakshuka",
    "oatmeal": "oatmeal fruits bowl",
    "croissant": "croissant",
    "pancakes": "chocolate pancakes",
    "brownie": "chocolate brownie",
    "fried_rice": "fried rice",
    "pork_belly": "pork belly braised",
    "panko": "breaded chicken",
    "tortilla_wrap": "breakfast wrap tortilla",
    "bbq_turkey": "grilled turkey"
}

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    
    for key, query in searches.items():
        try:
            page.goto(f"https://www.pexels.com/search/{query.replace(' ', '%20')}/", 
                      wait_until='domcontentloaded', timeout=20000)
            time.sleep(2)
            # scroll a bit to load lazy images
            page.evaluate('window.scrollBy(0, 300)')
            time.sleep(1)
            
            img_url = page.evaluate('''() => {
                // Look for gallery images - they have data-testid or are in article/a tags
                const allImgs = document.querySelectorAll('img');
                for (const img of allImgs) {
                    const src = img.src || '';
                    // Skip tiny thumbnails (40x40), get real photos
                    if (src.includes('images.pexels.com/photos/') && !src.includes('w=40')) {
                        return src;
                    }
                }
                // If no large found, try srcset
                for (const img of allImgs) {
                    const srcset = img.srcset || '';
                    const match = srcset.match(/https:\\/\\/images\\.pexels\\.com\\/photos\\/\\d+\\/[^ ]+/);
                    if (match) return match[0];
                }
                // Fallback: get IDs from the small thumbnails
                for (const img of allImgs) {
                    const src = img.src || '';
                    const match = src.match(/photos\\/(\\d+)\\/pexels-photo-\\1/);
                    if (match) {
                        return `https://images.pexels.com/photos/${match[1]}/pexels-photo-${match[1]}.jpeg`;
                    }
                }
                return null;
            }''')
            
            if img_url:
                # Extract base photo URL and add proper sizing
                m = re.search(r'(https://images\.pexels\.com/photos/\d+/pexels-photo-\d+\.jpeg)', img_url)
                if m:
                    results[key] = m.group(1) + "?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop"
                else:
                    results[key] = img_url.split('?')[0] + "?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop"
                print(f"OK {key}")
            else:
                # Use thumbnail ID as fallback
                thumb = page.evaluate('''() => {
                    for (const img of document.querySelectorAll('img')) {
                        const src = img.src || '';
                        const m = src.match(/photos\\/(\\d+)/);
                        if (m && src.includes('pexels')) return m[1];
                    }
                    return null;
                }''')
                if thumb:
                    results[key] = f"https://images.pexels.com/photos/{thumb}/pexels-photo-{thumb}.jpeg?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop"
                    print(f"OK(thumb) {key}")
                else:
                    print(f"MISS {key}")
        except Exception as e:
            print(f"ERR {key}: {str(e)[:80]}")
    
    browser.close()

print("\n=== RESULTS ===")
print(json.dumps(results, indent=2))
