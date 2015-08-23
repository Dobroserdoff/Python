import socket
import urlparse
import zipfile
import epub
import xml.etree.ElementTree as ET


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
        content = create_title_or_annotation(book, epub_zip, ['title', 'annotation'])
    elif query['submit'] == ['index']:
        content = create_index()
    elif query['submit'] == ['title']:
        content = create_title_or_annotation(book, epub_zip, ['title', 'annotation'])
    elif query['submit'] == ['contents']:
        content = create_contents(book, epub_zip)
    elif query['submit'] == ['annotation']:
        content = create_title_or_annotation(book, epub_zip, ['annotation', 'title'])
    elif query['link'][-4:] == '.css':
        content = epub_zip.read(book.content + query['link'])
    elif query['link'][-6:] == '.xhtml':
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
    """
    Creates index page html string on demand
    :return: html string
    """
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    head = header('.epub reader')

    title = Element('<h1>', 'Choose .epub file').set_attribute('align', 'center')
    epub_file = Element('<input >').set_attribute('type', 'file').set_attribute('name', 'epub_file')
    epub_file.set_attribute('width', '50px')
    ok_button = Element('<button>', 'Ok').set_attribute('name', 'submit').set_attribute('value', 'index_ok')
    br = Element('<br />')
    form = Element('<form>', epub_file + br + ok_button).set_attribute('align', 'center')
    body = Element('<body>', title + form)

    html = Element('<html>', head + body)
    return doctype + str(html)


def create_title_or_annotation(book, epub_zip, value):
    """
    Creates title page html string
    :param book: epub.Book()
    :param epub_zip: ZipFile
    :return: html string
    """
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'

    guide = book.get_descr().get_guide_element()
    for item in guide:
        if item.attrib['title'] == value[0]:
            title = book.content + '/' + item.attrib['href']

    xhtml_str = epub_zip.read(title)
    html_tag = '<html lang="en">\n  <meta  charset="UTF-8">\n  '
    head_start = xhtml_str.find('<head>')
    body_close = xhtml_str.find('  </body>')
    html_str = doctype + html_tag + xhtml_str[head_start:body_close]
    html_str += str(create_buttons('index', 'contents', value[1])) + xhtml_str[body_close:]

    return html_str


def create_contents(book, epub_zip):
    """
    Creates table of contetnts page html string
    :param book: epub.Book()
    :param epub_zip: ZipFile
    :return: html string
    """
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    head = header('Table of contens')
    br = Element('<br />')

    ncx_element = book.get_descr().find_manifest_items_by_media('application/x-dtbncx+xml')[0]
    file_path = book.content + '/' + ncx_element.attrib['href']
    xml_str = epub_zip.read(file_path)
    root = ET.fromstring(xml_str)

    pairs = []
    get_name_link_pairs(root, pairs)
    elements = get_name_link_elements(pairs)
    result = elements[0] + br
    for i in range(len(elements)):
        if i+1 != len(elements):
            result += elements[i+1] + br
    buttons = create_buttons('index', 'title', 'annotation')
    body = Element('<body>', result + buttons).set_attribute('align', 'center')

    html = Element('<html>', head + body)
    return doctype + str(html)


def get_name_link_pairs(root, pairs):
    """
    Creates list of chapter/link pairs
    :param root: xml element
    :param pairs: list of pairs
    """
    for item in root:
        if item._children:
            get_name_link_pairs(item, pairs)
        else:
            if item.tag[-4:] == 'text':
                pairs.append(item.text.encode('utf-8'))
            elif item.tag[-7:] == 'content':
                pairs.append('$' + item.attrib['src'].encode('utf-8'))


def get_name_link_elements(pairs):
    """
    Creates html elements out of list of pairs
    :param pairs: list of pairs
    :return: list of elements
    """
    elements = []
    for i in range(len(pairs)):
        if i+1 == len(pairs):
            if pairs[i][0] != '$':
                element = Element('<h1>', pairs[i])
            else:
                continue
        else:
            if pairs[i+1][0] == '$':
                element = Element('<a>', pairs[i]).set_attribute('href', pairs[i+1][1:])
            elif pairs[i][0] != '$':
                element = Element('<h1>', pairs[i])
            else:
                continue
        elements.append(element)
    return elements


def create_buttons(first, second, third=None):
    """
    Creates footer navigation buttons
    :param first: name of the first button
    :param second: name of the second button
    :param third: name of the third button (if needed)
    :return: html string
    """
    br = Element('<br />')
    first_element = Element('<button>', first.capitalize()).set_attribute('name', 'submit').set_attribute('value', first)
    second_element = Element('<button>', second.capitalize()).set_attribute('name', 'submit').set_attribute('value', second)

    if third:
        third_element = Element('<button>', third.capitalize()).set_attribute('name', 'submit').set_attribute('value', third)
        form = Element('<form>', first_element + second_element + third_element)
    else:
        form = Element('<form>', first_element + second_element)

    center = Element('<center>', br + br + form)
    return center


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