import socket
import pickle
import threading

currentPlayerNumber = 0
all_players = {}
lock = threading.Lock()

def network_thread(player):
    global all_players, currentPlayerNumber
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 1234))
    s.settimeout(0.1)
    while True:
        try:
            # Wysyłamy tylko pozycję i kierunek gracza
            send_pickle(s, player.data)
            
            try:
                currentPlayerNumber = recv_pickle(s)
                with lock:
                    all_players = recv_pickle(s)
            except socket.timeout:
                pass

        except Exception as e:
            print("Network error:", e)
            break

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