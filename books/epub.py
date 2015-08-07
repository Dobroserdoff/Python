import shutil
import uuid
import sys
import os
import json
import find_elements
import subprocess
import unpack
from xml.etree import ElementTree

DEBUG = False


def safe_main():
    if DEBUG:
        main()
        sys.exit(0)

    try:
        main()
    except Exception as e:
        print >> sys.stderr, 'Error occured', e
        sys.exit(1)

    sys.exit(0)


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        patch_out = sys.argv[2]
        patch_in = sys.argv[3]
    else:
        filename = 'geroi_nashego_vremeni.epub'
        patch_out = 'testbook_out.json'
        patch_in = 'testbook_in.json'

    try:
        book = Book()
        book.load('geroi_nashego_vremeni.epub')
        result_json = unpack.parse_book_xml(book.get_descr().save())

        out = open(patch_out, 'w')
        try:
            out.write(result_json)
        finally:
            out.close()

        book.clear()
        book.get_descr().get_metadata().load_json(patch_in)

        if len(sys.argv) > 4:
            book.save(sys.argv[4])
        else:
            book.save('new_' + filename)

    finally:
        if not DEBUG:
            book.close()


def find_content(container):
    """
    Looking through container file to find content file
    :return: Content file path
    """
    tree = ElementTree.parse(container)
    root = tree.getroot()
    for child in root.iter():
        if 'full-path' in child.attrib:
            content = child.attrib['full-path']
            return content


def read_file(filepath, encoding='utf-8'):
    """
    Read data from xml file
    :return: Unicode
    """
    f = open(filepath)
    try:
        filedata = f.read()
        if encoding:
            return filedata.decode(encoding)
        else:
            return filedata
    finally:
        f.close()


def process(arg, cwd=None):
    proc = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = proc.communicate()
    returncode = proc.returncode
    if returncode != 0:
        raise Exception(err)


def delete_files(delete_paths, files_directory, work_directory):
    for item in delete_paths:
        os.remove(os.path.join(files_directory, item))
    list_of_files = list(os.walk(work_directory))
    for dirpath, dirnames, filenames in list_of_files:
        if len(filenames) == 0:
            try:
                os.rmdir(dirpath)
            except Exception as e:
                print >> sys.stderr, 'Error occured', e


class BookDescr(object):
    def __init__(self):
        self.root = None

    def load(self, xml_str):
        self.root = ElementTree.fromstring(xml_str)

    def save(self):
        return ElementTree.tostring(self.root, 'utf-8')

    def remove_cover_images(self):
        """
        Removes cover images elements
        Return file paths
        """
        ids = self.get_metadata().remove_items_by_name(u'cover')
        return self.remove_manifest_items(ids)

    def remove_cover_pages(self):
        """
        Removes cover pages elements
        Returns file paths
        """
        return self.remove_items_by_guide_type(u'cover')

    def remove_fonts(self):
        """
        Removes fonts elements
        Return file paths
        """
        return self.remove_items_by_manifest_mediatype(u'application/x-font-ttf')

    # Metadata operations

    def get_metadata(self):
        for elem in self.root:
            if elem.tag == u'{http://www.idpf.org/2007/opf}metadata':
                metadata = Metadata(elem, self)
                return metadata

    def set_metadata_element(self, new_metadata):
        """
        Replace metadata with new_metadata content
        """
        for elem in list(self.root):
            if elem.tag == u'{http://www.idpf.org/2007/opf}metadata':
                self.root.remove(elem)
                self.root.insert(0, new_metadata)

    # Manifest operations

    def get_manifest_element(self):
        for elem in self.root:
            if elem.tag == u'{http://www.idpf.org/2007/opf}manifest':
                return elem

    def find_manifest_item(self, id_):
        return find_elements.one_by_attr(self.get_manifest_element(), u'{http://www.idpf.org/2007/opf}item', u'id', id_)

    def find_manifest_items_by_media(self, mediatype):
        """
        Finds manifest items by mediatype
        Returns elements
        """
        return find_elements.some_by_attr(self.get_manifest_element(), u'{http://www.idpf.org/2007/opf}item', u'media-type', mediatype)

    def remove_manifest_items(self, ids):
        """
        Removes manifest items by their ids
        Returns file paths from them
        """
        manifest = self.get_manifest_element()
        paths = []
        for id_ in ids:
            manifest_item = self.find_manifest_item(id_)
            paths.append(manifest_item.attrib[u'href'])
            manifest.remove(manifest_item)
        return paths

    def remove_items_by_manifest_mediatype(self, mediatype_):
        """
        Removes items from everywhere finding them in manifest by media-type.
        Returns filepaths from removed items.
        """
        items = self.find_manifest_items_by_media(mediatype_)

        ids = [item.attrib[u'id'] for item in items]

        return self.remove_manifest_items(ids)

    # Spine operations

    def get_spine_element(self):
        for elem in self.root:
            if elem.tag == u'{http://www.idpf.org/2007/opf}spine':
                return elem

    def find_spine_item(self, id_):
        return find_elements.one_by_attr(self.get_spine_element(), u'{http://www.idpf.org/2007/opf}itemref', u'idref', id_)

    def remove_spine_items(self, ids):
        spine = self.get_spine_element()
        for id_ in ids:
            spine.remove(self.find_spine_item(id_))

    # Guide operations

    def get_guide_element(self):
        for elem in self.root:
            if elem.tag == u'{http://www.idpf.org/2007/opf}guide':
                return elem

    def find_guide_items_by_type(self, type_):
        return find_elements.some_by_attr(self.get_guide_element(), u'{http://www.idpf.org/2007/opf}reference', u'type', type_)

    def remove_items_by_guide_type(self, type_):
        """
        Removes items from everywhere finding them in guide by type.
        Returns filepaths from removed items.
        """
        guide = self.get_guide_element()

        items = self.find_guide_items_by_type(type_)

        ids = [item.attrib[u'title'] for item in items]

        for item in items:
            guide.remove(item)

        self.remove_spine_items(ids)
        return self.remove_manifest_items(ids)


