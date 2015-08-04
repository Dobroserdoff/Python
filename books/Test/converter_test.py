import pack
import unpack
import xml.etree.ElementTree as ET
from unittest import TestCase


class TestUnpack(TestCase):

    def test_unpack_001(self):
        self.do_unpack_test('meta3.xml', 'meta1.json')

    def do_unpack_test(self, xml_path, json_path):
        tree = ET.ElementTree(file=xml_path)
        root = tree.getroot()
        result_produced = unpack.parse_book_xml(ET.tostring(root))
        print result_produced
        json_file = open(json_path)
        try:
            result_expected = json_file.read()
        finally:
            json_file.close()
        print result_expected
        self.assertEqual(result_produced, result_expected)


#TestPack works properly only with DEBUG=True in pack.py


class TestPack(TestCase):

    def test_pack_001(self):
        self.final_files_comparison('meta2.xml', 'meta2.json', 'new_meta2.xml')

    def test_pack_002(self):
        expected_remove_list = ['images/cover.jpg', 'cover.xhtml', 'fonts/LiberationSerif-Regular.ttf',
                                'fonts/LiberationSerif-Italic.ttf', 'fonts/LiberationSerif-Bold.ttf',
                                'fonts/LiberationSerif-BoldItalic.ttf']
        self.remove_lists_comparison('meta2.xml', 'meta2.json', expected_remove_list)

    def final_files_comparison(self, old_path, json_path, new_path):
        tree = ET.ElementTree(file=old_path)
        root = tree.getroot()

        for piece in root:
            if 'metadata' in piece.tag:
                for elem in list(piece):
                    if 'identifier' in elem.tag:
                        piece.remove(elem)

        json_file = open(json_path)
        try:
            json_str = json_file.read()
        finally:
            json_file.close()
        result_produced, remove_list = pack.make_book_xml(ET.tostring(root), json_str)

        new_file = open(new_path)
        try:
            result_expected = new_file.read()
        finally:
            new_file.close()
        self.assertEqual(result_produced, result_expected)

    def remove_lists_comparison(self, old_path, json_path, expected_remove_list):
        tree = ET.ElementTree(file=old_path)
        root = tree.getroot()

        for piece in root:
            if 'metadata' in piece.tag:
                for elem in list(piece):
                    if 'identifier' in elem.tag:
                        piece.remove(elem)

        json_file = open(json_path)
        try:
            json_str = json_file.read()
        finally:
            json_file.close()
        result_produced, produced_remove_list = pack.make_book_xml(ET.tostring(root), json_str)
        self.assertEqual(produced_remove_list, expected_remove_list)
