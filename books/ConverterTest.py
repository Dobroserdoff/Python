# -*- coding: UTF-8 -*-

import os
import unittest

import Converter


class TestConverter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tests_dir = os.path.join(os.path.dirname(__file__), 'Test')

    def get_path(self, filename):
        return os.path.join(self.tests_dir, filename)

    def test_titles(self):
        metadata = Converter.metadata_list(self.get_path('meta1.xml'))
        titles = metadata['title']
        expected = [u'Человек в футляре (Сборник)', u'Человек в футляре']
        self.assertEqual(expected, titles)

    def test_titles_namespace(self):
        metadata = Converter.metadata_list(self.get_path('meta2.xml'))
        titles = metadata['title']
        expected = [u'Человек в футляре (Сборник)', u'Человек в футляре']
        self.assertEqual(expected, titles)


if __name__ == '__main__':
    unittest.main()
