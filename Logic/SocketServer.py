import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('localhost', 63345)
sock.bind(server_address)
sock.listen(1)
while True:
    new_link_str = ''
    connection, client_address = sock.accept()
    request = connection.recv(1024)
    print request
    if request[:3] == 'GET':
        link = request.split()[1]
        if link == '/favicon.ico':
            connection.close()
            continue
        counter = int(link.split('/')[-1][:-5]) + 1
        new_link = link.split('/')[1:-1]
        new_link.append(str(counter) + '.html')
        print link
        print new_link
        for i in new_link:
            new_link_str += '/' + i
    message = """HTTP/1.1 200 OK\r\n\r\n<!DOCTYPE html>
    <html>
    <head lang="en">
        <meta charset="UTF-8">
        <title>You are the winner at life!</title>
    </head>
    <body>
        <p>%s</p>
    </body>
    </html>""" % ('<a href="' + new_link_str + '">' + str(counter) + '</a>')
    connection.sendall(message)
    connection.close()