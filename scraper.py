import requests
import json

def fetch_data():
    # မင်းရဲ့ HTML မှာ သုံးထားတဲ့ Search Query တွေအတိုင်း သတ်မှတ်မယ်
    category_queries = {
        "All": "popular",
        "Game": "games",
        "Social": "social",
        "Tool": "tools"
    }

    final_json = {}
    headers = {"User-Agent": "Mozilla/5.0"}

    for cat_name, query in category_queries.items():
        print(f"Searching for {query}...")
        # HTML ထဲက link အတိုင်း search API ကို သုံးမယ်
        api_url = f"https://ws75.aptoide.com/api/7/apps/search?query={query}&limit=25"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=15)
            if response.status_code == 200:
                result = response.json()
                # Aptoide API structure: datalist -> list
                items = result.get("datalist", {}).get("list", [])
                
                apps_list = []
                for item in items:
                    # Icon ကို graphic ထဲမှာ အရင်ရှာမယ်
                    icon_url = item.get("graphic") or item.get("icon")
                    
                    apps_list.append({
                        "name": item.get("name"),
                        "package": item.get("package"),
                        "icon": icon_url,
                        "version": item.get("file", {}).get("vername", "N/A"),
                        "rating": item.get("stats", {}).get("rating", {}).get("avg", 0),
                        # Download link သို့မဟုတ် Store link
                        "link": f"https://{item.get('package')}.en.aptoide.com/app"
                    })
                
                final_json[cat_name] = apps_list
                print(f"Found {len(apps_list)} apps for {cat_name}")
            else:
                final_json[cat_name] = []
        except Exception as e:
            print(f"Error fetching {cat_name}: {e}")
            final_json[cat_name] = []

    # Final apps.json ရေးသားခြင်း
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_data()
