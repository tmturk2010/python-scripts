import requests
import geocoder
import folium
import time
import sys
import csv

gp_api_key = "AIzaSyAj8FLsd4h0jO9aUzsNZKiyQo3YJHfb_ZI"  # <-- BURAYA Google Places API anahtarını koy

# Eğer IP tabanlı konum alınamazsa kullanıcıdan koordinat isteyecek.
def get_location():
    g = geocoder.ip('me')
    if g.ok and g.latlng:
        return g.latlng[0], g.latlng[1]
    print("IP tabanlı konum alınamadı veya başarısız. Lütfen 'lat,lon' formatında koordinat gir (ör: 41.0082,28.9784), ya da Enter basıp İstanbul merkezi kullan:")
    s = input("Koordinat (boş = İstanbul merkez): ").strip()
    if not s:
        return 41.0082, 28.9784
    try:
        lat, lon = map(float, s.split(','))
        return lat, lon
    except Exception:
        print("Geçersiz format, İstanbul merkezi kullanılacak.")
        return 41.0082, 28.9784

# Google Places Nearby Search ile pizzacıları ara. (keyword='pizza')
def search_places(lat, lon, radius=2000, keyword="pizza"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    results = []
    params = {
        'key': gp_api_key,
        'location': f"{lat},{lon}",
        'radius': radius,
        'keyword': keyword,
        'type': 'restaurant',
    }

    while True:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        j = resp.json()

        # Hata varsa kullanıcıya bildir
        if 'error_message' in j:
            raise RuntimeError("Google Places API hata: " + j.get('error_message', 'Unknown error'))

        for p in j.get('results', []):
            loc = p.get('geometry', {}).get('location', {})
            results.append({
                'name': p.get('name'),
                'address': p.get('vicinity'),
                'lat': loc.get('lat'),
                'lon': loc.get('lng'),
                'rating': p.get('rating'),
                'user_ratings_total': p.get('user_ratings_total'),
                'place_id': p.get('place_id'),
            })

        # Eğer daha fazla sayfa varsa, next_page_token ile getir
        next_token = j.get('next_page_token')
        if next_token:
            # next_page_token aktifleşmesi için kısa süre beklemek gerekebilir
            time.sleep(2)  # bazen 2-3 saniye gerekebilir
            params = {'key': gp_api_key, 'pagetoken': next_token}
            continue
        break

    return results

def save_csv(results, filename='pizzacilar.csv'):
    if not results:
        return
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name','address','lat','lon','rating','user_ratings_total','place_id'])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

def make_map(user_lat, user_lon, results, filename='pizzacilar.html'):
    m = folium.Map(location=[user_lat, user_lon], zoom_start=14)
    folium.Marker([user_lat, user_lon], popup='Senin konumun', icon=folium.Icon(color='red')).add_to(m)
    for p in results:
        popup_text = f"{p['name']}\n{p.get('address','')}\nRating: {p.get('rating','-')} ({p.get('user_ratings_total',0)})"
        folium.Marker([p['lat'], p['lon']], popup=popup_text).add_to(m)
    m.save(filename)

def main():
    if not gp_api_key or gp_api_key == "[Burayı ben doldurcam]":
        print("Lütfen dosyanın en üstündeki gp_api_key değişkenine Google Places API anahtarını koy ve tekrar çalıştır.")
        sys.exit(1)

    lat, lon = get_location()
    print(f"Arama konumu: {lat}, {lon}")

    try:
        results = search_places(lat, lon)
    except Exception as e:
        print("API isteği başarısız oldu:", e)
        sys.exit(1)

    if not results:
        print("Belirtilen yarıçap içinde pizzacı bulunamadı.")
        sys.exit(0)

    print(f"\nBulunan pizzacı sayısı: {len(results)}\n")
    for i, p in enumerate(results, 1):
        print(f"{i}. {p['name']} - {p.get('address','-')} (lat:{p['lat']}, lon:{p['lon']}) | Rating: {p.get('rating','-')} ({p.get('user_ratings_total',0)} yorum)")

    save_csv(results)
    make_map(lat, lon, results)
    print("\n'pizzacilar.csv' ve 'pizzacilar.html' oluşturuldu. 'pizzacilar.html' tarayıcıda açılarak harita görüntülenebilir.")

if __name__ == '__main__':
    main()