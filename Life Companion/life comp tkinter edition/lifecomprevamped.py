# importlar
import os
import time
import datetime
import calendar
import requests
import tkinter as tk
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from tkinter import *
from tkinter import ttk

# .env yükle
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# api keyler
weather_api_key = os.getenv("WEATHER_API_KEY")
currency_api_key = os.getenv("CURRENCY_API_KEY")

# isimler dosyasının yer belirteci
filename = os.path.join(os.path.dirname(__file__), "names.txt")

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

lifecompapp = App()
frm = ttk.Frame(lifecompapp, padding=10)
frm.grid()

lifecompapp.master.title("Life Companion")

def save_input():
    isim_var = isim_var.get()

isim_var = tk.StringVar()

# isimler dosyasını aç
try:
    with open(filename, "r") as f:
        isim_var = f.read().strip()
        if isim_var:
            hosgeldinmesaj = ttk.Label(frm, text=f"Hoş geldiniz, {isim_var}!")
            hosgeldinmesaj.grid(column=0, row=0, pady=(0, 10))
        else:
            raise FileNotFoundError


# dosya yoksa isim sorup dosya oluştur
except FileNotFoundError:
    isim_label = tk.Label(lifecompapp, text="Adınızı giriniz:")
    isim_label.grid(column=0, row=0)
    isim_kaydet = tk.Entry(lifecompapp, textvariable=isim_var)
    isim_kaydet.grid(column=0, row=0)
    kaydet_dugme = tk.Button(lifecompapp, text="Kaydet", command=save_input)
    kaydet_dugme.grid(column=0, row=1)
    with open(filename, "w") as f:
        f.write(isim_var)
    hosgeldinmesajyeni = ttk.Label(frm, text=f"Merhaba {isim_var}, isminiz sisteme kaydedildi!")
    hosgeldinmesajyeni.grid(column=0, row=0, pady=(0, 10))

cikisdugme = ttk.Button(frm, text="Çıkış", command=lifecompapp.quit)
cikisdugme.grid(column=1, row=0)

def takvim():
    today = datetime.date.today()
    takvimdisplay = ttk.Label(frm, text=calendar.month(today.year, today.month))
    takvimdisplay.grid(column=1, row=1)

def saattarih():
    now = datetime.datetime.now()
    saattarihdisplay = ttk.Label(frm, text=f"Tarih ve Saat: {now.strftime('%d/%m/%Y %H:%M')}")
    saattarihdisplay.grid(column=5, row=0)

def havadurumu():
    location = input("Hangi şehir için hava durumunu görmek istiyorsun?> ")
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}&aqi=yes"
    try:
        response = requests.get(url).json()
        hddisplay1 = ttk.Label(frm, text=f"\n{response['location']['name']}, {response['location']['country']}")
        hddisplay2 = ttk.Label(frm, text=f"Sıcaklık: {response['current']['temp_c']}°C")
        hddisplay3 = ttk.Label(frm, text=f"Hava: {response['current']['condition']['text']}")
        hddisplay4 = ttk.Label(frm, text=f"Hava Kalitesi (US-EPA): {response['current']['air_quality']['us-epa-index']}")

        hddisplay1.grid(column=7,row=0)
        hddisplay2.grid(column=7, row=1)
        hddisplay3.grid(column=7, row=2)
        hddisplay4.grid(column=7, row=3)

     # int yoksa diye fln hata mesajı
    except Exception as e:
        print("Hava durumu alınamadı:", e)

def doviz():
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

        dolardisplay = ttk.Label(frm, text=f"1 Dolar = {usd_try:.2f} ₺")
        eurodisplay = ttk.Label(frm, text=f"1 Euro  = {eur_try:.2f} ₺")
        bitcoindisplay = ttk.Label(frm, text=f"1 Bitcoin = {btc_usd:.2f} $")

        dolardisplay.grid(column=6, row=0)
        eurodisplay.grid(column=6, row=1)
        bitcoindisplay.grid(column=6, row=2)

    # int fln yoksa veri alamzsa hata veriyo işte
    except Exception as e:
        print("Döviz verileri alınamadı:", e)

def hesapsil():
    emin = input("Verilerinizi silmek istediğinize emin misiniz? Evet, Hayır>")
    if emin == "Evet":
        os.remove(filename)
        print("İşlem başarıyla tamamlandı")
    else:
         print("İşlem iptal edildi")

ttk.Button(frm, text="Takvim", command=takvim).grid(column=0, row=3)
ttk.Button(frm, text="Saat ve Tarih", command=saattarih).grid(column=1, row=3)
ttk.Button(frm, text="Hava Durumu", command=havadurumu).grid(column=2, row=3)
ttk.Button(frm, text="Döviz", command=doviz).grid(column=3, row=3)
ttk.Button(frm, text="Hesap Sil", command=hesapsil).grid(column=3, row=4)

lifecompapp.mainloop()