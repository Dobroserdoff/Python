import socket
import urlparse
import html
# -*- coding: utf-8 -*-


class Date(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        """
        creates nice string of date to print
        :return: str
        """
        return '%s, %s, %s' % (self.year, self.month, self.day)

    def __cmp__(self, other_date):
        """
        compares date with other_date
        :param other_date: date to compare with
        :return: int
        """
        if self.year < other_date.year:
            return -1
        if self.year > other_date.year:
            return 1
        if self.month < other_date.month:
            return -1
        if self.month > other_date.month:
            return 1
        if self.day < other_date.day:
            return -1
        if self.day > other_date.day:
            return 1
        return 0


class Address(object):
    def __init__(self, country=None, city=None, street=None, building=None, apartment=None):
        self.country = country
        self.city = city
        self.street = street
        self.building = building
        self.apartment = apartment
        self.props = [self.country, self.city, self.street, self.building, self.apartment]

    def __str__(self):
        addr = []
        for i in self.props:
            if i:
                addr.append(i)
        return ', '.join(addr)

    def match(self, request):
        addr = []
        for i in range(len(request)):
            if request[i] == self.props[i]:
                addr.append(request[i])
        if len(addr) == len(request):
            return True
        else:
            return False


class Person(object):
    def __init__(self, first=None, middle=None, last=None, birthday=None, phone=None, spouse=None, kids=None, home=None,
                 work=None, number=None):
        self.first = first
        self.middle = middle
        self.last = last
        self.birthday = birthday
        self.phone = phone
        self.spouse = spouse
        if kids:
            self.kids = kids
        else:
            self.kids = []
        self.home = home
        self.work = work
        self.number = number
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        person = [self.first, self.middle, self.last, self.birthday, self.phone, self.spouse, self.kids, self.home,
                  self.work, self.number]
        if self.index == len(person):
            raise StopIteration()
        result = person[self.index]
        self.index += 1
        return result

    def __getitem__(self, item):
        person = [self.first, self.middle, self.last, self.birthday, self.phone, self.spouse, self.kids, self.home,
                  self.work, self.number]
        return person[item]

    def __setitem__(self, key, value):
        if key == 0:
            self.first = value
        if key == 1:
            self.middle = value
        if key == 2:
            self.last = value
        if key == 3:
            self.birthday = value
        if key == 4:
            self.phone = value
        if key == 5:
            self.spouse = value
        if key == 6:
            self.kids = value
        if key == 7:
            self.home = value
        if key == 8:
            self.home = value
        if key == 9:
            self.number = value

    def create_from_name_and_birthday(self, first_name, last_name, birthday):
        """
        creates a personal data to work with
        :param first_name:
        :param last_name:
        :param birthday:
        """
        self.first = first_name
        self.last = last_name
        self.birthday = birthday

    def fill_from_file_string(self, line):
        """
        convert specified string of file into personal data to work with
        :type line: str
        """
        line = line.split('$')[:-1]
        self.first = line[0]
        self.middle = line[1]
        self.last = line[2]

        if line[3]:
            parts = line[3].split(', ')
            self.birthday = Date(parts[0], parts[1], parts[2])

        self.phone = line[4]
        self.spouse = line[5]

        if len(line[6]) > 0:
            for j in line[6].split('&'):
                self.kids.append(j)

        if line[7]:
            parts = line[7].split(', ')
            self.home = Address()
            for i in range(len(parts)):
                self.home.props[i] = parts[i]

        if line[8]:
            parts = line[8].split(', ')
            self.work = Address()
            for i in range(len(parts)):
                self.work.props[i] = parts[i]

        self.number = line[9]

    def to_file_string(self):
        """ return srt to store in file
        :rtype: str
        """
        result = []
        heritage = []
        person = [self.first, self.middle, self.last, self.birthday, self.phone, self.spouse, self.kids, self.home,
                  self.work, self.number]
        for prop_field in person:
            if self.spouse and prop_field is self.spouse:
                result.append(self.spouse.to_string(['number']))
            elif prop_field is self.kids:
                for j in self.kids:
                    heritage.append(j.number)
                result.append('&'.join(heritage))
            else:
                result.append(str(prop_field) if prop_field else '')
        result.append('\n')
        return '$'.join(result)

    def compare(self, other_human, sort_prop='first'):
        """ compare us with other human using specified sort_prop
            sort_props is string with property name
            :return int
        """
        my_prop_value = self.get_prop_by_name(sort_prop)
        other_prop_value = other_human.get_prop_by_name(sort_prop)

        if my_prop_value is None:
            if other_prop_value is None:
                return 0
            return -1

        if other_prop_value is None:
            return 1

        return cmp(my_prop_value, other_prop_value)

    def get_prop_by_name(self, prop_name):
        """
        :param prop_name:
        :rtype: Text | Data | None
        """
        if prop_name == 'first':
            return self.first
        if prop_name == 'middle':
            return self.middle
        if prop_name == 'last':
            return self.last
        if prop_name == 'birthday':
            return self.birthday
        if prop_name == 'phone':
            return self.phone
        if prop_name == 'spouse':
            return self.spouse
        if prop_name == 'kids':
            result = []
            if self.kids:
                for i in self.kids:
                    result.append(i)
                return result
        if prop_name == 'home':
            return self.home
        if prop_name == 'work':
            return self.work
        if prop_name == 'number':
            return self.number
        return None

    def to_string(self, print_props_names=None):
        """ create pretty string for printing
            print_props is array with names as strings
            :return: str
        """
        result = []

        if print_props_names is None:
            print_props_names = ['first', 'middle', 'last', 'birthday', 'phone', 'spouse', 'kids', 'home', 'work']

        for print_prop_name in print_props_names:
            if print_prop_name == 'spouse' and self.spouse:
                result.append(self.spouse.to_string(['first', 'last']))
                continue

            if print_prop_name == 'kids':
                for kid in self.kids:
                    if kid != self.kids[-1]:
                        result.append(kid.first)
                        result.append(kid.last + ',')
                    else:
                        result.append(kid.first)
                        result.append(kid.last)
                continue

            prop_value = self.get_prop_by_name(print_prop_name)

            if not prop_value:
                continue

            result.append(str(prop_value))
        return ' '.join(result)

    def set_middle_name(self, name):
        self.middle = name

    def set_phone(self, phone):
        self.phone = phone

    def set_spouse(self, person):
        self.spouse = person

    def add_kid(self, kid):
        self.kids.append(kid)

    def set_home(self, address):
        self.home = address

    def set_work(self, address):
        self.work = address

    def set_number(self):
        number = self.first[0]
        if self.middle:
            number += self.middle[0]
        number += self.last[0]
        number += str(self.birthday.year) + str(self.birthday.month) + str(self.birthday.day)
        self.number = number

    def match(self, request, add_request=None):
        person = [self.first, self.middle, self.last, self.phone]
        if add_request:
            return request in person and add_request in person
        else:
            return request in person

    def match_number(self, request):
        return self.number == request

    def spouse_kids_fix(self, book):
        if self.spouse:
            self.spouse = book.find_person_by_number(self.spouse)
        if len(self.kids) > 0:
            for i in range(len(self.kids)):
                if self.kids[i]:
                    self.kids[i] = book.find_person_by_number(self.kids[i])


class Book(object):
    def __init__(self):
        self.addrbook = []
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        self.addrbook = []
        if self.index == len(self.addrbook):
            raise StopIteration()
        result = self.addrbook[self.index]
        self.index += 1
        return result

    def __getitem__(self, item):
        self.addrbook = []
        return self.addrbook[item]

    def set_numbers(self):
        for i in self.addrbook:
            i.set_number()

    def load_from_file(self, filename):
        my_file = open(filename)
        for line in my_file:
            human = Person()
            human.fill_from_file_string(line)
            self.addrbook.append(human)
        for person in self.addrbook:
            person.spouse_kids_fix(self)

    def save_to_file(self, filename):
        for i in self.addrbook:
            i.set_number()
            filename.write(i.to_file_string())

    def sort(self, prop_name='first'):
        my_compare = lambda o1, o2: o1.compare(o2, prop_name)
        self.addrbook.sort(cmp=my_compare)

    def del_person(self, request, add_request=None):
        try:
            person = self.find_person_by_name(request, add_request)
            self.addrbook.remove(person)
        except Exception as e:
            print e

    def print_all(self, prop_names=None):
        for person in self.addrbook:
            print person.to_string(prop_names)

    def print_by_address(self, request):
        for person in self.addrbook:
            if person.home and person.home.match(request) is True and \
                    person.work and person.work.match(request) is True:
                print (person.first + ' ' + person.last + ' ' + str(person.home) + ' ' + str(person.work) +
                       ' Home & Work')
                continue
            if person.home and person.home.match(request) is True:
                print (person.first + ' ' + person.last + ' ' + str(person.home) + ' Home')
            if person.work and person.work.match(request) is True:
                print (person.first + ' ' + person.last + ' ' + str(person.work) + ' Work')

    def find_person_by_number(self, number):
        """
        Returns human or None if not found
        :param number:
        :rtype: Person
        """
        result = Person()
        for person in self.addrbook:
            if person.match_number(number):
                result = person
                break
            else:
                result = None
        return result

    def find_person_by_name(self, request, add_request=None):
        """
        :param first name, last name:
        :rtype: Person
        """
        result = None
        for person in self.addrbook:
            if person.match(request, add_request):
                if result:
                    raise Exception("Please, specify person")
                else:
                    result = person
        return result


def creation():
    book = []
    human1 = Person()
    human1.create_from_name_and_birthday('John', 'Doe', Date(1970, 11, 3))
    human1.set_middle_name('Dead')
    human1.set_phone('8956')
    human1.set_home(Address('USA', 'New York', '5th Ave', '86', '101'))
    human1.set_number()

    human2 = Person()
    human2.create_from_name_and_birthday('Jane', 'Doe', Date(1975, 2, 4))
    human2.set_middle_name('Zombie')
    human2.set_phone('8031')
    human2.set_spouse(human1)
    human2.set_number()
    human2.set_home(Address('USA', 'New York', '5th Ave', '86', '101'))
    human1.set_spouse(human2)

    human3 = Person()
    human3.create_from_name_and_birthday('Ivan', 'Morozoff', Date(1950, 8, 4))
    human3.set_middle_name('Russian')
    human3.set_phone('9012')
    human3.set_home(Address('Russia', 'Moscow', 'Arbat St', '86', '101'))
    human3.set_work(Address('Russia', 'Moscow', 'Novinsky Blvd', '22', '19'))
    human3.set_number()
    book.append(human3)

    human4 = Person()
    human4.create_from_name_and_birthday('Nicky', 'Devil', Date(1666, 13, 13))
    human4.set_middle_name('Junior')
    human4.set_phone('1488')
    human4.set_home(Address('USA', 'New York', '5th Ave', '86', '101'))
    human4.set_work(Address('USA', 'New York', '10th St', '120', '401'))
    human4.set_number()
    human1.add_kid(human4)
    human2.add_kid(human4)
    book.append(human1)
    book.append(human2)
    book.append(human4)

    human5 = Person()
    human5.create_from_name_and_birthday('John', 'Snow', Date(1673, 05, 12))
    human5.set_middle_name('Bastard')
    human5.set_phone('4183')
    human5.set_home(Address('Westeros', 'The Wall', 'Black Castle', '13', '666'))
    human5.set_number()

    human6 = Person()
    human6.create_from_name_and_birthday('Ygritte', 'Wild', Date(1676, 11, 28))
    human6.set_middle_name('Red')
    human6.set_phone('7913')
    human6.set_home(Address('Westeros', 'North', 'Wastelands', '123', '45'))
    human6.set_spouse(human5)
    human6.set_number()
    human5.set_spouse(human6)

    human7 = Person()
    human7.create_from_name_and_birthday('Olga', 'Petrova', Date(1754, 9, 14))
    human7.set_middle_name('Soviet')
    human7.set_phone('2462')
    human7.set_home(Address('Russia', 'Ekaterinburg', 'Lenina St', '103', '81'))
    human7.set_work(Address('Russia', 'Ekaterinburg', 'Mira St', '26', '11'))
    human7.set_number()
    human5.add_kid(human3)
    human5.add_kid(human7)
    human6.add_kid(human3)
    human6.add_kid(human7)
    book.append(human5)
    book.append(human6)
    book.append(human7)

    out = open('Book.txt', 'wt')
    for human in book:
        print human.to_file_string()
        out.write(human.to_file_string())


def main():
    book = Book()
    book.load_from_file('Book.txt')
    book.sort('middle')
    # book.del_person('John', 'Doe')
    # book.print_by_address(['USA', 'New York'])
    # book.print_all(['first', 'middle', 'last', 'birthday', 'phone', 'spouse', 'kids', 'home', 'work'])
    out = open('book.txt', 'wt')
    book.save_to_file(out)
    create_socket(book)


def create_socket(book):
    book.sort('first')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', 33322)
    sock.bind(server_address)
    sock.listen(5)
    while True:
        connection, client_address = sock.accept()
        request = connection.recv(1024)
        if request[:3] == 'GET':
            link = request.split()[1]
            urlparse_result = urlparse.urlparse(link)
            if urlparse_result.path == '/favicon.ico':
                process_favicon(connection)
                connection.close()
                continue
            result = urlparse.parse_qs(urlparse_result.query)
            process(book, connection, result)
        connection.close()


def process_favicon(connection):
    with open('favicon.ico', 'r') as icon_file:
        icon = icon_file.read()
        connection.sendall('HTTP/1.1 200 OK\r\n\r\n' + icon)


def process(book, connection, query):
    if not query:
        create_index(book, connection)
    elif 'add_person' in query:
        create_add(connection)
    elif 'cancel' in query:
        create_index(book, connection)
    elif 'confirm_add' in query:
        confirm_add(book, query)
        create_index(book, connection)
    elif 'personal' in query:
        create_personal(book, query['personal'][0], connection)
    elif 'personal_ok' in query:
        create_index(book, connection)
    elif 'del_person' in query:
        create_del(book, connection)
    elif 'confirm_del' in query:
        delete_person(book, query)
        create_index(book, connection)
    elif 'edit' in query:
        edit_personal(book, query['edit'][0], connection)
    elif 'confirm_edit' in query:
        confirm_edit(book, query)
        create_index(book, connection)


def create_index(book, connection):
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    style = html.Element('<style>', 'ul {list-style-type: none; text-align:center;}')
    index = html.Element('<html>', str(html.header('Address Book', style) + str(html.index(book))))
    connection.sendall(doctype + str(index))


def create_add(connection):
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    style = html.Element('<style>', 'sup {color: red}')
    add = html.Element('<html>', str(html.header('Add Person', style) + str(html.add_and_edit('add'))))
    connection.sendall(doctype + str(add))


def confirm_add(book, query):
    bday = query['birthday'][0].split(', ')
    human = Person()
    human.create_from_name_and_birthday(query['first'][0], query['last'][0],
                                        Date(int(bday[0]), int(bday[1]), int(bday[2])))
    if 'middle' in query:
        human.set_middle_name(query['middle'][0])
    if 'phone' in query:
        human.set_phone(query['phone'][0])
    if 'home' in query:
        home_address = query['home'][0].split(', ')
        human.set_home(', '.join(home_address))
    if 'work' in query:
        work_address = query['work'][0].split(', ')
        human.set_work(', '.join(work_address))
    if 'spouse' in query:
        spouse = query['spouse'][0].split(' ')
        human.set_spouse(book.find_person_by_name(spouse[0], spouse[1]))
    if 'kids' in query:
        kids = query['kids'][0].split(', ')
        for i in kids:
            kid_name = i.split(' ')
            human.add_kid(book.find_person_by_name(kid_name[0], kid_name[1]))
    book.addrbook.append(human)


def create_del(book, connection):
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    style = html.Element('<style>', 'ul {list-style-type: none; text-align:left;}')
    delete = html.Element('<html>', str(html.header('Delete Person', style) + str(html.delete(book))))
    connection.sendall(doctype + str(delete))


def delete_person(book, query):
    for person in query:
        if person[:4] == 'del_':
            name = person[4:].split('_')
            book.del_person(name[0], name[1])


def create_personal(book, person_name, connection):
    name_parse = person_name.split('_')
    name = name_parse[0] + ' ' + name_parse[1]
    person = book.find_person_by_name(name_parse[0], name_parse[1])
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    personal = html.Element('<html>', str(html.header(name) + str(html.personal(person))))
    connection.sendall(doctype + str(personal))


def edit_personal(book, person_name, connection):
    name_parse = person_name.split('_')
    name = name_parse[0] + ' ' + name_parse[1]
    person = book.find_person_by_name(name_parse[0], name_parse[1])
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    style = html.Element('<style>', 'sup {color: red}')
    edit = html.Element('<html>', str(html.header('Edit ' + name, style) + str(html.add_and_edit('edit', person))))
    connection.sendall(doctype + str(edit))


def confirm_edit(book, query):
    name = query['original'][0].split('_')
    person = book.find_person_by_name(name[0], name[1])
    bday = query['birthday'][0].split(', ')

    person.first = query['first'][0]
    person.last = query['last'][0]
    person.birthday = Date(int(bday[0]), int(bday[1]), int(bday[2]))

    if 'middle' in query:
        person.middle = query['middle'][0]
    else:
        person.middle = None

    if 'phone' in query:
        person.phone = query['phone'][0]
    else:
        person.phone = None

    if 'spouse' in query:
        spouse_name = query['spouse'][0].split(' ')
        spouse = book.find_person_by_name(spouse_name[0], spouse_name[1])
        person.spouse = spouse
    else:
        person.spouse = None

    if 'kids' in query:
        person.kids = []
        for i in query['kids']:
            kid_full = i.split(', ')
            for j in kid_full:
                kid_name = j.split(' ')
                kid = book.find_person_by_name(kid_name[0], kid_name[1])
                person.kids.append(kid)
    else:
        person.kids = []

    if 'home' in query:
        home_addr = []
        home_addr_parse = query['home'][0].split(', ')
        for k in home_addr_parse:
            home_addr.append(k)
        current_home_addr = Address()
        current_home_addr.props = home_addr
        person.home = current_home_addr
    else:
        person.home = None

    if 'work' in query:
        work_addr = []
        work_addr_parse = query['work'][0].split(', ')
        for l in work_addr_parse:
            work_addr.append(l)
        current_work_addr = Address()
        current_work_addr.props = work_addr
        person.work = current_work_addr
    else:
        person.work = None


# creation()
if __name__ == '__main__':
    main()