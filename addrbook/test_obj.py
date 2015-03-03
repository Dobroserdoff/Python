from unittest import TestCase
import obj


class TestAddress(TestCase):
    def test_match(self):
        addr = obj.Address()
        addr.props = ['Russia', 'Moscow', 'Tolstogo', '16', None]

        request = ['Russia']
        self.assertTrue(addr.match(request))

        request = ['Russia', 'Moscow']
        self.assertTrue(addr.match(request))

        request = ['Russia', 'Moscow', 'Tolstogo', '16']
        self.assertTrue(addr.match(request))

        request = ['Russia', 'Moscow', 'Tolstogo', '16', '52']
        self.assertFalse(addr.match(request))

        request = ['Russia', 'Moscow', '16']
        self.assertFalse(addr.match(request))

    def test_to_string(self):
        addr = obj.Address()
        addr.props = ['Russia', 'Moscow', 'Tolstogo', '16']
        self.assertEqual('Russia, Moscow, Tolstogo, 16', addr.to_string())

        addr.props = ['Russia', 'Moscow', None, '16']
        self.assertEqual('Russia, Moscow, 16', addr.to_string())


class TestPerson(TestCase):
    def test_create_from_name_and_birthday(self):
        person = obj.Person(obj.Text('Name'), obj.Text('Lastname'), obj.Date(1982, 12, 01))

        test_person = obj.Person()
        test_person.create_from_name_and_birthday('Name', 'Lastname', obj.Date(1982, 12, 01))
        self.assertEqual(person.to_string(), test_person.to_string())

    def test_fill_from_file_string(self):
        home = obj.Address()
        home.props = ['Russia', 'Moscow', 'Arbat St', '86', '101']
        work = obj.Address()
        work.props = ['Russia', 'Moscow', 'Novinsky Blvd', '22', '19']
        person = obj.Person(obj.Text('Ivan'), obj.Text('Russian'), obj.Text('Morozoff'), obj.Date(1950, 8, 4),
                            obj.Text('9012'), None, None, home, work)

        test_person = obj.Person()
        book = obj.Book()
        input_file = open('Book.txt')
        book.load_from_file('Book.txt')
        addr_book = []
        for string in input_file:
            test_person.fill_from_file_string(string)
            test_person.spouse_kids_fix(book)
            addr_book.append(test_person.to_string())
        self.assertIn(person.to_string(), addr_book)

    def test_to_file_string(self):
        book = obj.Book()
        book.load_from_file('Book.txt')
        human = obj.Person()
        human.create_from_name_and_birthday('Ygritte', 'Wild', obj.Date(1676, 11, 28))
        human.set_middle_name('Red')
        human.set_phone('7913')
        human.set_home(['Westeros', 'North', 'Wastelands', '123', '45'])
        human.set_spouse(book.find_person_by_name('John', 'Snow'))
        human.add_kid(book.find_person_by_name('Ivan', 'Morozoff'))
        human.add_kid(book.find_person_by_name('Olga', 'Petrova'))
        human.set_number()

        addr_book = open('Book.txt')
        self.assertIn(human.to_file_string(), addr_book)

    def test_compare(self):
        human = obj.Person()
        human.create_from_name_and_birthday('Nicky', 'Devil', obj.Date(1666, 13, 13))

        other_human = obj.Person()
        other_human.create_from_name_and_birthday('John', 'Snow', obj.Date(1673, 05, 12))

        self.assertEqual(human.compare(other_human), 1)
        self.assertEqual(human.compare(other_human, 'last'), -1)
        self.assertEqual(human.compare(other_human, 'middle'), 0)

    def test_to_string(self):
        person = 'Nicky Junior Devil 1666-13-13 1488 USA, New York, 5th Ave, 86, 101 USA, New York, 10th St, 120, 401'

        human = obj.Person()
        human.create_from_name_and_birthday('Nicky', 'Devil', obj.Date(1666, 13, 13))
        human.set_middle_name('Junior')
        human.set_phone('1488')
        human.set_home(['USA', 'New York', '5th Ave', '86', '101'])
        human.set_work(['USA', 'New York', '10th St', '120', '401'])
        self.assertEqual(person, human.to_string())

    def test_match(self):
        human = obj.Person()
        human.create_from_name_and_birthday('Ivan', 'Morozoff', obj.Date(1950, 8, 4))

        other_human = obj.Person()
        other_human.create_from_name_and_birthday('Olga', 'Petrova', obj.Date(1754, 9, 14))

        first = 'Ivan'
        last = 'Morozoff'
        self.assertTrue(human.match(first, last))
        self.assertFalse(other_human.match(first, last))

    def test_match_number(self):
        human = obj.Person()
        human.create_from_name_and_birthday('John', 'Snow', obj.Date(1673, 05, 12))
        human.set_middle_name('Bastard')
        human.set_number()

        other_human = obj.Person()
        other_human.create_from_name_and_birthday('John', 'Doe', obj.Date(1970, 11, 3))
        other_human.set_middle_name('Dead')
        other_human.set_number()

        request = obj.Text('JBS1673512')
        self.assertTrue(human.match_number(request))
        self.assertFalse(other_human.match_number(request))


class TestBook(TestCase):
    def test_load_from_file(self):
        human = obj.Person()
        human.create_from_name_and_birthday('Ivan', 'Morozoff', obj.Date(1950, 8, 4))

        book = obj.Book()
        book.load_from_file('Book.txt')
        book_print = []
        for i in range(len(book.addrbook)):
            book_print.append(book.addrbook[i].to_string(['first', 'last', 'birthday']))
        self.assertIn(human.to_string(), book_print)

    def test_del_person(self):
        book = obj.Book()
        book.load_from_file('Book.txt')
        book.del_person('John', 'Doe')
        book_print = []
        for i in range(len(book.addrbook)):
            book_print.append(book.addrbook[i].to_string(['first', 'last', 'birthday']))

        human = obj.Person()
        human.create_from_name_and_birthday('John', 'Doe', obj.Date(1970, 11, 3))
        self.assertNotIn(human.to_string(), book_print)

    def test_find_person_by_number(self):
        human = obj.Person()
        human.create_from_name_and_birthday('John', 'Snow', obj.Date(1673, 05, 12))
        human.set_middle_name('Bastard')
        human.set_number()

        book = obj.Book()
        book.load_from_file('Book.txt')
        other_human = book.find_person_by_number(human.number)
        self.assertEqual(human.to_string(), other_human.to_string(['first', 'middle', 'last', 'birthday']))

    def test_find_person_by_name(self):
        human = obj.Person()
        human.create_from_name_and_birthday('John', 'Snow', obj.Date(1673, 05, 12))

        book = obj.Book()
        book.load_from_file('Book.txt')
        other_human = book.find_person_by_name(human.first.to_string(), human.last.to_string())
        self.assertEqual(human.to_string(), other_human.to_string(['first', 'last', 'birthday']))
