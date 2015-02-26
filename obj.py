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


class Human(object):
    def __init__(self):
        self.props = [None, None, None, None, None, None, [], None]
        # first, middle, last, birthday, phone, spouse, kids, number

    def create_from_name_and_birthday(self, first_name, last_name, birthday):
        """
        creates a personal data to work with
        :param first_name:
        :param last_name:
        :param birthday:
        """
        self.props[0] = Text(first_name)
        self.props[2] = Text(last_name)
        self.props[3] = birthday

    def fill_from_file_string(self, line):
        """
        convert specified string of file into personal data to work with
        :type line: str
        """
        line = line.split('$')[:-1]
        for i in range(len(line)):
            if line[i] == '':
                self.props[i] = None
            elif len(line[i].split('-')) > 1:
                self.props[i] = Date(line[i].split('-')[0], line[i].split('-')[1], line[i].split('-')[2])
            elif i == 6:
                for j in range(len(line[i].split('&'))):
                    self.props[i].append(Text(line[i].split('&')[j]))
            else:
                self.props[i] = Text(line[i])

    def to_file_string(self):
        """ return srt to store in file
        :rtype: str
        """
        result = []
        heritage = []
        for i in self.props:
            if i:
                if type(i) is list:
                    for j in range(len(i)):
                        if i[j]:
                            heritage.append(i[j].to_string(['number']))
                        else:
                            heritage.append('')
                    result.append('&'.join(heritage))
                elif type(i) is Human:
                    result.append(i.to_string(['number']))
                else:
                    result.append(i.to_string())
            else:
                result.append('')
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

        return my_prop_value.compare(other_prop_value)

    def get_prop_by_name(self, prop_name):
        """
        :param prop_name:
        :rtype: Text | Data | None
        """
        if prop_name == 'first':
            return self.props[0]
        if prop_name == 'middle':
            return self.props[1]
        if prop_name == 'last':
            return self.props[2]
        if prop_name == 'birthday':
            return self.props[3]
        if prop_name == 'phone':
            return self.props[4]
        if prop_name == 'spouse':
            return self.props[5]
        if prop_name == 'kids':
            result = []
            if self.props[6]:
                for i in range(len(self.props[6])):
                    result.append(self.props[6][i])
                return result
        if prop_name == 'number':
            return self.props[7]
        return None

    def to_string(self, print_props_names=None):
        """ create pretty string for printing
            print_props is array with names as strings
            :return: str
        """
        result = []

        if print_props_names is None:
            print_props_names = ['first', 'middle', 'last', 'birthday', 'phone', 'spouse', 'kids', 'number']

        for print_prop_name in print_props_names:
            if print_prop_name == 'spouse' and self.props[5]:
                result.append(self.props[5].to_string(['first', 'last']))
                continue

            if print_prop_name == 'kids':
                if self.props[6]:
                    for i in range(len(self.props[6])):
                        if self.props[6][i]:
                            result.append(self.props[6][i].to_string(['first', 'last']))
                    continue

            prop_value = self.get_prop_by_name(print_prop_name)

            if prop_value is None:
                continue

            result.append(prop_value.to_string())
        return ' '.join(result)

    def set_middle_name(self, name):
        if name != 0:
            self.props[1] = Text(name)
        else:
            self.props[1] = None

    def set_phone(self, phone):
        if phone != 0:
            self.props[4] = Text(phone)
        else:
            self.props[4] = None

    def set_spouse(self, person):
        if person != 0:
            self.props[5] = person
        else:
            self.props[5] = None

    def set_kids(self, kid):
        self.props[6].append(kid)

    def set_number(self):
        number = self.props[0].to_string()[0]
        if self.props[1]:
            number += self.props[1].to_string()[0]
        number += self.props[2].to_string()[0]
        number += str(self.props[3].year) + str(self.props[3].month) + str(self.props[3].day)
        self.props[7] = Text(number)

    def match(self, first, last):
        for i in self.props:
            if i and i.to_string() == first:
                for j in self.props:
                    if j and j.to_string() == last:
                        return True
            else:
                return False

    def match_number(self, number):
        if self.props[-1].to_string() == number.to_string():
            return True
        else:
            return False

    def spouse_kids_fix(self, book):
        if self.props[5]:
            self.props[5] = book.find_person_by_number(self.props[5])
        if self.props[6]:
            for i in range(len(self.props[6])):
                if self.props[6][i]:
                    self.props[6][i] = book.find_person_by_number(self.props[6][i])


class Book(object):
    def __init__(self):
        self.addrbook = []

    def set_numbers(self):
        for i in self.addrbook:
            i.set_number()

    def load_from_file(self, filename):
        my_file = open(filename)
        for line in my_file:
            human = Human()
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

    def find_person_by_number(self, number):
        """
        Returns human or None if not found
        :param number:
        :rtype: Human
        """
        result = Human()
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
        :rtype: Human
        """
        result = Human()
        for person in self.addrbook:
            if person.match(first, last):
                result = person
                break
            else:
                result = None
        return result


def creation():

    book = []
    human1 = Human()
    human1.create_from_name_and_birthday('John', 'Doe', Date(1970, 11, 3))
    human1.set_middle_name('Dead')
    human1.set_phone('8956')
    human1.set_number()

    human2 = Human()
    human2.create_from_name_and_birthday('Jane', 'Doe', Date(1975, 2, 4))
    human2.set_middle_name('Zombie')
    human2.set_phone('8031')
    human2.set_spouse(human1)
    human2.set_number()
    human1.set_spouse(human2)

    human3 = Human()
    human3.create_from_name_and_birthday('Ivan', 'Morozoff', Date(1950, 8, 4))
    human3.set_middle_name('Russian')
    human3.set_phone('9012')
    human3.set_number()
    book.append(human3)

    human4 = Human()
    human4.create_from_name_and_birthday('Nicky', 'Devil', Date(1666, 13, 13))
    human4.set_middle_name('Junior')
    human4.set_phone('1488')
    human4.set_number()
    human1.set_kids(human4)
    human2.set_kids(human4)
    book.append(human1)
    book.append(human2)
    book.append(human4)

    human5 = Human()
    human5.create_from_name_and_birthday('John', 'Snow', Date(1673, 05, 12))
    human5.set_middle_name('Bastard')
    human5.set_phone('4183')
    human5.set_number()

    human6 = Human()
    human6.create_from_name_and_birthday('Ygritte', 'Wild', Date(1676, 11, 28))
    human6.set_middle_name('Red')
    human6.set_phone('7913')
    human6.set_spouse(human5)
    human6.set_number()
    human5.set_spouse(human6)

    human7 = Human()
    human7.create_from_name_and_birthday('Olga', 'Petrova', Date(1754, 9, 14))
    human7.set_middle_name('Soviet')
    human7.set_phone('2462')
    human7.set_number()
    human5.set_kids(human3)
    human5.set_kids(human7)
    human6.set_kids(human3)
    human6.set_kids(human7)
    book.append(human5)
    book.append(human6)
    book.append(human7)

    out = open('Book.txt', 'wt')
    for human in book:
        out.write(human.to_file_string())


def main():

    book = Book()
    book.load_from_file('Book.txt')
    book.sort('middle')
    # book.del_person('Nicky', 'Devil')
    book.print_all(['first', 'middle', 'last', 'birthday', 'phone', 'spouse', 'kids'])
    out = open('book.txt', 'wt')
    book.save_to_file(out)

#creation()
main()