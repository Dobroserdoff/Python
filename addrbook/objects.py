class Date(object):
    def __init__(self, year, month, day):
        # self.year = year
        # self.month = month
        # self.day = day
        self.days_from_beginning = year * 10000 + month * 100 + day

    def get_year(self):
        return self.days_from_beginning / 10000

    def get_month(self):
        return (self.days_from_beginning % 10000) / 100

    def get_day(self):
        return self.days_from_beginning % 100

    def to_string(self):
        return '%s-%s-%s' % (self.get_year(), self.get_month(), self.get_day())

    def compare(self, other_date):
        # self.was_compared = True
        if self.get_year() < other_date.get_year():
            return -1
        if self.get_year() > other_date.get_year():
            return 1
        if self.get_month() < other_date.get_month():
            return -1
        if self.get_month() > other_date.get_month():
            return 1
        if self.get_day() < other_date.get_day():
            return -1
        if self.get_day() > other_date.get_day():
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


class RichText(Text):
    def __init__(self, s):
        self.s = s.replace('$', '$$')

    def to_string(self):
        return '[%s]' % self.s


class Human(object):
    def __init__(self):
        self.fields = [None, None, None, None, None]  # first, middle, last, birthday, phone

    def create_from_name_and_birthday(self, first_name, last_name, birthday):
        self.fields[0] = Text(first_name)
        self.fields[2] = Text(last_name)
        self.fields[3] = birthday

    def create_from_file_string(self):
        pass

    def to_file_string(self):
        """ create string for storing in file
            returns string
        """
        pass

    def compare(self, other_human, sort_field='first'):
        """ compare us with other human using specified sort_field
            sort_fields is string with field name
        """
        my_field_value = self.get_field_by_name(sort_field)
        other_field_value = other_human.get_field_by_name(sort_field)

        if my_field_value is None:
            if other_field_value is None:
                return 0
            return -1

        if other_field_value is None:
            return 1

        return my_field_value.compare(other_field_value)


    def get_field_by_name(self, field_name):
        if field_name == 'first':
            return self.fields[0]
        if field_name == 'middle':
            return self.fields[1]
        if field_name == 'last':
            return self.fields[2]
        if field_name == 'birthday':
            return self.fields[3]
        if field_name == 'phone':
            return self.fields[4]

        return None

    def to_string(self, print_fields=None):
        """ create pretty string for printing
            print_fields is array with names as strings
            :return: str
        """

        result = ''
        first = True

        if print_fields is None:
            print_fields = ['first', 'middle', 'last', 'birthday', 'phone']

        for print_field in print_fields:
            field_value = self.get_field_by_name(print_field)

            if field_value is None:
                continue

            if first:
                first = False
            else:
                result += ' '

            result += field_value.to_string()

        return result

    def set_middle_name(self, name):
        self.fields[1] = Text(name)

    def set_phone(self, phone):
        self.fields[4] = Text(phone)


class Book(object):
    def __init__(self):
        pass

    def load_from_file(self, filename):
        # self.humans = [...]
        pass

    def save_to_file(self, filename):
        pass

    def sort(self, field_names):
        pass

    def print_all(self, field_names):
        pass


def compare(o1, o2):
    # print 'Compare %s %s' % (o1.to_string(), o2.to_string())
    return o1.compare(o2)


def main():
    human = Human()
    human.create_from_name_and_birthday('John', 'Doe', Date(1970, 11, 3))

    # print human.to_string()

    human.set_middle_name('Junior')

    human.to_string()
    # print human.to_string()

    human.set_phone('003')
    # print human.to_string(['birthday', 'phone', 'first'])

    human2 = Human()
    human2.create_from_name_and_birthday('Jane', 'Doe', Date(1975, 2, 4))

    human3 = Human()
    human3.create_from_name_and_birthday('Ivan', 'Morozoff', Date(1950, 8, 4))
    humans = [human, human2, human3]

    my_compare = lambda o1, o2: o1.compare(o2, 'birthday')

    humans.sort(cmp=my_compare)

    for h in humans:
        print h.to_string(['birthday', 'first', 'last', 'phone', 'middle'])


def main2():
    t1 = Text("1")
    print t1.to_string()
    t2 = Text("0")

    x = str(None)
    print x.lower()
    print ord(x[0])

    x = Date(2014, 10, 9)
    # x.year += 1

    # array = [Text("x"), Text("y"), Text("a"), RichText('1000$')]

    array = [Date(2014, 10, 9), Date(2015, 1, 1), Date(1812, 12, 12)]

    for item in array:
        print item.to_string()
    print

    array.sort(cmp=compare)

    for item in array:
        print item.to_string()

main()
main2()