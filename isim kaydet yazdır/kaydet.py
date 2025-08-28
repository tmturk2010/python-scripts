import json
import os

# dosya adı
filename = "greeting.json"

# dosya varsa oku yoksa oluştur
if os.path.exists(filename):
	with open(filename, "r", encoding="utf-8") as file:
		try:
			greetings = json.load(file)
		except json.JSONDecodeError:
			greetings = []
else:
	greetings = []

# input al
name = input("Adınızı girin: ")
surname = input("Soyadınızı girin: ")
age = input("Yaşınızı girin: ")

# inputu json yap
greeting = {
	"name": name,
	"surname": surname,
	"age": age
}

# inputu dosyaya kaydet
greetings.append(greeting)
with open(filename, "w", encoding="utf-8") as file:
	json.dump(greetings, file, ensure_ascii=False, indent=2)

# inputu okunabilir şekilde ekrana yazdır
greetingprintable = f"Benim adım {name} {surname} ve ben {age} yaşındayım."
print(greetingprintable)