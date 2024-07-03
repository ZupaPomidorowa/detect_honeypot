import argparse
import paramiko


class SSHConnect:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ssh = None
        self.chanel = None

    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ip, port=self.port, username=self.username, password=self.password)
            self.chanel = self.ssh.invoke_shell()
            print('Connected')
            print('Start scanning ...')
        except paramiko.BadHostKeyException as badHostKeyException:
            print(f'Server’s host key could not be verified: {badHostKeyException}')
        except paramiko.AuthenticationException:
            print('Authentication failed')
        except paramiko.SSHException as sshException:
            print(f'Can\'t establish SSH connection: {sshException}')
        except Exception as e:
            print(f"Error: {e}")

    def execute_command(self, cmd, end, ignore_first = False):
        buff = ''
        self.chanel.send(cmd + '\n')
        first = True
        while True:
            resp = self.chanel.recv(9999)
            buff += resp.decode('utf-8')
            if ignore_first and first:
                if buff.endswith(end):
                    buff = ''
                    first = False
            else:
                if buff.endswith(end):
                    break
        return buff

    def close(self):
        if self.chanel is not None:
            self.chanel.close()
        if self.ssh is not None:
            self.ssh.close()


def check_osversion(ssh_connection):
    print('Checking os version')
    end = '~# '
    resp = ssh_connection.execute_command('cat /proc/version', end, ignore_first = True)
    version = resp.split('\n')[1].strip('\x1b[4l').strip('\r')
    default_version = 'Linux version 3.2.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.6.3 (Debian 4.6.3-14) ) #1 SMP Debian 3.2.68-1+deb7u1'
    if version == default_version:
        print('[\033[92m+\033[00m] Found the same os version')
    else:
        print('[\033[91m-\033[00m"] Os version is different')

def print_detect_cowrie():
    detect_cowrie_art = """
  ____                   _            _      _            _   
 / ___|_ __ _____      _(_) ___    __| | ___| |_ ___  ___| |_ 
| |   | '__/ _ \ \ /\ / / |/ _ \  / _` |/ _ \ __/ _ \/ __| __|
| |___| | | (_) \ V  V /| |  __/ | (_| |  __/ ||  __/ (__| |_ 
 \____|_|  \___/ \_/\_/ |_|\___|  \__,_|\___|\__\___|\___|\__|
    """
    print(detect_cowrie_art)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', type=str, action='store', help="IP address to connect")
    parser.add_argument("-u", "--username", action='store', help="Connect using a specific username")
    parser.add_argument("-p", "--password", action='store', help="Connect using a specific password")

    args = parser.parse_args()

    print_detect_cowrie()

    ssh_connection = SSHConnect(args.ip, '2222', args.username, args.password)
    print('Connecting via ssh ...')
    ssh_connection.connect()
    check_osversion(ssh_connection)


if __name__ == "__main__":
    main()


def check_name(chan):
    #svr@04
    pass


def check_group(chan):
    #cat /etc/group
    #cat /etc/shadow
    #cat /ctc/passwd
    pass


def check_cpu(chan):
    #cat /proc/cpuinfo
    pass


def check_mounts(chan):
    # cat /proc/mounts
    pass


def check_meminfo(chan):
    buff = ''
    while not buff.endswith(':~# '):
        resp = chan.recv(9999)
        buff += resp.decode('utf-8')

    chan.send('cat /proc/meminfo' + '\n')

    buff = ''
    memory = ''
    while not buff.endswith(':~# '):
        resp = chan.recv(9999)
        if resp.decode('utf-8') != ':MemFree:          997740 kB' and resp != b'\x1b[4h':
            memory = resp
        buff += resp.decode('utf-8')
        print(resp.decode('utf-8'))

    print('dupa')
    print(memory)






