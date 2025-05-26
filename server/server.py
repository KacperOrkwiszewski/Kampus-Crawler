import socket
import threading
import json

clients = {}
positions = {}
lock = threading.Lock()

def handle_client(conn, addr, player_id):
    global clients, positions
    buffer = ""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data.decode()
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue
                pos = json.loads(line)
                with lock:
                    positions[player_id] = pos
                    # Przygotuj dane do wysłania wszystkim klientom
                    all_positions = json.dumps(positions) + "\n"
                    for c in list(clients.values()):
                        try:
                            c.sendall(all_positions.encode())
                        except:
                            pass
    finally:
        with lock:
            if player_id in clients:
                del clients[player_id]
            if player_id in positions:
                del positions[player_id]
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
            clients[player_id] = conn
            positions[player_id] = {'x': 0, 'y': 0}
        threading.Thread(target=handle_client, args=(conn, addr, player_id), daemon=True).start()

if __name__ == '__main__':
    main()