import requests
import json

def fetch_data():
    # ပိုမိုသေချာသော API URL များ (v7 standard)
    category_map = {
        "All": "https://ws75.aptoide.com/api/7/getApps?limit=25&sort=trending",
        "Game": "https://ws75.aptoide.com/api/7/listAppsByCategory?limit=20&category_id=2",
        "Social": "https://ws75.aptoide.com/api/7/listAppsByCategory?limit=20&category_id=15",
        "Tool": "https://ws75.aptoide.com/api/7/listAppsByCategory?limit=20&category_id=24"
    }

    final_json = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
    }

    for cat_name, url in category_map.items():
        print(f"Fetching {cat_name} from {url}...")
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                data = response.json()
                
                # Aptoide v7 data extraction logic
                # 'datalist' ဒါမှမဟုတ် 'data' ထဲမှာ list ရှိမရှိ စစ်မယ်
                items = data.get("datalist", {}).get("list", [])
                
                # တကယ်လို့ datalist ထဲမှာ မရှိရင် data -> list ထဲမှာ ထပ်ရှာမယ်
                if not items:
                    items = data.get("data", {}).get("list", [])

                apps_list = []
                for item in items:
                    # Icon link ကို graphic ဒါမှမဟုတ် icon နေရာမှာ ရှာမယ်
                    icon_url = item.get("graphic") or item.get("icon")
                    
                    apps_list.append({
                        "name": item.get("name"),
                        "package": item.get("package"),
                        "icon": icon_url,
                        "version": item.get("file", {}).get("vername", "N/A"),
                        "rating": item.get("stats", {}).get("rating", {}).get("avg", 0),
                        "link": f"https://{item.get('package')}.en.aptoide.com/app"
                    })
                
                final_json[cat_name] = apps_list
                print(f"Done {cat_name}: Found {len(apps_list)} apps.")
            else:
                print(f"Failed {cat_name}: Status {response.status_code}")
                final_json[cat_name] = []
        except Exception as e:
            print(f"Error {cat_name}: {e}")
            final_json[cat_name] = []

    # Final Check: data တစ်ခုမှ မရခဲ့ရင် file ကို မရေးခင် သတိပေးမယ်
    if not any(final_json.values()):
        print("CRITICAL: No data fetched at all!")

    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fetch_data()
