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
        self.root = ET.parse(xml_str)

    def save(self):
        return ET.tostring(self.root)

    def remove_cover_pages(self):
        """
        Removes cover pages elements
        Returns file paths
        """
        return self.remove_items_by_guide_type(u'cover')

    def remove_cover_images(self):
        """
        Removes cover images elements
        Return file paths
        """
        return self.remove_items_by_metadata_name(u'cover')

    def remove_fonts(self):
        """
        Removes fonts elements
        Return file paths
        """
        return self.remove_items_by_manifest_mediatype(u'application/x-font-ttf')

    # Common operations

    def find_elements_by_attr(self, parent, tag_name, attr_name, attr_value):
        return self.filter_elements_by_attr(self.find_elements_by_attr(parent, tag_name), attr_name, attr_value)

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

    def get_metadata_element(self):
        for elem in self.root:
            if elem.tag == u'metadata':
                return elem

    def find_metadata_items_by_name(self, name_):
        """
        Finds metadata item by its name
        Returns element
        """
        return self.find_elements_by_attr(self.get_metadata_element(), u'{http://www.idpf.org/2007/opf}item', u'name', name_)

    def remove_items_by_metadata_name(self, name_):
        """
        Removes items from everywhere finding them in metadata by name.
        Returns filepaths from removed items.
        """
        metadata = self.get_metadata_element()

        items = self.find_metadata_items_by_name(name_)

        ids = [item.attrib[u'content'] for item in items]

        for item in items:
            metadata.remove(item)

        return self.remove_manifest_items(ids)

    # Manifest operations

    def get_manifest_element(self):
        for elem in self.root:
            if elem.tag == u'manifest':
                return elem

    def find_manifest_item(self, id_):
        return self.find_element_by_attr(self.get_manifest_element(), u'{http://www.idpf.org/2007/opf}metadata', u'id', id_)

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
            if elem.tag == u'spine':
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
            if elem.tag == u'guide':
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