class Metadata(object):
    def __init__(self, meta, descr):
        if meta.tag == u'{http://www.idpf.org/2007/opf}metadata':
            self.meta = meta
        else:
            raise Exception(u'Unexpected element %s' % meta)
        if type(descr) is BookDescr:
            self.descr = descr
        else:
            raise Exception(u'Unexpected type of data %s' % type(descr))

    def find_items_by_name(self, name_):
        """
        Finds metadata item by its name
        Returns element
        """
        return find_elements.some_by_attr(self.meta, u'{http://www.idpf.org/2007/opf}meta', u'name', name_)

    def remove_items_by_name(self, name_):
        """
        Removes items from everywhere finding them in metadata by name.
        Returns filepaths from removed items.
        """
        metadata = self.meta

        items = self.find_items_by_name(name_)

        ids = [item.attrib[u'content'] for item in items]

        for item in items:
            metadata.remove(item)

        return ids

    def load_json(self, filepath):
        """
        Creates new metadata using data from .json file
        """
        metajson = json.loads(read_file(filepath))

        new_metadata = ElementTree.Element(u'metadata')
        new_metadata.attrib = {u'xmlns': u'http://www.idpf.org/2007/opf', u'xmlns:dc': u'http://purl.org/dc/elements/1.1/'}

        for key in metajson:
            element = ElementTree.Element(u'dc:' + key)
            if key == u'creator':
                for inner_key in metajson[key]:
                    if inner_key == u'display':
                        element.text = metajson[key][inner_key]
                    elif inner_key == u'sort':
                        element.attrib = {u'p6:file-as': metajson[key][inner_key],
                                          u'xmlns:p6': u'http://www.idpf.org/2007/opf'}
                    else:
                        raise Exception(u'Unexpected inner key %s' % key)

            else:
                element.text = unicode(metajson[key])
            new_metadata.append(element)

        identifier = ElementTree.SubElement(new_metadata, u'dc:identifier', {u'id': u'Zero'})
        identifier.text = unicode(uuid.uuid4())

        self.meta = new_metadata
        self.descr.set_metadata_element(new_metadata)


class Book(object):
    def __init__(self):
        self.path = str(uuid.uuid4()) + '/'
        self._descr = BookDescr()

    def load(self, filename):
        """
        Load data from file to Book object including self.descr instance method
        """
        os.mkdir(self.path)
        process(['unzip', filename, '-d', self.path])
        content_unicode = read_file(os.path.join(self.path, self.get_content_path()))
        self._descr.load(str(content_unicode.encode('utf-8')))

    def get_descr(self):
        return self._descr

    def save(self, filename):
        """
        Creates new .epub file
        """
        out = open(os.path.join(self.path, self.get_content_path()), 'w')
        try:
            out.write(self._descr.save())
        finally:
            out.close()
        process(['zip', '-r', '../' + self.path[:-1], 'mimetype', 'META-INF', 'OEBPS'], cwd=self.path)
        os.rename(self.path[:-1] + '.zip', filename)

    def clear(self):
        """
        Clear content and delete all unneccesary files inside Book folder
        """
        images_path = self.get_descr().remove_cover_images()
        pages_path = self.get_descr().remove_cover_pages()
        fonts_path = self.get_descr().remove_fonts()
        delete_paths = images_path + pages_path + fonts_path
        files_directory = os.path.dirname(os.path.join(self.path, self.get_content_path()))

        try:
            delete_files(delete_paths, files_directory, self.path)
        except Exception as e:
            print >> sys.stderr, 'Error occured: ', e

    def close(self):
        if os.path.isdir(self.path):
                shutil.rmtree(self.path)

    def get_content_path(self):
        """
        :return: Content file path
        """
        return find_content(os.path.join(self.path, 'META-INF', 'container.xml'))


if __name__ == '__main__':
    safe_main()
