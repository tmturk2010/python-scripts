# deneme
import os
from dotenv import load_dotenv

# Bu dosyanın (main.py) bulunduğu klasördeki .env dosyasını oku
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Test için
print("Weather API Key:", os.getenv("WEATHER_API_KEY"))