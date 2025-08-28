# bu yılı alması için import
from datetime import date

# kullanıcıya doğduğu yıl sorulur ve birth değişkenine kaydedilir
birth = int(input("Doğum yılınız ne? "))
# bu yıl datetime import'undan alınıp yearnow değişkenine kaydedilir
yearnow = int(date.today().year)
# şuanki yıldan kullanıcının doğduğu yıl çıkarılır ve userage değişkenine yazılır
userage = int(yearnow - birth)
# kullanıcının yaşının bulunduğu cümle usermessage değişkenine yazılır
useragemessage = ("Siz " + str(userage) + " yaşındasınız.")
# ekrana kullanıcının yaşının yazdığı cümleyi barındıran usermessage değişkeni yazdırılır
print(useragemessage)