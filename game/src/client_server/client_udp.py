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
        self.disconnect = False
        self.is_connected = False
        self.server_addr = None
        self.socket = None

    def network_thread(self, player):
        while not self.disconnect:
            if not self.is_connected:
                print("not connected")
                time.sleep(0.05)
                self.connect_to_server()
                if not self.is_connected:
                    continue
            try:
                send_pickle_udp(self.socket, player.data, self.server_addr)
                player.data.clientID, _ = recv_pickle_udp(self.socket)
                self.currentPlayerNumber, _ = recv_pickle_udp(self.socket)
                all_players, _ = recv_pickle_udp(self.socket)
                with self.lock:
                    if isinstance(all_players, dict):
                        self.all_players = all_players
                    else:
                        print("corrupt data all_players:", all_players)
                # time.sleep(0.01)
            except Exception as e:
                print("UDP client error:", e)
                self.is_connected = False
                self.socket.close()
            # time.sleep(0.05)

    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(2)
            self.server_addr = (self.host, self.port)
            self.is_connected = True
        except Exception as e:
            self.is_connected = False
            self.socket = None
