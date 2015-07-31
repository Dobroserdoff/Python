import unpack, xml.etree.ElementTree as ET
from unittest import TestCase


class TestUnpack(TestCase):

    def test_001(self):
        self.do_test('meta1.xml', 'meta1.json')

    def do_test(self, xml_path, json_path):
        tree = ET.ElementTree(file=xml_path)
        root = tree.getroot()
        result_produced = unpack.parse_book_xml(ET.tostring(root))
        print result_produced
        json_expected = open(json_path)
        result_expected = ''
        for line in json_expected:
            result_expected += line
        print result_expected
        self.assertEqual(result_produced, result_expected)
