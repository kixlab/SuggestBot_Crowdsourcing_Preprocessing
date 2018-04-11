import socket

# host and port # for gpu machine. If testing, below 2 lines will not be activated
host = '143.248.48.96'
port = 8890

#host = "115.68.222.144"
#port = 8890

#below function sends *youtube url* to the gpu machine.
# url example : TODO (set it right!)
def send_url(url):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except socket.error as e:
        print("socket error occurred:",e)
    s.sendall(url.encode())
    handshake = "\n.....waiting for the files to receive..."
    s.sendall(handshake.encode())
    data = s.recv(1024)
    if not data:
        print('closing connection!!!')
    s.close()
