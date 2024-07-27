import argparse
import nmap3
import json


def run_nmap(ip_adders):
    print(f'Start nmap scan {ip_adders}')
    nmap = nmap3.Nmap()
    result: dict = nmap.nmap_version_detection(ip_adders, args='-p- -A -T4')

    if check_cowrie(result):
        print('Cowrie honeypot detected')
    elif check_kippo(result):
        print('Kippo honeypot detected')
    elif check_dionaea(result):
        print('Dionaea honeypot detected')
    elif check_conpot(result):
        print('Conpot honeypot detected')


def check_cowrie(scan_result):
    ip = list(scan_result.keys())[0]
    ports = scan_result[ip]['ports']

    for port in ports:
        name = port['service'].get('name', '')
        product = port['service'].get('product', '')
        version = port['service'].get('version', '')

        if name == 'ssh' and product == 'OpenSSH' and version == '6.0p1 Debian 4+deb7u2':
            return True

    return False


def check_kippo(scan_result):
    ip = list(scan_result.keys())[0]
    ports = scan_result[ip]['ports']

    for port in ports:
        name = port['service'].get('name', '')
        product = port['service'].get('product', '')
        version = port['service'].get('version', '')

        if name == 'ssh' and product == 'OpenSSH' and version == '5.1p1 Debian 5':
            return True

    return False


def check_dionaea(scan_result):
    ip = list(scan_result.keys())[0]
    ports = scan_result[ip]['ports']
    accepted_ports_list = ['21', '23', '42', '53', '80', '135', '443', '445', '1433', '1723', '1883', '3306', '5060',
                           '9100', '11211', '27017']
    accepted_ports = True

    for port in ports:
        if port['portid'] not in accepted_ports_list:
            accepted_ports = False

    if 'dionaea' in json.dumps(scan_result).lower() and accepted_ports:
        return True
    return False


def check_conpot(scan_result):
    ip = list(scan_result.keys())[0]
    ports = scan_result[ip]['ports']
    state = scan_result[ip]['state']['state']

    if not ports and state == 'up':
        return True

    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str, required=True, help="IP address to scan")

    args = parser.parse_args()

    run_nmap(args.ip)


if __name__ == "__main__":
    main()
