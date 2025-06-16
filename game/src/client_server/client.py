import socket
import threading
from client_server.common import recv_pickle, send_pickle
import time


class Client:
    def __init__(self, hostname, port_number):
        self.currentPlayerNumber = 0
        self.all_players = {}
        self.player_objects = {}
        self.lock = threading.Lock()
        self.host = hostname
        self.port = port_number
        self.is_connected = False

    def network_thread(self, player):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.settimeout(0.1)
        self.is_connected = True
        while True:
            try:
                # Send player data
                send_pickle(s, player.data)
                try:
                    self.currentPlayerNumber = recv_pickle(s)
                    with self.lock:
                        self.all_players = recv_pickle(s)
                    # wait a bit so the cpu isn't working at full capacity | higher value may cause lag
                    time.sleep(0.005)
                except socket.timeout:
                    pass

            except Exception as e:
                self.is_connected = False
                print("Network error:", e)
                break
