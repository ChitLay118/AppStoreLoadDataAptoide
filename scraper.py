import requests
import json
import os

def fetch_aptoide_data():
    base_url = "https://ws75.aptoide.com/api/7/getApps"
    
    # UI မှာ ပြသမယ့် Category ၄ ခု သတ်မှတ်ခြင်း
    category_map = {
        "All": "https://ws75.aptoide.com/api/7/getApps?limit=20&sort=trending",
        "Game": "https://ws75.aptoide.com/api/7/getApps?limit=15&group_name=Games",
        "Social": "https://ws75.aptoide.com/api/7/getApps?limit=15&group_name=Social",
        "Tool": "https://ws75.aptoide.com/api/7/getApps?limit=15&group_name=Tools"
    }

    final_json = {}

    for cat_name, url in category_map.items():
        print(f"Fetching {cat_name} data...")
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            data = response.json()
            
            apps_list = []
            if "datalist" in data and "list" in data["datalist"]:
                for item in data["datalist"]["list"]:
                    apps_list.append({
                        "name": item.get("name"),
                        "package": item.get("package"),
                        "icon": item.get("graphic"),
                        "version": item.get("file", {}).get("vername"),
                        "rating": item.get("stats", {}).get("rating", {}).get("avg"),
                        "link": f"https://{item.get('package')}.en.aptoide.com/app"
                    })
            
            final_json[cat_name] = apps_list
        except Exception as e:
            print(f"Error fetching {cat_name}: {e}")

    # apps.json file ထဲ သိမ်းမယ်
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
    
    print("Update Complete: apps.json has been created.")

if __name__ == "__main__":
    fetch_aptoide_data()
