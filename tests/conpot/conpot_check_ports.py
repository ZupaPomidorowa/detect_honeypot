import socket


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


def port_2121(ip):
    port = 2121
    print('Connecting to port 2121')
    resp = connect_to_socket(ip, port)
    print(f'Response {repr(resp)}')


def port_5020(ip):
    port = 5020
    print('Connecting to port 5020')
    resp = connect_to_socket(ip, port)
    print(f'Response {repr(resp)}')


def port_8800(ip):
    port = 8800
    print('Connecting to port 8800')
    resp = connect_to_socket(ip, port)
    print(f'Response {repr(resp)}')


def port_10201(ip):
    port = 10201
    print('Connecting to port 10201')
    resp = connect_to_socket(ip, port)
    print(f'Response {repr(resp)}')


def port_44818(ip):
    port = 44818
    print('Connecting to port 44818')
    resp = connect_to_socket(ip, port)
    print(f'Response {repr(resp)}')


def main():
    ip = '172.17.0.2'
    print('Start scanning ...')
    port_2121(ip)
    port_5020(ip)
    port_8800(ip)
    port_10201(ip)
    port_44818(ip)


if __name__ == '__main__':
    main()
