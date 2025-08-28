# kullanıcıdan ilk sayı alınır ve n1 değişkenine kaydedilir
n1 = int(input("Lütfen ilk numarayı girin: "))
# kullanıcıdan ikinci sayı alınır ve n2 değişkenine kaydedilir
n2 = int(input("Lütfen ikinci numarayı girin: "))
# kullanıcıdan 4 işlemden birini seçmesi istenir ve op değişkenine kaydedilir
op = str(input("Lütfen yapacağınız işlemi yazınız (+, -, *, /): "))
# eğer kullanıcı + seçtiyse
if op == ("+"):
# n1 ve n2 değişkeni toplanıp ekrana yazdırılır
     print(n1 + n2)
# eğer kullanıcı - seçtiyse
elif op == ("-"):
# n1, n2 değikeninden çıkarılıp ekrana yazdırılır
    print(n1 - n2)
# eğer kullanıcı * seçtiyse
elif op == ("*"):
# n1 ile n2 değişkeni çarpılıp ekrana yazdırılır
    print(n1 * n2)
# eğer kullanıcı / seçtiyse
elif op == ("/"):
# n1 değişkeni n2 değişkenine bölünüp ekrana yazdırılır
    print(n1 / n2)
# eğer kullanıcı 4 işlem dışında başka bir şey yazarsa uyarı mesajı yazdırılır
else:
    print("Hatalı tuşlama yaptınız")