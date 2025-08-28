import random

# 1 ila 6 arası bir sayı seç ve dice değişkenine kaydet
numbers = [1, 2, 3, 4, 5, 6]
dice = str(random.choice(numbers))

# rastgele sayıyı kaydet
print("Zardan çıkan sayı " + dice)