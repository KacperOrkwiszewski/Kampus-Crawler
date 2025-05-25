import socket
import threading
import json

clients = {}
lock = threading.Lock()

def handle_client(conn, addr, player_id):
    global clients
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            pos = json.loads(data.decode())
            with lock:
                clients[player_id] = pos
                # Przygotuj dane do wysłania wszystkim klientom
                all_positions = json.dumps(clients).encode()
                for c in list(clients.keys()):
                    try:
                        clients[c]['conn'].sendall(all_positions)
                    except:
                        pass
    finally:
        with lock:
            del clients[player_id]
        conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 12345))
    s.listen()
    print('Server started')
    player_id = 0
    while True:
        conn, addr = s.accept()
        player_id += 1
        with lock:
            clients[player_id] = {'x': 0, 'y': 0, 'conn': conn}
        threading.Thread(target=handle_client, args=(conn, addr, player_id), daemon=True).start()

if __name__ == '__main__':
    main()