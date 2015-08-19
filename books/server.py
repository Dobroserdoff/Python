import socket
import urlparse
import epub


def main():
    sock = create_socket()
    reciver_connection(sock)


def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', 12345)
    sock.bind(server_address)
    sock.listen(5)
    return sock


def reciver_connection(sock):
    while True:
        connection, client_address = sock.accept()
        request = connection.recv(1024)
        print request
        if request[:3] == 'GET':
            link = request.split()[1]
            urlparse_result = urlparse.urlparse(link)
            if urlparse_result.path == '/favicon.ico':
                process_favicon(connection)
                connection.close()
                continue
            result = urlparse.parse_qs(urlparse_result.query)
            process_connection(result, connection)


def process_favicon(connection):
    with open('favicon.ico', 'r') as icon_file:
        icon = icon_file.read()
        connection.sendall('HTTP/1.1 200 OK\r\n\r\n' + icon)


def process_connection(query, connection):
    print query
    if not query:
        html_str = create_index()
    elif query['submit'][0] == ['ok']:
        book = epub.Book()
        book.load(query['epub_file'][0])

    reply(connection, html_str)


def reply(connection, content):
    connection.sendall(content)
    connection.close()


def header(title, style=None):
    """
    Builds html header
    :param title:  Title
    :param style: css directions
    :return: html string
    """
    title = Element('<title>', title)
    meta = Element('<meta >').set_attribute('cahrset', 'UTF-8')
    if style:
        head = Element('<head>', meta + style + title)
    else:
        head = Element('<head>', meta + title)
    result = head.set_attribute('lang', 'en')
    return result


def create_index():
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    head = header('.epub reader')

    title = Element('<h1>', 'Choose .epub file').set_attribute('align', 'center')
    epub_file = Element('<input >').set_attribute('type', 'file').set_attribute('name', 'epub_file')
    ok_button = Element('<button>', 'Ok').set_attribute('name', 'submit').set_attribute('value', 'ok')
    br = Element('<br />')
    form = Element('<form>', epub_file + br + ok_button).set_attribute('align', 'center')
    body = Element('<body>', title + form)

    return doctype + str(head) + str(body)


class Element(object):

    def __init__(self, tag, content=None, tab=0):
        self.tag = tag
        self.closingtag = tag[0] + '/' + tag[1:]
        if (tag[-2] == '/') or (tag[-2] == ' '):
            self.closingtag = None
        self.tab = tab
        self.content = content

    def __str__(self):
        if self.content:
            result = self.tab * '\t' + self.tag + '\n'
            str_content = str(self.content)
            lines = str_content.split('\n')
            if '' in lines:
                lines.remove('')
            for line in lines:
                result += (self.tab + 1) * '\t' + line + '\n'
            if self.closingtag:
                result += self.tab * '\t' + self.closingtag + '\n'
        else:
            result = self.tab * '\t' + self.tag + '\n'
            if self.closingtag:
                result += self.tab * '\t' + self.closingtag + '\n'
        return result

    def __add__(self, other):
        content = str(self) + str(other)
        if other.closingtag:
            end = content.rfind(other.closingtag)
        else:
            end = len(content)
        if content[len(self.tag):end][-1] == '\n':
            end -= 1
        result = Element(self.tag, content[len(self.tag):end], -1)
        result.closingtag = other.closingtag
        return result

    def set_attribute(self, name, value=None):
        if self.tag[-2] == '/':
            if value:
                attr_tag = self.tag[:-2] + name + '="' + value + '" ' + self.tag[-2:]
                self.tag = attr_tag
            else:
                attr_tag = self.tag[:-2] + name + ' ' + self.tag[-2:]
                self.tag = attr_tag
        else:
            if value:
                attr_tag = self.tag[:-1] + ' ' + name + '="' + value + '"' + self.tag[-1]
                self.tag = attr_tag
            else:
                attr_tag = self.tag[:-1] + ' ' + name + self.tag[-1]
                self.tag = attr_tag
        return self


if __name__ == '__main__':
    main()