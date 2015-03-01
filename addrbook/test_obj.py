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

