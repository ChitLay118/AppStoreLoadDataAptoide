import requests
import json

def fetch_data():
    # Category အလိုက် ရှာဖွေမည့် Query များ
    category_queries = {
        "All": "popular",
        "Game": "games",
        "Social": "social",
        "Tool": "tools"
    }

    final_json = {}
    # Aptoide API ကို လှည့်စားရန် Browser User-Agent သုံးခြင်း
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    for cat_name, query in category_queries.items():
        # limit=50 သို့ ပြောင်းလဲလိုက်သည်
        print(f"Fetching 50 Direct Links for Category: {cat_name} (Query: {query})...")
        
        # Search API URL - limit ကို ၅၀ အထိ တိုးမြှင့်ထားသည်
        api_url = f"https://ws75.aptoide.com/api/7/apps/search?query={query}&limit=50"
        
        try:
            # Data ပမာဏ ပိုများလာသောကြောင့် timeout ကို ၃၀ စက္ကန့်အထိ တိုးထားသည်
            response = requests.get(api_url, headers=headers, timeout=30)
            if response.status_code == 200:
                result = response.json()
                # Aptoide v7 data structure အရ datalist -> list ထဲမှာ app တွေရှိပါတယ်
                items = result.get("datalist", {}).get("list", [])
                
                apps_list = []
                for item in items:
                    # အရေးကြီးဆုံးအပိုင်း: တိုက်ရိုက် APK link ကို file -> path ထဲကနေ ယူခြင်း
                    direct_apk_url = item.get("file", {}).get("path")
                    
                    # အကယ်၍ direct path မတွေ့ခဲ့ရင် website link ကို fallback အနေနဲ့ သုံးမယ်
                    if not direct_apk_url:
                        direct_apk_url = f"https://{item.get('package')}.en.aptoide.com/app"

                    apps_list.append({
                        "name": item.get("name"),
                        "package": item.get("package"),
                        "icon": item.get("graphic") or item.get("icon"),
                        "version": item.get("file", {}).get("vername", "N/A"),
                        "rating": item.get("stats", {}).get("rating", {}).get("avg", 0),
                        "downloadUrl": direct_apk_url, # Direct .apk download link
                        "description": f"Download {item.get('name')} latest version."
                    })
                
                final_json[cat_name] = apps_list
                print(f"Successfully fetched {len(apps_list)} apps for {cat_name}.")
            else:
                print(f"Failed to fetch {cat_name}. Status Code: {response.status_code}")
                final_json[cat_name] = []
                
        except Exception as e:
            print(f"Error fetching {cat_name}: {str(e)}")
            final_json[cat_name] = []

    # Final apps.json ဖိုင်ကို သိမ်းဆည်းခြင်း
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
    
    print("\n[DONE] apps.json updated with 50 apps per category (DIRECT APK links).")

if __name__ == "__main__":
    fetch_data()
