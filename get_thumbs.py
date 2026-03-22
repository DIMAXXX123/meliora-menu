from playwright.sync_api import sync_playwright
import json, time, re

# Search for each dish category on Pexels - extract photo IDs from thumbnails
searches = [
    ("ramen", "ramen noodle soup"),
    ("miso_soup", "miso soup japanese"),
    ("edamame", "edamame soybeans"),
    ("tuna_tartare", "tuna tartare"),
    ("tempura", "tempura shrimp"),
    ("tataki", "raw tuna sliced"),
    ("bao_buns", "steamed buns asian"),
    ("gyoza", "dumplings fried"),
    ("bruschetta", "bruschetta toast"),
    ("spring_roll", "spring roll rice paper"),
    ("fried_chicken", "fried chicken crispy"),
    ("green_curry", "green curry thai"),
    ("beef_skewers", "beef skewers yakitori"),
    ("gnocchi", "gnocchi potato"),
    ("katsu", "chicken cutlet breaded"),
    ("sushi_roll", "sushi roll"),
    ("nigiri", "nigiri salmon sushi"),
    ("maki", "sushi maki roll"),
    ("udon", "udon stir fry noodles"),
    ("yakisoba", "noodles stir fry"),
    ("glass_noodles", "glass noodles vermicelli"),
    ("poke_bowl", "poke bowl hawaiian"),
    ("avocado_salad", "avocado salad bowl"),
    ("poached_eggs", "poached eggs benedict"),
    ("shakshuka", "shakshuka eggs"),
    ("oatmeal", "oatmeal porridge fruit"),
    ("croissant", "croissant bakery"),
    ("pancakes", "pancakes chocolate stack"),
    ("brownie", "chocolate brownie dessert"),
    ("fried_rice", "fried rice wok"),
    ("pork_belly", "pork belly glazed"),
    ("panko", "schnitzel breaded"),
    ("tortilla_wrap", "breakfast burrito wrap"),
    ("bbq_steak", "grilled steak plated"),
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    
    for key, query in searches:
        try:
            page.goto(f"https://www.pexels.com/search/{query.replace(' ', '%20')}/", 
                      wait_until='domcontentloaded', timeout=20000)
            time.sleep(1.5)
            
            # Get ALL photo IDs from img src tags (thumbnails load immediately)
            ids = page.evaluate('''() => {
                const ids = [];
                document.querySelectorAll('img[src*="images.pexels.com/photos/"]').forEach(img => {
                    const m = img.src.match(/photos\\/(\\d+)/);
                    if (m && !ids.includes(m[1])) ids.push(m[1]);
                });
                return ids;
            }''')
            
            if ids and len(ids) > 0:
                # First ID is usually a related-search thumb, skip to 2nd if available
                pid = ids[1] if len(ids) > 1 else ids[0]
                results[key] = pid
                print(f"OK {key}: {pid} (found {len(ids)} ids)")
            else:
                print(f"MISS {key}")
        except Exception as e:
            print(f"ERR {key}: {str(e)[:60]}")
    
    browser.close()

# Build final URL mapping
final = {}
for k, pid in results.items():
    final[k] = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=200&h=200&fit=crop"

print("\n=== PHOTO IDS ===")
print(json.dumps(results, indent=2))
print("\n=== URLS ===")
print(json.dumps(final, indent=2))
