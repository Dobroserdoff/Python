from unittest import TestCase
import obj

__author__ = 'somov'


class TestAddress(TestCase):
    def test_match(self):
        addr = obj.Address('Russia', 'Moscow', 'Tolstogo', '16')

        request = ['Russia']
        self.assertTrue(addr.match(request))

        request = ['Russia', 'Moscow']
        self.assertTrue(addr.match(request))

        request = ['Russia', 'Moscow', 'Tolstogo', '16']
        self.assertTrue(addr.match(request))

        request = ['Russia', 'Moscow', 'Tolstogo', '16', '52']
        self.assertFalse(addr.match(request))

        request = ['Russia', 'Moscow', None, '16']
        self.assertFalse(addr.match(request))