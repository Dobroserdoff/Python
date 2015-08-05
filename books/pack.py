import os
import shutil
import subprocess
import uuid
import sys
import json
import epub
import xml.etree.ElementTree as ET

DEBUG = False


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        patch = sys.argv[2]
    else:
        filename = 'chelovek_v_futlyare_sbornik_.epub'
        patch = 'testbook.json'

    if os.path.isdir('temp/'):
        shutil.rmtree('temp/')
        os.mkdir('temp/')

    try:
        work_directory = 'temp'
        process(['unzip', filename, '-d' + work_directory])
        container_path = os.path.join(work_directory, 'META-INF', 'container.xml')
        metadata_path = os.path.join(work_directory, epub.find_content(container_path))
        files_directory = os.path.dirname(metadata_path)
        new_xml_string, files_to_delete = make_book_xml(epub.read_file(metadata_path, encoding=None), epub.read_file(patch))

        try:
            delete_files(files_to_delete, files_directory, work_directory)
        except Exception as e:
            print >> sys.stderr, 'Error occured: ', e

        out = open(metadata_path, 'w')
        try:
            out.write(new_xml_string)
        finally:
            out.close()

        process(['zip', '-r', '../temp', 'mimetype', 'META-INF', 'OEBPS'], cwd='temp/')

        if len(sys.argv) > 3:
            os.rename('temp.zip', sys.argv[3] + '.epub')
        else:
            os.rename('temp.zip', 'new_' + filename)

    finally:
        if not DEBUG:
            if os.path.isdir('temp/'):
                shutil.rmtree('temp/')


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


def make_book_xml(old_xml_str, json_str):
    root = ET.fromstring(old_xml_str)
    patch = json.loads(json_str)
    metadata = elem_constr(patch)
    add_content, cover_path = metadata_uncover(root)
    fix_add, xhtml_path, fonts_paths = fix_add_content(add_content)

    files_to_delete = [cover_path, xhtml_path]
    for item in fonts_paths:
        files_to_delete.append(item)

    new_xml_str = output(metadata, fix_add)
    return new_xml_str, files_to_delete


def metadata_uncover(root):
    add_content = []

    for child in root:
        if child.tag == '{http://www.idpf.org/2007/opf}metadata':
            for piece in child:
                if 'meta' in piece.tag:
                    meta = piece
        elif 'manifest' in child.tag:
            for elem in list(child):
                if elem.attrib['id'] == meta.attrib['content']:
                    cover_path = elem.attrib['href']
                    child.remove(elem)
            add_content.append(child)
        else:
            add_content.append(child)

    return add_content, cover_path


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


def delete_files(files_to_delete, files_directory, work_directory):
    for item in files_to_delete:
        os.remove(os.path.join(files_directory, item))
    list_of_files = list(os.walk(work_directory))
    for dirpath, dirnames, filenames in list_of_files:
        if len(filenames) == 0:
            try:
                os.rmdir(dirpath)
            except Exception as e:
                print >> sys.stderr, 'Error occured', e


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


def process(arg, cwd=None):
    proc = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = proc.communicate()
    returncode = proc.returncode
    if returncode != 0:
        raise Exception(err)


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
