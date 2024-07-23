from ftplib import FTP
import http.client

def check_ftp(ip, port):
    ftp = FTP()
    print(ip, port, ftp)
    ftp.connect(ip, port)
    response = ftp.getwelcome()
    print(response)
    response = ftp.sendcmd("'")
    print(response)
    ftp.quit()
    return response


def check_http(ip, port):
    conn = http.client.HTTPConnection(ip, port, timeout=30)
    conn.request("GET", "/")
    response = conn.getresponse()
    print(response)
    print(response.status, response.reason)
    conn.close()
    return response


def main():
    ip = '172.17.0.2'
    print('Start scanning ...')
    port = 2121
    print('Connecting to port 2121')
    ftp_response = check_ftp(ip, port)
    print(ftp_response)
    #port = 8800
    #print('Connecting to port 8800')
    #http_response = check_http(ip, port)
    #print(http_response)


if __name__ == "__main__":
    main()
