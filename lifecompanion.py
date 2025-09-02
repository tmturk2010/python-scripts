import datetime
import calendar

filename = "names.txt"

try:
    with open(filename, "r") as f:
        name = f.read().strip()
        if name:
            print(f"Hoş geldiniz, {name}!")
        else:
            raise FileNotFoundError
except FileNotFoundError:
    # Dosya yoksa veya boşsa kullanıcıdan isim al
    name = input("Adınızı girin: ")
    with open(filename, "w") as f:
        f.write(name)
    print(f"Merhaba {name}, seni kaydettim ✅")

# Takvim kısmı
today = datetime.date.today()
yy = today.year
mm = today.month
print(calendar.month(yy, mm))