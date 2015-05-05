import socket
import LogicLinear
import urlparse

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('localhost', 63345)
sock.bind(server_address)
sock.listen(5)
while True:
    connection, client_address = sock.accept()
    request = connection.recv(1024)
    print request
    if request[:3] == 'GET':
        link = request.split()[1]
        print link
        if link == '/favicon.ico':
            connection.close()
            continue
    message = """HTTP/1.1 200 OK\r\n\r\n<!DOCTYPE html>
    <html>
    <head lang="en">
        <meta charset="UTF-8">
        <title>Logix</title>
    </head>
    <body>
            <h1 align="center">Logix</h1>
            <form action="http://localhost:63345" method="get">
                <p align="center">Please, input expression:
                    <br />
                    <input type="text" name="equation"  size="30" maxlength="50" align="center" />
                    <br />
                    <input type="submit" value="calculate" align="center" />
                </p>
    </form>
    </body>
    </html>"""
    connection.sendall(message)
    table = urlparse.parse_qs(urlparse.urlparse(link).query)
    print table
    if 'equation' in table:
        connection.sendall(LogicLinear.create_html(LogicLinear.html_request(table['equation'][0])))
    connection.close()