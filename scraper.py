import requests
import json

def fetch_data():
    # Aptoide API Links
    category_map = {
        "All": "https://ws75.aptoide.com/api/7/getApps?limit=25&sort=trending",
        "Game": "https://ws75.aptoide.com/api/7/getApps?limit=20&cat_id=2",
        "Social": "https://ws75.aptoide.com/api/7/getApps?limit=20&cat_id=15",
        "Tool": "https://ws75.aptoide.com/api/7/getApps?limit=20&cat_id=24"
    }

    final_json = {}
    headers = {"User-Agent": "Mozilla/5.0"}

    for cat_name, url in category_map.items():
        print(f"Fetching {cat_name}...")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                items = data.get("datalist", {}).get("list", [])
                
                apps_list = []
                for item in items:
                    apps_list.append({
                        "name": item.get("name"),
                        "package": item.get("package"),
                        "icon": item.get("graphic"),
                        "version": item.get("file", {}).get("vername", "N/A"),
                        "rating": item.get("stats", {}).get("rating", {}).get("avg", 0),
                        "link": f"https://{item.get('package')}.en.aptoide.com/app"
                    })
                final_json[cat_name] = apps_list
                print(f"Done {cat_name}: {len(apps_list)} apps.")
            else:
                final_json[cat_name] = []
        except Exception as e:
            print(f"Error {cat_name}: {e}")
            final_json[cat_name] = []

    # သိမ်းဆည်းခြင်း
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_data()
