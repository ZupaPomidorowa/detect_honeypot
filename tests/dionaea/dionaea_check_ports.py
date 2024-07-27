import argparse
import socket


def connect_to_socket(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            resp = s.recv(1024).decode().strip()
            return resp
    except socket.error as e:
        print(f'Socket error: {e}')
        return None


def port_21(ip):
    port = 21
    print('Connecting to port 21')
    resp = connect_to_socket(ip, port)
    default_banner = '220 DiskStation FTP server ready.'
    if resp == default_banner:
        print('[\033[92m+\033[00m] Found default FTP banner')
    elif resp == None:
        print('[\033[93m?\033[00m] Didn\'t get response')
    else:
        print('[\033[91m-\033[00m] Didn\'t find default FTP banner')


def port_23(ip):
    port = 23
    print('Connecting to port 23')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find default FTP banner')


def port_42(ip):
    port = 42
    print('Connecting to port 42')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find anything')


def port_53(ip):
    port = 53
    print('Connecting to port 53')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find anything')


def port_80(ip):
    port = 80
    print('Connecting to port 80')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find anything')


def port_443(ip):
    port = 443
    print('Connecting to port 443')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find anything')


def port_445(ip):
    port = 445
    print('Connecting to port 445')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find anything')


def port_1433(ip):
    port = 1433
    print('Connecting to port 1433')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find anything')


def port_1723(ip):
    port = 1723
    print('Connecting to port 1723')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find anything')


def port_1883(ip):
    port = 1883
    print('Connecting to port 1883')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find anything')


def port_3306(ip):
    port = 3306
    print('Connecting to port 3306')
    resp = connect_to_socket(ip, port)
    print(f'Response {repr(resp)}')


def port_5060(ip):
    port = 5060
    print('Connecting to port 5060')
    resp = connect_to_socket(ip, port)
    if resp != '':
        print(f'[\033[92m+\033[00m] Found banner {resp}')
    elif resp == '':
        print('[\033[93m?\033[00m] Didn\'t get banner')
    else:
        print('[\033[91m-\033[00m] Didn\'t find anything')


def port_9100(ip):
    port = 9100
    print('Connecting to port 9100')
    resp = connect_to_socket(ip, port)
    print(f'Response {repr(resp)}')


def port_11211(ip):
    port = 11211
    print('Connecting to port 11211')
    resp = connect_to_socket(ip, port)
    print(f'Response {repr(resp)}')


def port_27017(ip):
    port = 27017
    print('Connecting to port 27017')
    resp = connect_to_socket(ip, port)
    print(f'Response {repr(resp)}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str, action='store', help='IP address to connect')
    args = parser.parse_args()

    print('Start scanning ...')
    port_21(args.ip)
    port_23(args.ip)
    port_42(args.ip)
    port_53(args.ip)
    port_80(args.ip)
    port_443(args.ip)
    port_445(args.ip)
    port_1433(args.ip)
    port_1723(args.ip)
    port_1883(args.ip)
    port_3306(args.ip)
    port_5060(args.ip)
    port_9100(args.ip)
    port_11211(args.ip)
    port_27017(args.ip)


if __name__ == '__main__':
    main()
