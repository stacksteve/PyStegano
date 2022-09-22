import socket


def receive_data(port: int) -> bytes:
    if not port > 1023:
        raise KeyError("Port has to be > 1023")
    with socket.socket() as sock:
        host = "0.0.0.0"  # localhost -> the machine running this code
        sock.bind((host, port))
        sock.listen(1)
        print("[+] Waiting for connection")
        conn, address = sock.accept()
        print(f"[+] {address[0]} just connected")
        with conn:
            data = bytes()
            print("[+] Receiving data")
            while True:
                recv_data = conn.recv(1024)
                if not recv_data:
                    break
                data += recv_data
    return data
