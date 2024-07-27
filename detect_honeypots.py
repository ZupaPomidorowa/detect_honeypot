import argparse
import socket
import requests
import ssl
from sshconnectcowrie import  SSHConnectCowrie


def connect_to_socket(ip, port, message=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            if message:
                s.sendall(message)
            resp = s.recv(1024)
            return resp
    except socket.error as e:
        print(f'Socket error {e}')
        return None


def check_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((ip, port))
            return True
    except socket.timeout:
        return False
    except socket.error:
        return False


def check_open_ports(ip):
    ports = [2222, 21, 23, 42, 53, 80, 135, 443, 445, 1433, 1723, 1883, 3306, 5060, 9100, 11211, 27017, 2121, 5020,
             8800, 10201, 44818]
    open_ports = []

    print(f'Start scanning ports on {ip}')

    for port in ports:
        if check_port(ip, port):
            open_ports.append(port)

    print(f'Open ports: {open_ports}')
    return open_ports


def get_latest_version(honeypot):
    if honeypot == 'cowrie':
        url = f"https://api.github.com/repos/cowrie/cowrie/releases/latest"
    elif honeypot == 'kippo':
        url = f"https://api.github.com/repos/desaster/kippo/releases/latest"
    elif honeypot == 'dionaea':
        return 'v0.11.0'
    elif honeypot == 'conpot':
        url = f"https://api.github.com/repos/mushorg/conpot/releases/latest"

    response = requests.get(url)

    if response.status_code == 200:
        latest_release = response.json()
        return latest_release['tag_name']
    else:
        print("Failed to find the latest version.")
        return None


def port_2222(ip):
    print('Connecting to port 2222')
    resp = connect_to_socket(ip, 2222).decode().strip()
    banner_cowrie = 'SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2'
    banner_kippo = 'SSH-2.0-OpenSSH_5.1p1 Debian-5'
    if resp == banner_cowrie:
        print('[\033[92m+\033[00m] Found default Cowrie banner')
        return 'cowrie'
    elif resp == banner_kippo:
        print('[\033[92m+\033[00m] Found default Kippo banner')
        return 'kippo'
    else:
        print('[\033[91m-\033[00m] Didn\'t find default banner')
        return None

def port_21(ip):
    print('Connecting to port 21')
    resp = connect_to_socket(ip, 21).decode().strip()
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
    message = b'\x00\x00\x00\xa4\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x08\x01\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x06\x00\x00\x01\x00\x00\x81\x00\x02PC NETWORK PROGRAM 1.0\x00\x02MICROSOFT NETWORKS 1.03\x00\x02MICROSOFT NETWORKS 3.0\x00\x02LANMAN1.0\x00\x02LM1.2X002\x00\x02Samba\x00\x02NT LANMAN 1.0\x00\x02NT LM 0.12\x00'
    resp = connect_to_socket(ip, 445, message)
    default_banner = b'SMBr'
    if default_banner in resp:
        print('[\033[92m+\033[00m] Found dionaea smb server')
        return True
    else:
        print('[\033[91m-\033[00m] Didn\'t find dionaea smb server')
        return False


def check_cowrie(ip):
    ssh_conn = SSHConnectCowrie(ip=ip, port=2222, username="root", password="1234")
    ssh_conn.connect()
    ssh_conn.check_os_version()
    ssh_conn.check_meminfo()
    ssh_conn.check_mounts()
    ssh_conn.check_cpu()
    ssh_conn.check_group()
    ssh_conn.check_shadow()
    ssh_conn.check_passwd()
    ssh_conn.check_hostname()
    ssh_conn.close()

def check_dionaea(ip):
    res_21 = port_21(ip)
    res_443 = port_443(ip)
    res_445 = port_445(ip)
    return res_21 and res_443 and res_445


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str, action='store', help="IP address to connect")
    args = parser.parse_args()

    open_ports = check_open_ports(args.ip)

    port_cowrie_kippo = 2222
    dionaea_ports = [21, 23, 42, 53, 80, 135, 443, 445, 1433, 1723, 1883, 3306, 5060, 9100, 11211, 27017]
    conpot_ports = [2121, 5020, 10201, 44818]

    if port_cowrie_kippo in open_ports:
        resp = port_2222(args.ip)
        if resp == 'cowrie':
            check_cowrie(args.ip)
            print('This host is probably Cowrie honeypot')
            version = get_latest_version('cowrie')
            print(f'Cowrie version {version}')
        elif resp == 'kippo':
            print('This host is probably Kippo honeypot')
            version = get_latest_version('kippo')
            print(f'Kippo version {version}')
    elif set(dionaea_ports) <= set(open_ports):
        print('The same open ports as in Dionaea honeypot')
        if check_dionaea(args.ip):
            print('This host is probably Dionaea honeypot')
            version = get_latest_version('dionaea')
            print(f'Dionaea version {version}')
        else:
            print('This host might be Dionaea')
    elif set(conpot_ports) <= set(open_ports):
        print('Same open ports as in Conpot honeypot')
        print('This host is probably Conpot honeypot')
        version = get_latest_version('conpot')
        print(f'Conpot version {version}')
    else:
        print('Not supported honeypot detected')



if __name__ == "__main__":
    main()