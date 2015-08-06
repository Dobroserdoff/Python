import uuid
import json
from xml.etree import ElementTree as ET


def find_content(container):
    tree = ET.parse(container)
    root = tree.getroot()
    for child in root.iter():
        if 'full-path' in child.attrib:
            content = child.attrib['full-path']
            return content


def read_file(filepath, encoding='utf-8'):
    f = open(filepath)
    try:
        filedata = f.read()
        if encoding:
            return filedata.decode(encoding)
        else:
            return filedata
    finally:
        f.close()


class BookDescr(object):
    def __init__(self):
        self.root = None

    def load(self, xml_str):
        self.root = ET.fromstring(xml_str)

    def save(self):
        return ET.tostring(self.root, 'utf-8')

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

    # Common operations

    def find_elements_by_attr(self, parent, tag_name, attr_name, attr_value):
        return self.filter_elements_by_attr(self.find_elements_by_tag(parent, tag_name), attr_name, attr_value)

    def find_elements_by_tag(self, parent, tag_name):
        elements = []
        for elem in parent:
            if elem.tag == tag_name:
                elements.append(elem)
        return elements

    def filter_elements_by_attr(self, elements_to_filter, attr_name, attr_value):
        elements = []
        for elem in elements_to_filter:
            if elem.attrib[attr_name] == attr_value:
                elements.append(elem)
        return elements

    def find_element_by_attr(self, parent, tag_name, attr_name, attr_value):
        result = self.find_elements_by_attr(parent, tag_name, attr_name, attr_value)
        if len(result) == 0:
            raise Exception(u'Tag %s not found' % tag_name)
        if len(result) > 1:
            raise Exception(u'Found multiple %s tags' % tag_name)
        return result[0]

    # Metadata operations

    def get_metadata(self, element=False):
        for elem in self.root:
            if elem.tag == u'{http://www.idpf.org/2007/opf}metadata':
                if element:
                    return elem
                else:
                    metadata = Metadata(elem, self)
                    return metadata

    def set_metadata_element(self, new_metadata):
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
        return self.find_element_by_attr(self.get_manifest_element(), u'{http://www.idpf.org/2007/opf}item', u'id', id_)

    def find_manifest_items_by_media(self, mediatype):
        """
        Finds manifest items by mediatype
        Returns elements
        """
        return self.find_elements_by_attr(self.get_manifest_element(), u'{http://www.idpf.org/2007/opf}item', u'media-type', mediatype)

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
        manifest = self.get_manifest_element()

        items = self.find_manifest_items_by_media(mediatype_)

        ids = [item.attrib[u'id'] for item in items]

        return self.remove_manifest_items(ids)

    # Spine operations

    def get_spine_element(self):
        for elem in self.root:
            if elem.tag == u'{http://www.idpf.org/2007/opf}spine':
                return elem

    def find_spine_item(self, id_):
        return self.find_element_by_attr(self.get_spine_element(), u'{http://www.idpf.org/2007/opf}itemref', u'idref', id_)

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
        return self.find_elements_by_attr(self.get_guide_element(), u'{http://www.idpf.org/2007/opf}reference', u'type', type_)

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

    def remove_cover_images(self):
        """
        Removes cover images elements
        Return file paths
        """
        return self.remove_items_by_metadata_name(u'cover')

    def find_metadata_items_by_name(self, name_):
        """
        Finds metadata item by its name
        Returns element
        """
        return self.descr.find_elements_by_attr(self.descr.get_metadata(element=True), u'{http://www.idpf.org/2007/opf}meta', u'name', name_)

    def remove_items_by_metadata_name(self, name_):
        """
        Removes items from everywhere finding them in metadata by name.
        Returns filepaths from removed items.
        """
        metadata = self.descr.get_metadata(element=True)

        items = self.find_metadata_items_by_name(name_)

        ids = [item.attrib[u'content'] for item in items]

        for item in items:
            metadata.remove(item)

        return self.descr.remove_manifest_items(ids)

    def load_json(self, filepath):
        """
        :param filepath:
        :return: metadata element
        """
        metajson = json.loads(read_file(filepath))

        new_metadata = ET.Element(u'metadata')
        new_metadata.attrib = {u'xmlns': u'http://www.idpf.org/2007/opf', u'xmlns:dc': u'http://purl.org/dc/elements/1.1/'}

        for key in metajson:
            element = ET.Element(u'dc:' + key)
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

        identifier = ET.SubElement(new_metadata, u'dc:identifier', {u'id': u'Zero'})
        identifier.text = unicode(uuid.uuid4())

        self.descr.set_metadata_element(new_metadata)

"""
tree = ET.ElementTree(file='Test/meta1.xml')
root = tree.getroot()
a = BookDescr()
a.load(ET.tostring(root))
print a.get_metadata(element=True)
print a

b = Metadata(a.get_metadata(element=True), a)
print b.meta
print b.descr

b.descr.remove_cover_pages()
b.descr.remove_fonts()

print b.descr.get_metadata().remove_cover_images()
b.load_json('Test/meta1.json')

out = open('Test/test1.xml', 'w')
out.write(b.descr.save())
"""