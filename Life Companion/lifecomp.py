# importlar
import os
import time
import datetime
import calendar
import requests
from datetime import date
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# .env yükle
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# şuanki yılı year değişkenine kaydet
year = date.today().year

# api keyler
weather_api_key = os.getenv("WEATHER_API_KEY")
currency_api_key = os.getenv("CURRENCY_API_KEY")

# isimler dosyasının yer belirteci
filename = os.path.join(os.path.dirname(__file__), "names.txt")

# isimler dosyasını aç
try:
    with open(filename, "r") as f:
        name = f.read().strip()
        if name:
            print(f"Hoş geldiniz, {name}!\n")
        else:
            raise FileNotFoundError
# dosya yoksa isim sorup dosya oluştur
except FileNotFoundError:
    name = input("Adınızı girin:\n> ")
    byear = int(input("Doğum yılınızı giriniz:\n>"))
    with open(filename, "w") as f:
        f.write(name)
        f.write(str(byear))
    print(f"\nMerhaba {name}, isminiz ve yaşınız sisteme kaydedildi!\n")

# menü seçme ekranı işte ya mal mısın neyini anlamadın
while True:
    menusec = input(
        "Lütfen yapmak istediğiniz işlemi seçiniz:\n"
        "1: Bu Ayın Takvimi\n"
        "2: Bugün Günlerden Ne?\n"
        "3: Hava Durumu Raporu\n"
        "4: Döviz\n"
        "5: Reşit Miyim?\n"
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
        # int yoksa diye fln hata mesajı
        except Exception as e:
            print("Hava durumu alınamadı:", e)

    # döviz
    elif menusec == "4":
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
        # int fln yoksa veri alamzsa hata veriyo işte
        except Exception as e:
            print("Döviz verileri alınamadı:", e)

    elif menusec == "5":
        if year - byear >18:
            print("Reşitsiniz!")
        else:
            print("Reşit değilsiniz!")
            
    # hesap sileceği
    elif menusec == "Sil":
        emin = input("Verilerinizi silmek istediğinize emin misiniz?\nEvet\nHayır\n>")
        if emin == "Evet":
            os.remove(filename)
            print("İşlem başarıyla tamamlandı")
        else:
            print("İşlem iptal edildi")
    
    # önünde yazan numaraları yazamıyacak kadar salak olanlar için hata mesajı
    else:
        print("Hatalı tuşlama yaptınız")
    
    # devam?
    print()
    devam = input("Devam etmek istiyor musunuz? (Evet/Hayır)\n> ").strip().lower()
    if devam != "evet":
        print("Hoşça kalın!")
        time.sleep(2)  # hoşçakalın dedikten sonra 2sn bekletiyo
        break
    print()