import argparse
import paramiko
from sshconnect import SSHConnect


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


def check_meminfo(ssh_connection):
    print('Checking memory info')
    end = '~# '
    resp = ssh_connection.execute_command('cat /proc/meminfo', end)
    memory = resp.split('\n')[2].strip('\r')
    default_memory = 'MemFree:          997740 kB'
    if memory == default_memory:
        print('[\033[92m+\033[00m] Found static memory information')
    else:
        print('[\033[91m-\033[00m"] Memory is different than default value')


def check_mounts(ssh_connection):
    print('Checking mounts file')
    end = '~# '
    resp = ssh_connection.execute_command('cat /proc/mounts', end)
    mounts = '\n'.join(resp.split('\n')[1:-1])
    mounts = mounts.strip('\x1b[4l').replace('\r', '')
    default_mounts = """rootfs / rootfs rw 0 0
    sysfs /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0
    proc /proc proc rw,relatime 0 0
    udev /dev devtmpfs rw,relatime,size=10240k,nr_inodes=997843,mode=755 0 0
    devpts /dev/pts devpts rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000 0 0
    tmpfs /run tmpfs rw,nosuid,relatime,size=1613336k,mode=755 0 0
    /dev/dm-0 / ext3 rw,relatime,errors=remount-ro,data=ordered 0 0
    tmpfs /dev/shm tmpfs rw,nosuid,nodev 0 0
    tmpfs /run/lock tmpfs rw,nosuid,nodev,noexec,relatime,size=5120k 0 0
    systemd-1 /proc/sys/fs/binfmt_misc autofs rw,relatime,fd=22,pgrp=1,timeout=300,minproto=5,maxproto=5,direct 0 0
    fusectl /sys/fs/fuse/connections fusectl rw,relatime 0 0
    /dev/sda1 /boot ext2 rw,relatime 0 0
    /dev/mapper/home /home ext3 rw,relatime,data=ordered 0 0
    binfmt_misc /proc/sys/fs/binfmt_misc binfmt_misc rw,relatime 0 0"""
    default_mounts = default_mounts.replace('    ', '')
    if mounts == default_mounts:
        print('[\033[92m+\033[00m] Found default mounted file systems')
    else:
        print('[\033[91m-\033[00m] Mounted file systems are different')


def check_cpu(ssh_connection):
    print('Checking cpu')
    end = '~# '
    resp = ssh_connection.execute_command('cat /proc/cpuinfo', end)
    cpu = resp.split('\n')[5].strip('\r')
    default_cpu = 'model name	: Intel(R) Core(TM)2 Duo CPU     E8200  @ 2.66GHz'
    if cpu == default_cpu:
        print('[\033[92m+\033[00m] Found default cpu')
    else:
        print('[\033[91m-\033[00m] Cpus are different')


def check_group(ssh_connection):
    #cat /ctc/passwd
    print('Checking group file')
    end = '~# '
    resp = ssh_connection.execute_command('cat /etc/group', end)
    group = resp.split('\n')[-2]
    group = group.split(':')[0]
    default_group = 'phil'
    if group == default_group:
        print('[\033[92m+\033[00m] Found phil in group')
    else:
        print('[\033[91m-\033[00m] Didn\'t find phil in group')


def check_shadow(ssh_connection):
    print('Checking shadow file')
    end = '~# '
    resp = ssh_connection.execute_command('cat /etc/shadow', end)
    default_user = 'phil'
    if default_user in resp:
        print('[\033[92m+\033[00m] Found user phil in shadow file')
    else:
        print('[\033[91m-\033[00m] Didn\'t find user phil in shadow file')


def check_passwd(ssh_connection):
    print('Checking passwd file')
    end = '~# '
    resp = ssh_connection.execute_command('cat /etc/passwd', end)
    default_user = 'phil'
    if default_user in resp:
        print('[\033[92m+\033[00m] Found user phil in passwd file')
    else:
        print('[\033[91m-\033[00m] Didn\'t find user phil in passwd file')


def check_hostname(ssh_connection):
    print('Checking hostname')
    end = '~# '
    resp = ssh_connection.execute_command('', end)
    if 'svr04' in resp:
        print('[\033[92m+\033[00m] Found defeault hostname')
    else:
        print('[\033[91m-\033[00m] Didn\'t find default hostname')


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
    print(f'Connecting to {args.ip} with username {args.username} and password {args.password} ...')
    ssh_connection.connect()
    print('Start scanning ...')
    check_osversion(ssh_connection)
    check_meminfo(ssh_connection)
    check_mounts(ssh_connection)
    check_cpu(ssh_connection)
    check_group(ssh_connection)
    check_shadow(ssh_connection)
    check_passwd(ssh_connection)
    check_hostname(ssh_connection)


if __name__ == "__main__":
    main()





