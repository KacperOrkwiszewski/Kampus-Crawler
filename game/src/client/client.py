import socket
import json
import threading

other_players = {}
other_players_lock = threading.Lock()

def network_thread(player):
    global other_players
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12345))
    s.settimeout(0.1)
    buffer = ""
    while True:
        try:
            pos = json.dumps({'x': player.pos_x, 'y': player.pos_y}) + "\n"
            s.sendall(pos.encode())
            try:
                data = s.recv(4096)
                if data:
                    buffer += data.decode()
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if line.strip():
                            with other_players_lock:
                                other_players = json.loads(line)
            except socket.timeout:
                pass
        except Exception as e:
            print("Network error:", e)
            break