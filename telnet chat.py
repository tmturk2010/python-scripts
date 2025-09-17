import socket
import threading

# Sunucu ayarları
HOST = "0.0.0.0"  # Her yerden bağlanılabilir
PORT = 2323       # Telnet portu (23 yerine 2323 kullanalım, rootsuz kullanmak için)

# Bağlantıyı yönetmek için fonksiyon
def handle_client(conn, addr):
    print(f"{addr} bağlandı!")
    conn.send(b"Telnet sunucusuna hosgeldiniz!\n")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            response = b"Gelen mesaj: " + data
            conn.send(response)
        except ConnectionResetError:
            break
    print(f"{addr} ayrıldı.")
    conn.close()

# Sunucu açma
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Sunucu {PORT} portunda dinliyor...")

while True:
    conn, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()