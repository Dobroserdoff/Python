import os
import uuid
import sys
import json
import epub
import zipfile
import xml.etree.ElementTree as ET

DEBUG = True


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        patch = sys.argv[2]
    else:
        filename = 'chelovek_v_futlyare_sbornik_.epub'
        patch = 'testbook.json'

    epub_zip = zipfile.ZipFile(filename)

    try:
        content = epub.find_content(epub_zip.open('META-INF/container.xml'))
        content_dir = os.path.dirname(content)
        new_xml_string, paths_to_delete, css_path = make_book_xml(epub_zip.read(content), epub.read_file(patch), content_dir)
        new_css_str = clean_css(epub_zip.read(content_dir + '/' + css_path))

        if len(sys.argv) > 3:
            final_epub = zipfile.ZipFile(sys.argv[3], mode='w')
        else:
            final_epub = zipfile.ZipFile('new_' + filename, mode='w')

        try:
            for unit in epub_zip.namelist():
                if unit[-1] != '/':
                    if unit not in paths_to_delete:
                        transfer = epub_zip.read(unit)
                        if unit[-11:] == 'Content.opf':
                            transfer = new_xml_string
                        elif unit[-8:] == 'main.css':
                            transfer = new_css_str
                        final_epub.writestr(unit, transfer)
        finally:
            final_epub.close()

    finally:
        epub_zip.close()


def safe_main():
    try:
        main()
    except Exception as e:
        print >> sys.stderr, 'Error occured', e
        sys.exit(1)

    sys.exit(0)


def make_book_xml(old_xml_str, json_str, content_dir=None):
    root = ET.fromstring(old_xml_str)
    patch = json.loads(json_str)
    metadata = elem_constr(patch)
    add_content, cover_path, css_path = metadata_uncover(root)
    fix_add, xhtml_path, fonts_paths = fix_add_content(add_content)
    new_xml_str = output(metadata, fix_add)

    files_to_delete = [cover_path]
    if xhtml_path: files_to_delete.append(xhtml_path)
    for item in fonts_paths:
        files_to_delete.append(item)

    if content_dir:
        paths_to_delete = []
        for unit in files_to_delete:
            paths_to_delete.append(content_dir + '/' + unit)
        return new_xml_str, paths_to_delete, css_path
    else:
        return new_xml_str, files_to_delete, css_path


def metadata_uncover(root):
    add_content = []
    metas = []
    cover_path = 'images/cover.jpg'

    for child in root:
        if child.tag == '{http://www.idpf.org/2007/opf}metadata':
            for piece in child:
                if 'meta' in piece.tag:
                    meta = piece
                    metas.append(meta)

        elif 'manifest' in child.tag:
            for elem in list(child):
                for item in metas:
                    if elem.attrib['id'] == item.attrib['content']:
                        cover_path = elem.attrib['href']
                        child.remove(elem)

                if elem.attrib['media-type'] == 'text/css':
                    css_path = elem.attrib['href']

            add_content.append(child)
        else:
            add_content.append(child)

    return add_content, cover_path, css_path


def clean_css(css_str):
    while '@font-face' in css_str:
        fontface = css_str.find('@font-face')
        facecut = css_str[fontface:].find('}')
        css_str = css_str[facecut+3:]
    while 'font-family' in css_str:
        fontfamily = css_str.find('font-family')
        familycut = css_str[fontfamily:].find(';\n') + fontfamily
        first_part = css_str[:fontfamily]
        second_part = css_str[familycut+2:]
        css_str = first_part + second_part
    return css_str


def fix_add_content(content):
    guide_uncover, cover = guide(content)
    manifest_uncover, xhtml_path, fonts_paths = manifest(guide_uncover, cover)
    add_content = spine(manifest_uncover, cover)
    return add_content, xhtml_path, fonts_paths


def guide(content):
    cover = {}
    for piece in content:
        if 'guide' in piece.tag:
            for elem in list(piece):
                if elem.attrib['type'] == 'cover':
                    cover.update({'title': elem.attrib['title']})
                    piece.remove(elem)
    return content, cover


def manifest(content, cover):
    fonts_paths = []
    xhtml_path = None
    for piece in content:
        if 'manifest' in piece.tag:
            for elem in list(piece):

                if elem.attrib['media-type'] == 'application/x-font-ttf':
                    fonts_paths.append(elem.attrib['href'])
                    piece.remove(elem)

                elif elem.attrib['id'] == cover['title']:
                    xhtml_path = elem.attrib['href']
                    piece.remove(elem)

    return content, xhtml_path, fonts_paths


def spine(content, cover):
    for piece in content:
        if 'spine' in piece.tag:
            for elem in list(piece):
                if elem.attrib['idref'] == cover['title']:
                    piece.remove(elem)
    return content


def elem_constr(metajson):
    metadata = ET.Element(u'metadata')
    metadata.attrib = {u'xmlns': u'http://www.idpf.org/2007/opf', u'xmlns:dc': u'http://purl.org/dc/elements/1.1/'}
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
        metadata.append(element)
    if not DEBUG:
        identifier = ET.SubElement(metadata, u'dc:identifier', {u'id': u'Zero'})
        identifier.text = unicode(uuid.uuid4())
    return metadata


def output(metadata, add_content):
    result = '<?xml version="1.0"?>\n'

    package = ET.Element(u'package')
    package.attrib = {u'version': u'2.0', u'xmlns': u'http://www.idpf.org/2007/opf', u'unique-identifier': u'Zero'}
    package.append(metadata)

    for i in add_content:
        package.append(i)
    result += ET.tostring(package, encoding='utf-8')

    return result


if __name__ == '__main__':
    safe_main()
