import pack
import unpack
import epub
import xml.etree.ElementTree as ET
from unittest import TestCase


class TestEpub(TestCase):
    def test_epub_001(self):
        self.do_epub_test('meta3.xml', 'new_meta3_no_cover_images.xml', ['images/cover.jpg'], lambda descr: descr.remove_cover_images(), dscr=False)

    def test_epub_002(self):
        self.do_epub_test('meta3.xml', 'new_meta3_no_cover_pages.xml', ['cover.xhtml'], lambda descr: descr.remove_cover_pages(), dscr=True)

    def test_epub_003(self):
        expected_fonts = ['fonts/LiberationSerif-Regular.ttf', 'fonts/LiberationSerif-Italic.ttf', 'fonts/LiberationSerif-Bold.ttf', 'fonts/LiberationSerif-BoldItalic.ttf']
        self.do_epub_test('meta3.xml', 'new_meta3_no_fonts.xml', expected_fonts, lambda descr: descr.remove_fonts(), dscr=True)

    def do_epub_test(self, xml_path_to_work_with, xml_path_to_expect_from, expected_filepaths, test_function, dscr):
        produced_tree = ET.ElementTree(file=xml_path_to_work_with)
        produced_root = produced_tree.getroot()
        for elem in produced_root:
            if elem.tag == u'{http://www.idpf.org/2007/opf}metadata':
                metadata = elem

        test_dscr = epub.BookDescr()
        file_to_work_with = open(xml_path_to_work_with)
        str_to_work_with = file_to_work_with.read()
        test_dscr.load(str_to_work_with)

        test_meta = epub.Metadata(metadata, test_dscr)

        if dscr:
            produced_filepaths = test_function(test_dscr)
        else:
            produced_filepaths = test_function(test_meta)

        expected_tree = ET.ElementTree(file=xml_path_to_expect_from)
        expected_root = expected_tree.getroot()
        str_to_expect_from = ET.tostring(expected_root, 'utf-8')

        self.assertEqual(test_dscr.save(), str_to_expect_from)
        self.assertEqual(produced_filepaths, expected_filepaths)


class TestUnpack(TestCase):
    def test_unpack_001(self):
        self.do_unpack_test('meta3.xml', 'meta1.json')

    def do_unpack_test(self, xml_path, json_path):
        tree = ET.ElementTree(file=xml_path)
        root = tree.getroot()
        result_produced = unpack.parse_book_xml(ET.tostring(root))
        json_file = open(json_path)
        try:
            result_expected = json_file.read()
        finally:
            json_file.close()
        self.assertEqual(result_produced, result_expected)


# TestPack works properly only with DEBUG=True in pack.py


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
