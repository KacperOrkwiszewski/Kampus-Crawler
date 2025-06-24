import pickle

def send_pickle_udp(sock, obj, addr):
    data = pickle.dumps(obj)
    sock.sendto(data, addr)

def recv_pickle_udp(sock, bufsize=4096):
    data, addr = sock.recvfrom(bufsize)
    obj = pickle.loads(data)
    return obj, addr