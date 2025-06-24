# script to run server locally
from client_server.server_udp import Server

server = Server("localhost", 49158)
server.run_server()