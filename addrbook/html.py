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

    def __add__(self, other):
        content = str(self) + str(other)
        end = content.rfind(other.closingtag)
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


def header(title, style=None):
    title = Element('<title>', title)
    if style:
        head = Element('<head>', str('<meta charset="UTF-8">\n') + str(style) + str(title))
    else:
        head = Element('<head>', str('<meta charset="UTF-8">\n') + str(title))
    result = str(head.set_attribute('lang', 'en'))
    return result


def index(book):
    title = Element('<h1>', 'Address Book').set_attribute('align', 'center')
    book_list = []
    for person in book.addrbook:
        personal_link = get_personal_link(person)
        personal_element = Element('<a>', str(personal_link[0])).set_attribute('href', str(personal_link[1]))
        li = Element('<li>', str(personal_element))
        book_list.append(str(li))
    ul = Element('<ul>', ''.join(book_list))
    addbutton = Element('<button>', 'Add Person').set_attribute('name', 'add_person').set_attribute('value', 'on')
    addbutton_center = Element('<center>', str(addbutton))
    addform = Element('<form>', str(addbutton_center)).set_attribute('action', 'http://localhost:33322')
    addform.set_attribute('method', 'get')
    delbutton = Element('<button>', 'Delete Person').set_attribute('name', 'del_person').set_attribute('value', 'on')
    delbutton_center = Element('<center>', str(delbutton))
    delform = Element('<form>', str(delbutton_center)).set_attribute('action', 'http://localhost:33322')
    delform.set_attribute('method', 'get')
    body = Element('<body>', str(title) + str(ul) + str(addform) + str(delform))
    return body


def get_personal_link(person):
    name = person.to_string(['first', 'last'])
    private_query = '/?personal=' + person.to_string(['first']) + '_' + person.to_string(['last'])
    return [name, private_query]


def add_and_edit(value, person=None):
    if value == 'add':
        title = Element('<h1>', 'Add Person').set_attribute('align', 'center')
    else:
        title = Element('<h1>', 'Edit ' + person.to_string(['first']) + ' ' +
                        person.to_string(['last'])).set_attribute('align', 'center')
    cells = create_cells_add_and_edit(person)
    if value == 'add':
        table = create_table(9, 2, ['align', 'center'], cells)
    else:
        table = create_table(10, 2, ['align', 'center'], cells)
    confirm = Element('<input />').set_attribute('type', 'submit').set_attribute('name', 'confirm_' + value)
    confirm.set_attribute('value', 'Confirm')
    confirm_center = Element('<center>', str(confirm))
    form = Element('<form>', str(table) + str(confirm_center)).set_attribute('action', 'http://localhost:33322')
    form.set_attribute('method', 'get')
    cancel = Element('<button>', 'Cancel').set_attribute('name', 'cancel').set_attribute('value', 'on')
    cancel_center = Element('<center>', str(cancel))
    cancel_form = Element('<form>', str(cancel_center)).set_attribute('action', 'http://localhost:33322')
    disclaimer = Element('<p>', str('Fields marked as <sup>*</sup> are obligatory to fill'))
    disclaimer.set_attribute('align', 'center')
    body = Element('<body>', str(title) + str(form) + str(cancel_form) + str(disclaimer))
    return body


def create_cells_add_and_edit(person=None):
    sup = '<sup>*</sup>'
    person_names = ['First Name:', 'Second Name:', 'Last Name:', 'Date of Birth:', 'Phone Number:', 'Spouse:',
                    'Children:', 'Home:', 'Work:']
    person_values = ['first', 'middle', 'last', 'birthday', 'phone', 'spouse', 'kids', 'home', 'work']
    patterns_names = []
    patterns_values = []
    result = []
    for i in person_names:
        if i == 'First Name:' or i == 'Last Name:' or i == 'Date of Birth:':
            pattern_names = Element('<td>', i + str(sup)).set_attribute('align', 'left')
        else:
            pattern_names = Element('<td>', i).set_attribute('align', 'left')
        patterns_names.append(pattern_names)
    for j in person_values:
        pattern_values = Element('<input />').set_attribute('type', 'text').set_attribute('name', j).\
            set_attribute('size', '40').set_attribute('maxlength', '150').set_attribute('align', 'center')
        if person:
            pattern_values.set_attribute('value', person.to_string([j]))
        if j == 'first' or j == 'last' or j == 'birthday':
            pattern_values.set_attribute('required')
        if j == 'birthday':
            pattern_values.set_attribute('placeholder', 'YYYY, MM, DD')
            pattern_values.set_attribute('pattern', '\d{4}, \d{1,2}, \d{1,2}')
        if j == 'home' or j == 'work':
            pattern_values.set_attribute('placeholder', 'Country, City, Street, Building, Apartment')
        if j == 'spouse':
            pattern_values.set_attribute('placeholder', 'Firstname Lastname')
        if j == 'kids':
            pattern_values.set_attribute('placeholder', 'Firstname Lastname, Firstname Lastname')
        pattern_values_cells = Element('<td>', pattern_values)
        patterns_values.append(pattern_values_cells)
    for k in range(len(patterns_names)):
        result.append(patterns_names[k])
        result.append(patterns_values[k])
    if person:
        hidden_name = Element('<input />').set_attribute('type', 'text').set_attribute('hidden')
        hidden_name.set_attribute('name', 'original').set_attribute('value', person.first + '_' + person.last)
        result.append(hidden_name)
        result.append('')
    return result


