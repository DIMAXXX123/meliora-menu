from playwright.sync_api import sync_playwright
import json, time

searches = {
    "ramen": "ramen",
    "miso_soup": "miso soup",
    "edamame": "edamame",
    "tuna_tartare": "tuna tartare",
    "tempura": "shrimp tempura",
    "tataki": "tuna sashimi",
    "bao_buns": "bao buns",
    "gyoza": "gyoza dumplings",
    "bruschetta": "bruschetta",
    "spring_roll": "spring roll",
    "fried_chicken": "korean fried chicken",
    "green_curry": "green curry",
    "beef_skewers": "beef skewers",
    "gnocchi": "gnocchi",
    "katsu": "chicken katsu",
    "sushi_roll": "sushi roll",
    "nigiri": "nigiri sushi",
    "maki": "maki sushi",
    "udon": "udon noodles",
    "yakisoba": "yakisoba",
    "glass_noodles": "glass noodles",
    "poke_bowl": "poke bowl",
    "avocado_salad": "avocado salad",
    "poached_eggs": "poached eggs",
    "shakshuka": "shakshuka",
    "oatmeal": "oatmeal fruits",
    "croissant": "croissant",
    "pancakes": "chocolate pancakes",
    "brownie": "chocolate brownie",
    "fried_rice": "fried rice seafood",
    "pork_belly": "braised pork belly",
    "panko": "panko chicken",
    "tortilla": "breakfast wrap"
}

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    for key, query in searches.items():
        try:
            search_url = f"https://www.pexels.com/search/{query.replace(' ', '%20')}/"
            page.goto(search_url, wait_until='domcontentloaded', timeout=20000)
            time.sleep(2)
            
            img_url = page.evaluate('''() => {
                // Pexels uses img tags with data-big-src or srcset
                const articles = document.querySelectorAll('article img, [data-testid] img, .photo-item__img, img.photo-item__img');
                for (const img of articles) {
                    const src = img.src || img.getAttribute('data-big-src') || '';
                    if (src && src.includes('pexels.com') && !src.includes('avatar') && !src.includes('logo')) {
                        return src;
                    }
                }
                // Try any img with pexels images
                for (const img of document.querySelectorAll('img')) {
                    const src = img.src || '';
                    if (src.includes('images.pexels.com/photos/') && !src.includes('avatar')) {
                        return src.split('?')[0] + '?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop';
                    }
                }
                return null;
            }''')
            
            if img_url:
                # Clean URL and add sizing
                base = img_url.split('?')[0]
                if 'images.pexels.com' in base:
                    results[key] = base + "?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop"
                else:
                    results[key] = img_url
                print(f"OK {key}: {results[key][:100]}...")
            else:
                print(f"MISS {key}")
        except Exception as e:
            print(f"ERR {key}: {str(e)[:80]}")
    
    browser.close()

print("\n=== RESULTS ===")
print(json.dumps(results, indent=2))
