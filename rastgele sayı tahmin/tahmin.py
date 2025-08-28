import random

# 1 ila 10 arası rastgele numara oluşturup randomnumber değişkenine kaydet
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
randomnumber = str(random.choice(numbers))

# kullanıcıdan bir sayı seçmesini söyle ve selectednumber değişkenine kaydet
selectednumber = input("1 ila 10 arası bir sayı seçin: ")

# iki sayıda aynı ise
if randomnumber == selectednumber:
    print("Doğru tahmin!")
    print("Doğru cevap " + str(randomnumber))

# iki sayı aynı değilse
else:
    print("Yanlış tahmin")
    print("Doğru cevap " + str(randomnumber))