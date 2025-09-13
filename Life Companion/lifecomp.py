import os
import datetime
import calendar
import requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# .env yükle
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# API Keyler
weather_api_key = os.getenv("WEATHER_API_KEY")
nasa_api_key = os.getenv("NASA_API_KEY")
currency_api_key = os.getenv("CURRENCY_API_KEY")

filename = "names.txt"

try:
    with open(filename, "r") as f:
        name = f.read().strip()
        if name:
            print(f"Hoş geldiniz, {name}!\n")
        else:
            raise FileNotFoundError
except FileNotFoundError:
    name = input("Adınızı girin:\n> ")
    with open(filename, "w") as f:
        f.write(name)
    print(f"\nMerhaba {name}, isminiz sisteme kaydedildi!\n")

menusec = input(
    "Lütfen yapmak istediğiniz işlemi seçiniz:\n"
    "1: Bu Ayın Takvimi\n"
    "2: Bugün Günlerden Ne?\n"
    "3: Hava Durumu Raporu\n"
    "4: Günün Uzay Fotoğrafı (NASA Tarafından) (SİLİNECEK!)\n"
    "5: Döviz\n"
    "Sil: Verilerimi sil\n>"
)

print()

# takvim
if menusec == "1":
    today = datetime.date.today()
    print(calendar.month(today.year, today.month))

# bugün
elif menusec == "2":
    now = datetime.datetime.now()
    print("Tarih ve Saat:", now.strftime("%d/%m/%Y %H:%M"))

# hava durumu
elif menusec == "3":
    location = input("Hangi şehir için hava durumunu görmek istiyorsun?\n> ")
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}&aqi=yes"
    try:
        response = requests.get(url).json()
        print(f"\n{response['location']['name']}, {response['location']['country']}")
        print(f"Sıcaklık: {response['current']['temp_c']}°C")
        print(f"Hava: {response['current']['condition']['text']}")
        print(f"Hava Kalitesi (US-EPA): {response['current']['air_quality']['us-epa-index']}")
    except Exception as e:
        print("Hava durumu alınamadı:", e)

# NASA uzay fotoğrafı (SİLİNECEK!)
elif menusec == "4":
    date = input("Hangi günün uzay fotoğrafını görmek istersiniz? (YYYY-AA-GG, boşsa bugün)\n> ")
    if not date:
        date = datetime.date.today().isoformat()
    apod_url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&date={date}"
    try:
        apod = requests.get(apod_url).json()
        print(f"\nTarih: {apod['date']}")
        print(f"Başlık: {apod['title']}")
        print(f"Açıklama: {apod['explanation']}\n")
        print(f"Medya Türü: {apod['media_type']}")
        if apod['media_type'] == 'image':
            response = requests.get(apod['url'])
            img = Image.open(BytesIO(response.content))
            img.show()
        elif apod['media_type'] == 'video':
            print(f"Video URL: {apod['url']}")
            if 'thumbnail_url' in apod:
                thumb_response = requests.get(apod['thumbnail_url'])
                img = Image.open(BytesIO(thumb_response.content))
                img.show()
    except Exception as e:
        print("APOD verisi alınamadı (Günün ilk saatleri yeni veriler gelmediğinden dolayı bir önceki günün tarihini yazınız):", e)

# döviz
elif menusec == "5":
    try:
        # USD -> TRY
        url_usd = f"https://api.currencyapi.com/v3/latest?apikey={currency_api_key}&base_currency=USD"
        usd_data = requests.get(url_usd).json()
        usd_try = usd_data['data']['TRY']['value']

        # EUR -> TRY
        url_eur = f"https://api.currencyapi.com/v3/latest?apikey={currency_api_key}&base_currency=EUR"
        eur_data = requests.get(url_eur).json()
        eur_try = eur_data['data']['TRY']['value']
        
        # BTC -> USD
        url_btc = f"https://api.currencyapi.com/v3/latest?apikey={currency_api_key}&base_currency=BTC"
        btc_data = requests.get(url_btc).json()
        btc_usd = btc_data['data']['USD']['value']

        print(f"1 Dolar = {usd_try:.2f} ₺")
        print(f"1 Euro  = {eur_try:.2f} ₺")
        print(f"1 Bitcoin = {btc_usd:.2f} $")

    except Exception as e:
        print("Döviz verileri alınamadı:", e)
        
# hesap sil
elif menusec == "Sil":
    emin = input("Verilerinizi silmek istediğinize emin misiniz?\nEvet\nHayır\n>")
    if emin == "Evet":
        os.remove(filename)
        print("İşlem başarıyla tamamlandı")
    else:
        print("İşlem iptal edildi")

else:
    print("Hatalı tuşlama yaptınız")