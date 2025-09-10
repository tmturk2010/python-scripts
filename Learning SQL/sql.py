import sqlite3
import os

# veritabanı dosyası
DB_PATH = os.path.join(os.path.dirname(__file__), 'deneme.db')

# veritabanına bağlan
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# tabloyu oluştur
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notlar (
                     username TEXT,
                     dbyaz TEXT
                 )''')
    conn.commit()
    conn.close()

init_db()

# kullanıcıdan işlem seçimi
islem = input(
    "Lütfen yapmak istediğiniz işlemi seçiniz:\n"
    "1: Veritabanına yaz\n"
    "2: Veritabanından al\n"
)

if islem == "1":
    username = input("Lütfen Kullanıcı adınızı yazınız: ")
    dbyaz = input("Yazmak istediğiniz mesajı yazınız: ")
    
    # veriyi yaz
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO notlar (username, dbyaz) VALUES (?, ?)", (username, dbyaz))
    conn.commit()
    conn.close()
    print("Mesaj başarıyla kaydedildi!")

elif islem == "2":
    username = input("Lütfen kullanıcı adınızı yazınız: ")
    
    # veriyi al
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT dbyaz FROM notlar WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    
    if row:
        print("Mesajınız:", row["dbyaz"])
    else:
        print("Kullanıcı bulunamadı.")

else:
    print("Geçersiz işlem seçtiniz.")