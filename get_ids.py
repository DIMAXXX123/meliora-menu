from playwright.sync_api import sync_playwright
import json, time, re

searches = {
    "ramen": "ramen bowl",
    "miso_soup": "miso soup",
    "edamame": "edamame",
    "tuna_tartare": "tuna tartare",
    "tempura": "shrimp tempura",
    "tataki": "tuna sashimi",
    "bao_buns": "bao buns",
    "gyoza": "gyoza",
    "bruschetta": "bruschetta",
    "spring_roll": "spring rolls",
    "fried_chicken": "fried chicken crispy",
    "green_curry": "green curry",
    "beef_skewers": "beef skewers",
    "gnocchi": "gnocchi",
    "katsu": "katsu",
    "sushi_roll": "sushi rolls",
    "nigiri": "nigiri sushi",
    "maki": "maki sushi",
    "udon": "udon noodles",
    "yakisoba": "stir fry noodles",
    "glass_noodles": "glass noodles",
    "poke_bowl": "poke bowl",
    "avocado_salad": "avocado salad",
    "poached_eggs": "poached eggs",
    "shakshuka": "shakshuka",
    "oatmeal": "oatmeal bowl",
    "croissant": "croissant",
    "pancakes": "pancakes chocolate",
    "brownie": "brownie chocolate",
    "fried_rice": "fried rice",
    "pork_belly": "pork belly",
    "panko": "breaded chicken fried",
    "tortilla_wrap": "breakfast wrap",
    "bbq_turkey": "grilled steak"
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
                      wait_until='networkidle', timeout=25000)
            time.sleep(2)
            
            # Extract ALL pexels photo IDs from page
            ids = page.evaluate('''() => {
                const ids = new Set();
                // From img src
                document.querySelectorAll('img').forEach(img => {
                    const src = img.src || '';
                    const m = src.match(/photos\\/(\\d+)/);
                    if (m) ids.add(m[1]);
                });
                // From links
                document.querySelectorAll('a[href*="/photo/"]').forEach(a => {
                    const m = a.href.match(/photo\\/[^/]+-?(\\d+)/);
                    if (m) ids.add(m[1]);
                });
                // From srcset
                document.querySelectorAll('img[srcset]').forEach(img => {
                    const matches = [...img.srcset.matchAll(/photos\\/(\\d+)/g)];
                    matches.forEach(m => ids.add(m[1]));
                });
                return [...ids];
            }''')
            
            if ids:
                # Pick first non-tiny ID
                pid = ids[0]
                results[key] = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop"
                print(f"OK {key}: {pid}")
            else:
                print(f"MISS {key}")
        except Exception as e:
            print(f"ERR {key}: {str(e)[:80]}")
    
    browser.close()

print("\n=== RESULTS ===")
print(json.dumps(results, indent=2))
