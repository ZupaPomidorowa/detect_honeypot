import socket
import ssl
from ssh_cowrie import SSHConnect

def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

def connect_to_socket(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f'Failed to create socket {e}')

    try:
        s.connect((ip, port))
        resp = s.recv(1024).decode().strip()
        s.close()
        return resp
    except socket.error as e:
        print(f'Failed to connect to socket')

def port_21(ip):
    print('Connecting to port 21')
    resp = connect_to_socket(ip, 21)
    default_banner = '220 DiskStation FTP server ready.'
    if resp == default_banner:
        print('[\033[92m+\033[00m] Found default FTP banner')
        return True
    else:
        print('[\033[91m-\033[00m] Didn\'t find default FTP banner')
        return False

def port_443(ip):
    print('Connecting to port 443')

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((ip, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=ip) as ssock:
            cert = ssock.getpeercert(True)
            cert = str(cert)
            if 'dionaea.carnivore.it1' in cert:
                print('[\033[92m+\033[00m] Found dionaea ssl-cert')
                return True
            else:
                print('[\033[91m-\033[00m] Didn\'t find default dionaea ssl-cert')
                return False

def port_445(ip):
    print('Connecting to port 445')
    port = 445
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f'Socket creation failed: {e}')
        return

    try:
        s.connect((ip, port))
        message = b'\x00\x00\x00\xa4\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x08\x01\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x06\x00\x00\x01\x00\x00\x81\x00\x02PC NETWORK PROGRAM 1.0\x00\x02MICROSOFT NETWORKS 1.03\x00\x02MICROSOFT NETWORKS 3.0\x00\x02LANMAN1.0\x00\x02LM1.2X002\x00\x02Samba\x00\x02NT LANMAN 1.0\x00\x02NT LM 0.12\x00'
        s.sendall(message)
        resp = s.recv(1024)
        s.close()
        if resp == resp:
            print('[\033[92m+\033[00m] Found dionaea smb server')
            return True
        else:
            print('[\033[91m-\033[00m] Didn\'t find dionaea smb server')
            return False
    except socket.error as e:
        print(f'Connection to port failed: {e}')


def port_2222(ip):
    print('Connecting to port 2222')
    resp = connect_to_socket(ip, 2222)
    banner_cowrie = 'SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2'
    banner_kippo = 'SSH-2.0-OpenSSH_5.1p1 Debian-5'
    if resp == banner_cowrie:
        print('[\033[92m+\033[00m] Found default Cowrie banner')
        return 'cowrie'
    elif resp == banner_kippo:
        print('[\033[92m+\033[00m] Found default Kippo banner')
        return 'cowrie'
    else:
        print('[\033[91m-\033[00m] Didn\'t find default banner')
        return resp


def check_dionaea(ip):
    res_21 = port_21(ip)
    res_443 = port_443(ip)
    res_445 = port_445(ip)
    return res_21 and res_443 and res_445

def check_cowrie(ip):
    ssh_conn = SSHConnect(ip=ip, port=2222, username="root", password="1234")
    ssh_conn.connect()
    ssh_conn.check_os_version()
    ssh_conn.check_meminfo()
    ssh_conn.check_mounts()
    ssh_conn.check_cpu()
    ssh_conn.check_group()
    ssh_conn.check_hostname()
    ssh_conn.close()



ip = '172.17.0.2'
port_list = [2222, 21, 23, 42, 53, 80, 135, 443, 445, 1433, 1723, 1883, 3306, 5060, 9100, 11211, 27017, 2121, 5020, 8800, 10201, 44818]
open_ports = []

for port in port_list:
    if check_port(ip, port):
        print(f"Port {port} on {ip} is open.")
        open_ports.append(port)
    else:
        print(f"Port {port} on {ip} is closed.")

print('Open ports')
print(open_ports)

conpot_ports = [2121, 5020, 10201, 44818]
dionaea_ports = [21, 23, 42, 53, 80, 135, 443, 445, 1433, 1723, 1883, 3306, 5060, 9100, 11211, 27017]
port_cowrie_kippo = [2222]

if port_cowrie_kippo == sorted(open_ports):
    resp = port_2222(ip)
    if resp == 'cowrie':
        check_cowrie(ip)
        print('This host is probably Cowrie')
    elif resp == 'kippo':
        print('This host is probably Dionaea')
    else:
        print('Not supported honeypot')
elif dionaea_ports == sorted(open_ports):
    print('Same open ports as in Dionaea')
    if check_dionaea(ip):
        print('This host is probably Dionaea')
    else:
        print('This host might be Dionaea')
elif conpot_ports == sorted(open_ports):
    print('Same open ports as in Conpot')
    print('This host is probably Conpot')
else:
    print('Not supported honeypot')