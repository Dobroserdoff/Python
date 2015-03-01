# -*- coding: utf-8 -*-
class Date(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def to_string(self):
        """
        creates nice string of date to print
        :return: str
        """
        return '%s-%s-%s' % (self.year, self.month, self.day)

    def compare(self, other_date):
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


class Text(object):
    def __init__(self, s):
        self.s = s

    def to_string(self):
        return '%s' % self.s

    def compare(self, other_text):
        if self.s < other_text.s:
            return -1
        if self.s > other_text.s:
            return 1
        return 0


class Address(object):
    def __init__(self, country, city=None, street=None, building=None, apartment=None):
        # FIXME: Эти отдельные поля не используются вообще, и их можно убрать тогда (а вернуть, когда понадобятся).
        self.country = country
        self.city = city
        self.street = street
        self.building = building
        self.apartment = apartment
        self.props = [self.country, self.city, self.street, self.building, self.apartment]

    def to_string(self):
        addr = []
        for i in self.props:
            if i:
                addr.append(i)
        return ', '.join(addr)

    def match(self, request):
        addr = []
        for i in range(len(request)):
            # FIXME: Тут я так и не понял, зачем первая часть условия.
            if request[i] and request[i] == self.props[i]:
                addr.append(request[i])
        if len(addr) == len(request):
            return True

            # FIXME: Здесь надо возвращать False. Сейчас функция ничего не возвращает (то есть возвращает None),
            # FIXME: и это в условиях работает так же, как и False, но лучше False возвращать явно.


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

    def create_from_name_and_birthday(self, first_name, last_name, birthday):
        """
        creates a personal data to work with
        :param first_name:
        :param last_name:
        :param birthday:
        """
        self.first = Text(first_name)
        self.last = Text(last_name)
        self.birthday = birthday

    # FIXME: Это специальное ключевое слово, которое позволяет убрать параметр self, если он не используется в коде.
    # FIXME: Есть ещё несколько хитростей с ним, до которых мы доберёмся позже.
    @staticmethod
    # FIXME: Название метода, начинающеся с подчёркивания — общепринятое соглашение для «частных» (private) методов.
    # FIXME: Считается, что такие методы нельзя вызывать не из этого же класса. PyCharm такие неправильные вызовы
    # FIXME: будет подчёркивать.
    def _load_text(text):
        if text:
            return Text(text)
        else:
            return None

    def fill_from_file_string(self, line):
        """
        convert specified string of file into personal data to work with
        :type line: str
        """
        line = line.split('$')[:-1]
        # FIXME: Остальные места можно упростить аналогично.
        self.first = self._load_text(line[0])
        if line[1]:
            self.middle = Text(line[1])
        else:
            self.middle = None
        # FIXME: или есть такая же, но более короткая конструкция
        # self.last = Text(line[2]) if line[2] else None
        # FIXME: но лично мне отдельный метод нравится больше
        if line[2]:
            self.last = Text(line[2])
        else:
            self.last = None
        if line[3]:
            self.birthday = Date(line[3].split('-')[0], line[3].split('-')[1], line[3].split('-')[2])
        else:
            self.birthday = None
        if line[4]:
            self.phone = Text(line[4])
        else:
            self.phone = None
        if line[5]:
            self.spouse = Text(line[5])
        else:
            self.spouse = None
        if len(line[6]) > 0:
            for j in range(len(line[6].split('&'))):
                self.kids.append(Text(line[6].split('&')[j]))
        if line[7]:
            # FIXME: Вот это некрасиво и неэффективно. Нужно один раз сделать «parts = line[7].split», а потом писать
            # FIXME: parts[0], parts[1] и так далее.
            self.home = Address(line[7].split(', ')[0], line[7].split(', ')[1], line[7].split(', ')[2],
                                line[7].split(', ')[3], line[7].split(', ')[4])
        else:
            self.spouse = None
        if line[8]:
            self.work = Address(line[8].split(', ')[0], line[8].split(', ')[1], line[8].split(', ')[2],
                                line[8].split(', ')[3], line[8].split(', ')[4])
        else:
            self.work = None
        if line[9]:
            self.number = Text(line[9])
        else:
            self.number = None

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
                # FIXME: Проверка длины не нужна. И без такой проверки (и блока else) будет работать правильно.
                if len(self.kids) > 0:
                    for j in self.kids:
                        heritage.append(j.to_string(['number']))
                    result.append('&'.join(heritage))
                else:
                    result.append('')
            else:
                # FIXME: Аналогично одному из верхний примечаний можно:
                # result.append(prop_field.to_string() if prop_field else '')
                if prop_field:
                    result.append(prop_field.to_string())
                else:
                    result.append('')
        result.append('\n') # FIXME: А это зачем?
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

        return my_prop_value.compare(other_prop_value)

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
                for i in range(len(self.kids)):
                    result.append(self.kids[i])
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
                if self.kids:
                    for i in range(len(self.kids)):
                        if self.kids[i]:
                            result.append(self.kids[i].to_string(['first', 'last']))
                    continue

            prop_value = self.get_prop_by_name(print_prop_name)

            if prop_value is None:
                continue

            result.append(prop_value.to_string())
        return ' '.join(result)

    def set_middle_name(self, name):
        if name != 0:
            self.middle = Text(name)
        else:
            self.middle = None

    def set_phone(self, phone):
        if phone != 0:
            self.phone = Text(phone)
        else:
            self.phone = None

    def set_spouse(self, person):
        if person != 0:
            self.spouse = person
        else:
            self.spouse = None

    def add_kid(self, kid):
        self.kids.append(kid)

    def set_home(self, address):
        if address != 0:
            self.home = address
        else:
            self.home = None

    def set_work(self, address):
        if address != 0:
            self.work = address
        else:
            self.work = None

    def set_number(self):
        number = self.first.to_string()[0]
        if self.middle:
            number += self.middle.to_string()[0]
        number += self.last.to_string()[0]
        number += str(self.birthday.year) + str(self.birthday.month) + str(self.birthday.day)
        self.number = Text(number)

    def match(self, first, last):
        if first == self.first.to_string() and last == self.last.to_string():
            return True
        else:
            return False

    def match_number(self, request):
        if self.number.to_string() == request.to_string():
            return True
        else:
            return False

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

    def del_person(self, first, last):
        person = self.find_person_by_name(first, last)
        self.addrbook.remove(person)

    def print_all(self, prop_names=None):
        for person in self.addrbook:
            print person.to_string(prop_names)

    def print_by_address(self, request, print_props_names=None):
        for person in self.addrbook:
            if person.home and person.home.match(request) is True and \
                    person.work and person.work.match(request) is True:
                print (person.to_string(print_props_names) + ' Home & Work')
                break
            if person.home and person.home.match(request) is True:
                print (person.to_string(print_props_names) + ' Home')
            if person.work and person.work.match(request) is True:
                print (person.to_string(print_props_names) + ' Work')

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

    def find_person_by_name(self, first, last):
        """
        :param first name, last name:
        :rtype: Person
        """
        result = Person()
        for person in self.addrbook:
            if person.match(first, last):
                result = person
                break
            else:
                result = None
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
        # print human.to_string()
        out.write(human.to_file_string())


def main():
    book = Book()
    book.load_from_file('Book.txt')
    book.sort('middle')
    # book.del_person('Nicky', 'Devil')
    # book.print_by_address(['USA', 'New York'])
    book.print_all(['first', 'middle', 'last', 'birthday', 'phone', 'spouse', 'kids', 'home', 'work'])
    out = open('book.txt', 'wt')
    book.save_to_file(out)


if __name__ == '__main__':
    # creation()
    main()
