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
        except paramiko.BadHostKeyException as badHostKeyException:
            print(f'Server’s host key could not be verified: {badHostKeyException}')
        except paramiko.AuthenticationException:
            print('Authentication failed')
        except paramiko.SSHException as sshException:
            print(f'Can\'t establish SSH connection: {sshException}')
        except Exception as e:
            print(f"Error: {e}")

    def execute_command(self, cmd, end, ignore_first=False):
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
