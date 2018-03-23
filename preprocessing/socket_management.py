import socket

# host and port # for gpu machine. If testing, below 2 lines will not be activated
#host = '143.248.48.96'
#port = 8890

host = "127.0.0.1"
port = 8890

#below function sends *youtube url* to the gpu machine.
# url example : TODO (set it right!)
def send_url(url):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(url.encode())
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))
