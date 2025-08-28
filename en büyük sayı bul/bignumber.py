# kullanıcıdan 2 sayı al ve number1 ve number2 değişkenine kaydet
number1 = input("Birinci sayıyı girin: ")
number2 = input("İkinci sayıyı girin: ")

# number1 daha mı büyük diye bak ve büyükse yazdır
if int(number1) > int(number2):
    print(number1 + " daha büyük")
# eğer number1 daha büyük değilse number2'yi yazdırıp onun daha büyük olduğunu söyle
else:
    print(number2 + " daha büyük")