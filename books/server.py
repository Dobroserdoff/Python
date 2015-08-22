import socket
import urlparse
import zipfile
import os
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
            result = {'submit': []}
            link = request.split()[1]
            urlparse_result = urlparse.urlparse(link)
            if urlparse_result.path == '/favicon.ico':
                process_favicon(connection)
                connection.close()
                continue
            elif urlparse_result.path == '/':
                result = urlparse.parse_qs(urlparse_result.query)
            elif len(urlparse_result.path) > 1:
                result['link'] = urlparse_result.path
            if not result:
                content = create_index()
                reply(connection, content)
            elif result['submit'] == ['index_ok']:
                book, epub_zip = get_book(result)
                process_connection(result, connection, book, epub_zip)
            else:
                process_connection(result, connection, book, epub_zip)


def process_favicon(connection):
    with open('favicon.ico', 'r') as icon_file:
        icon = icon_file.read()
        connection.sendall('HTTP/1.1 200 OK\r\n\r\n' + icon)


def get_book(query):
        book = epub.Book()
        book.load(query['epub_file'][0])
        epub_zip = zipfile.ZipFile(query['epub_file'][0])
        return book, epub_zip


def process_connection(query, connection, book, epub_zip):
    print query
    if query['submit'] == ['index_ok']:
        content = create_title(book, epub_zip)
    elif query['submit'] == ['index']:
        content = create_index()
    elif query['submit'] == ['contents']:
        content = create_title(book, epub_zip)
    elif query['submit'] == ['annotation']:
        content = create_title(book, epub_zip)
    elif query['link'][-4:] == '.css':
        content = epub_zip.read(book.content + query['link'])

    reply(connection, content)


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
    meta = Element('<meta >').set_attribute('charset', 'UTF-8')
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
    epub_file.set_attribute('width', '50px')
    ok_button = Element('<button>', 'Ok').set_attribute('name', 'submit').set_attribute('value', 'index_ok')
    br = Element('<br />')
    form = Element('<form>', epub_file + br + ok_button).set_attribute('align', 'center')
    body = Element('<body>', title + form)

    return doctype + str(head) + str(body)


def create_title(book, epub_zip):
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    content = epub.find_content(epub_zip.open('META-INF/container.xml'))
    content_dir = os.path.dirname(content)

    guide = book.get_descr().get_guide_element()
    for item in guide:
        if item.attrib['title'] == 'title':
            title = content_dir + '/' + item.attrib['href']

    xhtml_str = epub_zip.read(title)
    html_tag = '<html lang="en">\n  <meta  charset="UTF-8">\n  '
    head_start = xhtml_str.find('<head>')
    body_close = xhtml_str.find('  </body>')
    xhtml_str = doctype + html_tag + xhtml_str[head_start:body_close] + title_buttons() + xhtml_str[body_close:]
    return xhtml_str


def title_buttons():
    index = Element('<button>', 'Index').set_attribute('name', 'submit').set_attribute('value', 'index')
    contents = Element('<button>', 'Contents').set_attribute('name', 'submit').set_attribute('value', 'contents')
    annotation = Element('<button>', 'Annotation').set_attribute('name', 'submit').set_attribute('value', 'annotation')

    form = Element('<form>', index + contents + annotation)
    center = Element('<center>', form, 2)

    return str(center)


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
            result = self.tab * '  ' + self.tag + '\n'
            str_content = str(self.content)
            lines = str_content.split('\n')
            if '' in lines:
                lines.remove('')
            for line in lines:
                result += (self.tab + 1) * '  ' + line + '\n'
            if self.closingtag:
                result += self.tab * '  ' + self.closingtag + '\n'
        else:
            result = self.tab * '  ' + self.tag + '\n'
            if self.closingtag:
                result += self.tab * '  ' + self.closingtag + '\n'
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