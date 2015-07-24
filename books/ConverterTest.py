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

    @staticmethod
    def find_meta(metadata, key):
        # FIXME: Why I must write this method myself? Why this functionality not in converter?
        result = []
        for metaitem in metadata:
            itemkey, value = TestConverter.decipher_metaitem(metaitem)
            if itemkey == key:
                result.append(value)
        return result

    @staticmethod
    def decipher_metaitem(metaitem):
        # FIXME: Why do I need this method at all?
        if len(metaitem) != 1:  # FIXME: Why this check?
            raise Exception()
        return metaitem.keys()[0], metaitem.values()[0]

    def test_titles(self):
        metadata = Converter.metadata_list(self.get_path('meta1.xml'))
        titles = TestConverter.find_meta(metadata, 'title')
        expected = [u'Человек в футляре (Сборник)', u'Человек в футляре']
        self.assertEqual(expected, titles)

    def test_titles_namespace(self):
        metadata = Converter.metadata_list(self.get_path('meta2.xml'))
        titles = TestConverter.find_meta(metadata, 'title')
        expected = [u'Человек в футляре (Сборник)', u'Человек в футляре']
        self.assertEqual(expected, titles)


if __name__ == '__main__':
    unittest.main()
