import socket
import ssl


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


def port_21(ip):
    print('Connecting to port 21')
    resp = connect_to_socket(ip, 21).decode().strip()
    default_banner = '220 DiskStation FTP server ready.'
    if resp == default_banner:
        print('[\033[92m+\033[00m] Found default FTP banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find default FTP banner')


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
            else:
                print('[\033[91m-\033[00m] Didn\'t find default dionaea ssl-cert')


def port_445(ip):
    print('Connecting to port 445')
    message = b'\x00\x00\x00\xa4\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x08\x01\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x06\x00\x00\x01\x00\x00\x81\x00\x02PC NETWORK PROGRAM 1.0\x00\x02MICROSOFT NETWORKS 1.03\x00\x02MICROSOFT NETWORKS 3.0\x00\x02LANMAN1.0\x00\x02LM1.2X002\x00\x02Samba\x00\x02NT LANMAN 1.0\x00\x02NT LM 0.12\x00'
    resp = connect_to_socket(ip, 445, message)
    default_banner = b'SMBr'
    if default_banner in resp:
        print('[\033[92m+\033[00m] Found dionaea smb server')
    else:
        print('[\033[91m-\033[00m] Didn\'t find dionaea smb server')

def main():
    ip = '172.17.0.2'
    print('Start scanning ...')
    port_21(ip)
    port_443(ip)
    port_445(ip)


if __name__ == '__main__':
    main()