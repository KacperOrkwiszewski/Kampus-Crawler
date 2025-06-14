import pickle


# pickles object and sends to socket
def send_pickle(conn, obj):
    data = pickle.dumps(obj)
    length = len(data)
    conn.sendall(length.to_bytes(4, byteorder='big'))  # send pickle size
    conn.sendall(data)  # send pickle


# gets pickled object from socket, un-pickles it and returns it
def recv_pickle(conn):
    length_data = conn.recv(4)  # get pickle size
    if not length_data:
        return None
    length = int.from_bytes(length_data, byteorder='big')
    data = b''
    # receive pickle
    while len(data) < length:
        more = conn.recv(length - len(data))
        if not more:
            return None
        data += more
    obj = pickle.loads(data)  # un-pickle the pickle
    return obj
