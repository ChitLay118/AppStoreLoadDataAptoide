import requests
import json

def fetch_aptoide_data():
    # Aptoide ရဲ့ တရားဝင် Category ID များ
    # 0 = All/Trending, 2 = Games, 15 = Social, 24 = Tools
    category_map = {
        "All": "https://ws75.aptoide.com/api/7/getApps?limit=20&sort=trending",
        "Game": "https://ws75.aptoide.com/api/7/getApps?limit=20&cat_id=2",
        "Social": "https://ws75.aptoide.com/api/7/getApps?limit=20&cat_id=15",
        "Tool": "https://ws75.aptoide.com/api/7/getApps?limit=20&cat_id=24"
    }

    final_json = {}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    for cat_name, url in category_map.items():
        print(f"Fetching {cat_name}...")
        try:
            response = requests.get(url, headers=headers)
            # Response status ကို စစ်ဆေးမယ်
            if response.status_code != 200:
                print(f"Error: Server returned status {response.status_code} for {cat_name}")
                final_json[cat_name] = []
                continue

            data = response.json()
            apps_list = []

            # Aptoide API structure အရ datalist -> list ထဲမှာ app တွေရှိပါတယ်
            items = data.get("datalist", {}).get("list", [])
            
            if not items:
                print(f"Warning: No apps found for {cat_name}")

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
            print(f"Successfully fetched {len(apps_list)} apps for {cat_name}")

        except Exception as e:
            print(f"Exception for {cat_name}: {e}")
            final_json[cat_name] = []

    # apps.json ထဲ သိမ်းမယ်
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
    
    print("Process Finished. Please check apps.json")

if __name__ == "__main__":
    fetch_aptoide_data()
