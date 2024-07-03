import argparse
import socket

def detect_kippo(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created successfully')
    except socket.error as e:
        print(f'Socket creation failed: {e}')

    s.connect((ip, port))
    resp = s.recv(1024).decode().strip()
    s.close()

    default_banner = 'SSH-2.0-OpenSSH_5.1p1 Debian-5'
    if resp == default_banner:
        print('[\033[92m+\033[00m] Found default banner')
        return True
    print('[\033[91m-\033[00m] Didn\'t find default banner')
    return False



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str, action='store', help='IP address to connect')
    args = parser.parse_args()

    print('Start scanning ...')
    port = 2222

    if detect_kippo(args.ip, port):
        print('Kippo honeypot detected')
    else:
        print('Kippo honeypot not detected')


if __name__ == "__main__":
    main()