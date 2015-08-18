import pack
import unpack
import epub
from xml.etree import ElementTree
from unittest import TestCase


class TestEpub(TestCase):
    def test_bookdescr_remove_images(self):
        test_function = lambda descr, meta: descr.remove_cover_images()
        self.do_bookdescr_test('meta3.xml', 'new_meta3_no_cover_images.xml', ['images/cover.jpg'], test_function)

    def test_bookdescr_remove_pages(self):
        test_function = lambda descr, meta: descr.remove_cover_pages()
        self.do_bookdescr_test('meta3.xml', 'new_meta3_no_cover_pages.xml', ['cover.xhtml'], test_function)

    def test_bookdescr_remove_fonts(self):
        test_function = lambda descr, meta: descr.remove_fonts()
        expected_fonts = ['fonts/LiberationSerif-Regular.ttf', 'fonts/LiberationSerif-Italic.ttf', 'fonts/LiberationSerif-Bold.ttf', 'fonts/LiberationSerif-BoldItalic.ttf']
        self.do_bookdescr_test('meta3.xml', 'new_meta3_no_fonts.xml', expected_fonts, test_function)

    def do_bookdescr_test(self, xml_path_to_work_with, xml_path_to_expect_from, expected_filepaths, test_function):
        descr = epub.BookDescr()
        descr.load(read_file(xml_path_to_work_with))

        produced_filepaths = test_function(descr, descr.get_metadata())

        str_to_expect_from = format_xml_str(read_file(xml_path_to_expect_from))

        self.assertEqual(descr.save(), str_to_expect_from)
        self.assertEqual(produced_filepaths, expected_filepaths)

    def test_book_load(self):
        book = epub.Book()
        book.load('../geroi_nashego_vremeni.epub')
        produced = book.get_descr().save()
        expected = read_file('meta4.xml')
        self.assertEqual(produced, expected)

    def test_book_save(self):
        book_001 = epub.Book()
        book_001.load('../geroi_nashego_vremeni.epub')
        book_001.save('book_save_test.epub')
        book_002 = epub.Book()
        book_002.load('book_save_test.epub')
        produced = book_002.get_descr().save()
        expected = read_file('new_meta4.xml')
        self.assertEqual(produced, expected)


def format_xml_str(expected_xml):
    expected_tree = ElementTree.fromstring(expected_xml)
    return ElementTree.tostring(expected_tree, 'utf-8')


def read_file(path):
    file_ = open(path)
    try:
        return file_.read()
    finally:
        file_.close()


class TestUnpack(TestCase):
    def test_unpack_001(self):
        self.do_unpack_test('meta3.xml', 'meta1.json')

    def do_unpack_test(self, xml_path, json_path):
        tree = ElementTree.ElementTree(file=xml_path)
        root = tree.getroot()
        result_produced = unpack.parse_book_xml(ElementTree.tostring(root))
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
        tree = ElementTree.ElementTree(file=old_path)
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
        result_produced, remove_list = pack.make_book_xml(ElementTree.tostring(root), json_str)

        new_file = open(new_path)
        try:
            result_expected = new_file.read()
        finally:
            new_file.close()
        self.assertEqual(result_produced, result_expected)

    def remove_lists_comparison(self, old_path, json_path, expected_remove_list):
        tree = ElementTree.ElementTree(file=old_path)
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
        result_produced, produced_remove_list = pack.make_book_xml(ElementTree.tostring(root), json_str)
        self.assertEqual(produced_remove_list, expected_remove_list)