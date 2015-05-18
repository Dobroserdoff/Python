# -*- coding: utf-8 -*-

class Element(object):

    def __init__(self, tag, content=None, tab=0):
        self.tag = tag
        self.closingtag = tag[0] + '/' + tag[1:]
        if tag[-2] == '/':
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

def header(title):
    style = Element('<style>', 'ul {list-style-type: none; text-align:center;}\nsup {color: red}')
    title = Element('<title>', title)
    head = Element('<head>', str('<meta charset="UTF-8">\n') + str(style) + str(title))
    result = str(head.set_attribute('lang', 'en'))
    return result

def index(book):
    h1 = Element('<h1>', 'Address Book').set_attribute('align', 'center')
    book_list = []
    for person in book.addrbook:
        personal_link = get_personal_link(person)
        personal_element = Element('<a>', str(personal_link[0])).set_attribute('href', str(personal_link[1]))
        li = Element('<li>', str(personal_element))
        book_list.append(str(li))
    ul = Element('<ul>', ''.join(book_list))
    cells = create_cells_index()
    table = create_table(1, 2, ['align', 'center'], cells)
    body = Element('<body>', str(h1) + str(ul) + str(table))
    return body


def create_cells_index():
    button001 = Element('<button>', 'Add Person').set_attribute('name', 'add_person').set_attribute('value', 'on')
    cell001 = Element('<form>', str(button001)).set_attribute('action', 'http://localhost:33322')
    cell001.set_attribute('method', 'get')
    result001 = Element('<td>', str(cell001))
    button002 = Element('<button>', 'Delete Person').set_attribute('name', 'del_person').set_attribute('value', 'on')
    cell002 = Element('<form>', str(button002)).set_attribute('action', 'http://localhost:33322')
    cell002.set_attribute('method', 'get')
    result002 = Element('<td>', str(cell002))
    result = [result001, result002]
    return result


def add():
    title = Element('<h1>', 'Add Person').set_attribute('align', 'center')
    cells = create_cells_add()
    table = create_table(8, 2, ['align', 'center'], cells)
    form = Element('<form>', str(table)).set_attribute('action', 'http://localhost:33322')
    form.set_attribute('method', 'get')
    disclaimer = Element('<p>', str('Fields marked as <sup>*</sup> are obligatory to fill'))
    disclaimer.set_attribute('align', 'center')
    body = Element('<body>', str(title) + str(form) + str(disclaimer))
    return body


def create_cells_add():
    sup = '<sup>*</sup>'
    person_names = ['First Name:', 'Second Name:', 'Last Name:', 'Date of Birth:', 'Phone Number:', 'Home:', 'Work:']
    person_values = ['first', 'middle', 'last', 'birthday', 'phone', 'home', 'work']
    patterns_names = []
    patterns_values = []
    result =[]
    for i in person_names:
        if i == 'First Name:' or i == 'Last Name:' or i == 'Date of Birth:':
            pattern_names = Element('<td>', i + str(sup)).set_attribute('align', 'left')
        else:
            pattern_names = Element('<td>', i).set_attribute('align', 'left')
        patterns_names.append(pattern_names)
    for j in person_values:
        pattern_values = Element('<input />').set_attribute('type', 'text').set_attribute('name', j).\
            set_attribute('size', '40').set_attribute('maxlength', '50').set_attribute('align', 'center')
        if j == 'first' or j == 'last' or j == 'birthday':
            pattern_values.set_attribute('required')
        if j == 'birthday':
            pattern_values.set_attribute('placeholder', 'YYYY, MM, DD')
            pattern_values.set_attribute('pattern', '\d{4}, \d{1,2}, \d{1,2}')
        if j == 'home' or j == 'work':
            pattern_values.set_attribute('placeholder', 'Country, City, Street, Building, Apartment')
        pattern_values_cells = Element('<td>', pattern_values)
        patterns_values.append(pattern_values_cells)
    for k in range(len(patterns_names)):
        result.append(patterns_names[k])
        result.append(patterns_values[k])
    confirm = Element('<input />').set_attribute('type', 'submit').set_attribute('name', 'confirm_add')
    confirm.set_attribute('value', 'Confirm')
    cell_confirm = Element('<td>', str(confirm)).set_attribute('align', 'right')
    result.append(cell_confirm)
    cancel = Element('<button>', 'Cancel').set_attribute('name', 'cancel').set_attribute('value', 'on')
    cancel_form = Element('<form>', str(cancel)).set_attribute('action', 'http://localhost:33322')
    cell_cancel = Element('<td>', str(cancel_form)).set_attribute('align', 'left')
    result.append(cell_cancel)
    return result


def get_personal_link(person):
    name = person.to_string(['first', 'last'])
    private_query = '/?personal=' + person.to_string(['first']) + '_' + person.to_string(['last'])
    return [name, private_query]


def create_table(rows, columns, attributes, content):
    allrows = []
    allcolumns = []
    j = 0
    while j < rows:
        i = 0
        while i < columns:
            handycap = j * columns
            allcolumns.append(str(content[i+handycap]))
            i += 1
        row = Element('<tr>', ''.join(allcolumns))
        allcolumns = []
        allrows.append(str(row))
        j += 1
    table = Element('<table>', ''.join(allrows))
    allrows = []
    for k in range(len(attributes)):
        table.set_attribute(attributes[k], attributes[k+1])
        k += 2
        if k == len(attributes):
            break
    return table