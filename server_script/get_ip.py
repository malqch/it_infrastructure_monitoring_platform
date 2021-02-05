import socket
import uuid
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
mac = ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

def get_host_ip():

    """
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    print(hostname)
    ip = get_host_ip()
    print(ip)
