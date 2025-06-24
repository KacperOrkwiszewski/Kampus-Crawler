import socket
import threading
from client_server.common_udp import recv_pickle_udp, send_pickle_udp
import time

class Client:
    def __init__(self, hostname, port_number):
        self.currentPlayerNumber = 0
        self.all_players = {}
        self.player_objects = {}
        self.lock = threading.Lock()
        self.host = hostname
        self.port = port_number
        self.is_connected = True

    def network_thread(self, player):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_addr = (self.host, self.port)
        while self.is_connected:
            try:
                send_pickle_udp(s, player.data, server_addr)
                self.currentPlayerNumber, _ = recv_pickle_udp(s)
                all_players, _ = recv_pickle_udp(s)
                with self.lock:
                    self.all_players = all_players
                time.sleep(0.005)
            except Exception as e:
                print("UDP client error:", e)
                self.is_connected = False
                break