import socket

print("[!] Finding an available server....")
def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    ip = sock.getsockname()
    sock.close()
    return ip

def detect_server():
    ip = get_ip()
    base_ip = ip[0].split('.')[0:3]
    server_ip = ""
    for i in range(100):
        test_ip = ".".join(base_ip) +f".{i}"

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.connect((test_ip, 5555))

            print(f"[+] Server found at {test_ip}")
            sock.send("PING".encode())
            server_ip = test_ip
            sock.close()

        except:
            continue

    if server_ip == "":
        return detect_server()
    
    else:
        return server_ip

    