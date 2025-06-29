import socket
import threading
from client_server.common_udp import recv_pickle_udp, send_pickle_udp
import time

class Server:
    def __init__(self, hostname, port_number):
        self.players = {}  # addr: player_data
        self.last_seen = {}  # addr: timestamp
        self.lock = threading.Lock()
        self.host = hostname
        self.port = port_number
        self.timeout = 2.0  # sekundy bez pakietu = usunięcie gracza

    def run_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))
        while True:
            try:
                # Receive data
                player, addr = recv_pickle_udp(s)
                now = time.time()
                with self.lock:
                    self.players[addr] = player
                    self.last_seen[addr] = now
                    # delete inactive clients
                    to_remove = [a for a, t in self.last_seen.items() if now - t > self.timeout]
                    for a in to_remove:
                        del self.players[a]
                        del self.last_seen[a]
                    all_players = self.players.copy()
                # Send id, then number of players them player datas
                send_pickle_udp(s, addr, addr)
                send_pickle_udp(s, len(all_players), addr)
                send_pickle_udp(s, all_players, addr)
            except Exception as e:
                print("UDP server error:", e)
            time.sleep(0.05)
