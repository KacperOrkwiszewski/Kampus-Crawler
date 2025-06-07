import socket
import threading
import pickle

numberOfClients = 0
clients = {}
players = {}
lock = threading.Lock()


def handle_client(conn, addr, player_id):
    global clients, players, numberOfClients
    try:
        while True:
            print("number of clients: ", numberOfClients)
            # odbierz spicklowanego playera od klienta
            player = recv_pickle(conn)
            if player is None:
                print("Client disconnected")
                break
            print("got it, boss")
            with lock:
                players[player_id] = player
            # wyślij klientowi liczbę graczy
            with lock:
                send_pickle(conn, numberOfClients)
            # wyślij pozycje wszystkich graczy (możemy też wysłać listę playerów)
            with lock:
                send_pickle(conn, players)
    finally:
        with lock:
            if player_id in clients:
                del clients[player_id]
            if player_id in players:
                del players[player_id]
            numberOfClients -= 1
        conn.close()

def send_pickle(conn, obj):
    data = pickle.dumps(obj)
    length = len(data)
    conn.sendall(length.to_bytes(4, byteorder='big'))  # wysyłamy długość (4 bajty)
    conn.sendall(data)

def recv_pickle(conn):
    length_data = conn.recv(4)
    if not length_data:
        return None
    length = int.from_bytes(length_data, byteorder='big')
    data = b''
    while len(data) < length:
        more = conn.recv(length - len(data))
        if not more:
            return None
        data += more
    obj = pickle.loads(data)
    return obj

def main():
    global numberOfClients
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 1234))
    s.listen()
    print('Server started')
    player_id = 0
    while True:
        conn, addr = s.accept()
        print("connection established")
        numberOfClients += 1
        with lock:
            clients[player_id] = conn
        threading.Thread(target=handle_client, args=(conn, addr, player_id), daemon=True).start()
        player_id += 1

if __name__ == '__main__':
    main()