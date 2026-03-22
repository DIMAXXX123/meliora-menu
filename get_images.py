from playwright.sync_api import sync_playwright
import json, time

searches = {
    "ramen": "ramen bowl noodle soup",
    "miso_soup": "miso soup japanese",
    "edamame": "edamame beans",
    "tuna_tartare": "tuna tartare raw fish",
    "tempura_shrimp": "tempura shrimp crispy",
    "tataki": "tuna tataki seared",
    "bao_buns": "bao buns steamed",
    "gyoza": "gyoza dumplings fried",
    "bruschetta": "bruschetta burrata tomato",
    "spring_roll": "spring roll duck",
    "fried_chicken": "korean fried chicken",
    "green_curry": "green curry thai",
    "beef_skewers": "beef skewers teriyaki",
    "gnocchi": "gnocchi pasta cream",
    "katsu": "chicken katsu curry",
    "sushi_roll": "sushi roll dragon",
    "california_roll": "california roll sushi",
    "philadelphia_roll": "philadelphia roll salmon sushi",
    "nigiri": "nigiri salmon sushi",
    "maki": "maki roll sushi",
    "udon_noodles": "udon noodles stir fry",
    "yakisoba": "yakisoba noodles",
    "funchoza": "glass noodles asian",
    "poke_bowl": "poke bowl tuna salmon",
    "avocado_salad": "avocado salad green",
    "poached_eggs": "poached eggs toast breakfast",
    "shakshuka": "shakshuka eggs tomato",
    "oatmeal": "oatmeal fruits bowl",
    "croissant": "croissant fresh baked",
    "pancakes": "chocolate pancakes nutella",
    "brownie": "chocolate brownie dessert",
    "tortilla_wrap": "tortilla omelette wrap breakfast",
    "fried_rice": "seafood fried rice asian",
    "bbq_steak": "grilled turkey steak bbq",
    "asian_pork": "braised pork asian",
    "panko": "panko chicken breaded"
}

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    for key, query in searches.items():
        try:
            url = f"https://unsplash.com/s/photos/{query.replace(' ', '-')}"
            page.goto(url, wait_until='domcontentloaded', timeout=15000)
            time.sleep(2)
            
            # Get first image src
            imgs = page.evaluate('''() => {
                const imgs = document.querySelectorAll('img[srcset], img[data-src]');
                for (const img of imgs) {
                    const src = img.src || img.getAttribute('data-src') || '';
                    if (src.includes('images.unsplash.com/photo-')) {
                        return src.split('?')[0];
                    }
                }
                // Try all imgs
                for (const img of document.querySelectorAll('img')) {
                    const src = img.src || '';
                    if (src.includes('images.unsplash.com/photo-')) {
                        return src.split('?')[0];
                    }
                }
                return null;
            }''')
            
            if imgs:
                results[key] = imgs + "?w=200&h=200&fit=crop&q=80"
                print(f"OK {key}: {results[key][:80]}...")
            else:
                print(f"MISS {key}")
        except Exception as e:
            print(f"ERR {key}: {e}")
    
    browser.close()

print("\n\n=== RESULTS ===")
print(json.dumps(results, indent=2))
