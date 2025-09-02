import json

# veriyi json'dan okunabilir şekilde alıp yazdır
with open("greeting.json", "r", encoding="utf-8") as file:
	greetings = json.load(file)
	for data in greetings:
		print(f"Benim adım {data['name']} {data['surname']}. Ben {data['age']} yaşındayım")