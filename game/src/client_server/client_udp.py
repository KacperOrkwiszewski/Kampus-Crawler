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
        self.is_connected = False

    def network_thread(self, player):
        while not self.is_connected:
            print("Attempting to connect to UDP server...")
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(2)
                server_addr = (self.host, self.port)
                self.is_connected = True
            except Exception as e:
                print("UDP connection error:", e)
                time.sleep(0.5)
            while self.is_connected:
                try:
                    send_pickle_udp(s, player.data, server_addr)
                    self.currentPlayerNumber, _ = recv_pickle_udp(s)
                    all_players, _ = recv_pickle_udp(s)
                    with self.lock:
                        if isinstance(all_players, dict):
                            self.all_players = all_players
                        else:
                            print("Odebrano nieprawidłowe dane all_players:", all_players)
                    time.sleep(0.005)
                except Exception as e:
                    print("UDP client error:", e)
                    self.is_connected = False
                    s.close()