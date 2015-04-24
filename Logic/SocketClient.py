import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 62266)
sock.connect(server_address)
sock.sendall('This is the message.  It will be repeated.')
sock.close()