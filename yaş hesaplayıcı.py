from datetime import date

birth = int(input("Doğum yılınız ne? "))
yearnow = int(date.today().year)
userage = int(yearnow - birth)
useragemessage = ("Siz " + str(userage) + " yaşındasınız.")
print(useragemessage)