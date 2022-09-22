import socket


def transmit_data(data: bytes, host: str, port: int):
    with socket.socket() as s:
        s.connect((host, port))
        s.sendall(data)
