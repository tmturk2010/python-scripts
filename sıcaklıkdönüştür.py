# kullanıcıdan sıcaklık değerini al
temp = float(input("Lütfen dönüştürmek istdeğiniz sıcaklığı giriniz(Sıcaklık türünü yazmayınız, noktalı değerler kabul edilir): "))
# kullanıcıdan sıcaklık türünü al
temptype = str(input("Sıcaklık değeri Santigrat(C) mı Fahrenayt (F) mı? "))
# eğer Santigrat ise Fahrenayta dönüştür
if temptype == "C":
# dönüştürme işlemini yapıp F değişkenine kaydeder
    F = temp * 9/5 + 32
# F değişkenini yazdırır
    print("Sıcaklık değeri", F)
# eğer Fahrenayt ise Santigrata dönüştür
elif temptype == "F":
# dönüştürme işlemini yapıp C değişkenine kaydeder
    C = (temp - 32) * 5/9
# C değişkenin yazdırır
    print("Sıcaklık değeri", C)
# eğer sıcaklık türü kısmına F veya C yazılmadıysa uyarı mesajı gösterilir
else:
    print("Hatalı tuşlama yaptınız!")