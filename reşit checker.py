# kullanıcının yaşı sorulup userage değişkenine kaydedilir
userage = int(input("Kaç yaşındasınız? "))
# eğer kullanıcını yaşı 17'den büyükse (17 dahil değil)
if userage > 17: 
# ekrana reşit olduğunu belirten mesaj yazdırılır
    print("Reşitsiniz!")
# eğer kullanıcının yaşı 17 veya daha küçükse
else:
# ekrana reşit olmadığını belirtem mesaj yazdırılır
    print("Reşit değilsiniz!")