def delete(book):
    title = Element('<h1>', 'Delete Person').set_attribute('align', 'center')
    book_list = []
    for person in book.addrbook:
        input_element = Element('<input />').set_attribute('type', 'checkbox')
        input_element.set_attribute('id', person.first[0] + person.last[0])
        input_element.set_attribute('name', 'del_' + person.first + '_' + person.last)
        label = Element('<label>', person.first + ' ' + person.last)
        label.set_attribute('for', person.first[0] + person.last[0])
        li = Element('<li>', str(input_element) + str(label))
        book_list.append(str(li))
    ul = Element('<ul>', ''.join(book_list))
    listcell = Element('<td>', str(ul))
    confirm = Element('<input />').set_attribute('type', 'submit').set_attribute('name', 'confirm_del')
    confirm.set_attribute('value', 'Confirm')
    confirm_center = Element('<center>', str(confirm))
    confirmcell = Element('<td>', str(confirm_center))
    table = create_table(2, 1, ['align', 'center'], [listcell, confirmcell])
    form = Element('<form>', str(table)).set_attribute('action', 'http://localhost:33322')
    form.set_attribute('method', 'get')
    disclaimer = Element('<p>', 'Please, select one or more person you want to delete')
    disclaimer.set_attribute('align', 'center')
    body = Element('<body>', str(title) + str(form) + str(disclaimer))
    return body


def personal(person):
    title = Element('<h1>', person.to_string(['first']) + ' ' +
                    person.to_string(['last'])).set_attribute('align', 'center')
    cells = create_cells_personal(person)
    table = create_table(cells[0], 2, ['align', 'center'], cells[1])
    edit_button = Element('<button>', 'Edit').set_attribute('name', 'edit')
    edit_button.set_attribute('value', person.first + '_' + person.last)
    ok_button = Element('<button>', 'Ok').set_attribute('name', 'personal_ok')
    ok_button.set_attribute('value', 'on')
    form = Element('<form>', str(edit_button) + str(Element('<br />')) + str(ok_button))
    form.set_attribute('action', 'http://localhost:33322').set_attribute('method', 'get')
    center_form = Element('<center>', str(form))
    body = Element('<body>', str(title) + str(table) + str(center_form))
    return body


def create_cells_personal(person):
    result = []
    counter = 0
    set_order = ['Name:', 'Second Name:', 'Last Name:', 'Date of Birth:', 'Phone Number:', 'Spouse:', 'Children:',
                 'Home Address:', 'Work Address:']
    for i in range(len(set_order)):
        if person[i]:
            result.append(Element('<td>', set_order[i]))
            if i == 5:
                link = Element('<a>', person.spouse.to_string(['first', 'last']))
                link.set_attribute('href', '/?personal=' + person.spouse.to_string(['first']) + '_' +
                                   person.spouse.to_string(['last']))
                cell = Element('<td>', str(link))
            elif i == 6:
                children = []
                for kid in person.kids:
                    link = Element('<a>', kid.first + ' ' + kid.last)
                    link.set_attribute('href', '/?personal=' + kid.first + '_' + kid.last)
                    children.append(str(link))
                    if kid != person.kids[-1]:
                        children.append(str(Element('<br />')))
                cell = Element('<td>', ''.join(children))
            else:
                cell = Element('<td>', person[i])
            counter += 1
            result.append(cell)
    final = [counter, result]
    return final


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
        if k % 2:
            continue
        table.set_attribute(attributes[k], attributes[k+1])
        k += 2
        if k == len(attributes):
            break
    return table