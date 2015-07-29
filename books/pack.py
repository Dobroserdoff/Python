import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import Converter
import uuid

DEBUG = False


def main(filename, patch, output):
    path = str(uuid.uuid4())
    os.mkdir(path)

    try:
        process(['unzip', filename, '-d' + path])
        content = find_content(path + '/META-INF/container.xml')
        metadata_request = path + '/' + content
        step_one = Converter.metadata_list(metadata_request)
        step_two = Converter.id_clean(step_one, path)
        fix = metadata_content(step_two, patch)
        metadata = elem_constr(fix)
        add_content = metadata_uncover(metadata_request)
        fix_add = fix_add_content(add_content, metadata_request[:metadata_request.rfind('/')+1])
        result = Converter.output(metadata, fix_add)
        if os.path.exists(metadata_request[:metadata_request.rfind('/')+1] + 'fonts'):
            shutil.rmtree(metadata_request[:metadata_request.rfind('/')+1] + 'fonts')
        out = open(path + '/' + content, 'w')
        try:
            out.write(result)
        finally:
            out.close()
        process(['zip', '-r', '../' + path, 'mimetype', 'META-INF', 'OEBPS'], cwd=path)
        os.rename(path + '.zip', output + '.epub')
    finally:
        if not DEBUG:
            if os.path.isdir(path):
                shutil.rmtree(path)


def metadata_uncover(path):
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    add_content = []

    for child in root:
        if 'metadata' in child.tag:
            for piece in child:
                if 'meta' in piece.tag:
                    meta = piece
        elif 'manifest' in child.tag:
            for elem in list(child):
                if elem.attrib['id'] == meta.attrib['content']:
                    if os.path.exists(path[:path.rfind('/')+1] + elem.attrib['href']):
                        os.remove(path[:path.rfind('/')+1] + elem.attrib['href'])
                    child.remove(elem)
            add_content.append(child)
        else:
            add_content.append(child)

    return add_content


def fix_add_content(content, path):
    guide_uncover, cover = guide(content)
    manifest_uncover = manifest(guide_uncover, cover, path)
    add_content = spine(manifest_uncover, cover)
    return add_content


def guide(content):
    cover = {}
    for piece in content:
        if 'guide' in piece.tag:
            for elem in list(piece):
                if elem.attrib['type'] == 'cover':
                    cover.update({'title': elem.attrib['title']})
                    piece.remove(elem)
    return content, cover


def manifest(content, cover, path):
    for piece in content:
        if 'manifest' in piece.tag:
            for elem in list(piece):
                if elem.attrib['media-type'] == 'application/x-font-ttf':
                    piece.remove(elem)
                elif elem.attrib['id'] == cover['title']:
                    if os.path.exists(path + elem.attrib['href']):
                        os.remove(path + elem.attrib['href'])
                    piece.remove(elem)
    return content


def spine(content, cover):
    for piece in content:
        if 'spine' in piece.tag:
            for elem in list(piece):
                if elem.attrib['idref'] == cover['title']:
                    piece.remove(elem)
    return content


def elem_constr(result):
    elements = []
    for key in result:
        element = ET.Element('dc:' + key)
        if key == 'creator':
            for value in result[key]:
                if 'display' in value:
                    element.text = value[8:]
                else:
                    element.attrib = 'p6:file-as="' + value[5:] + '" xmlns:p6="http://www.idpf.org/2007/opf"'
        else:
            for value in result[key]:
                if key == 'identifier':
                    element.attrib = 'id="Zero"'
                element.text = value
        elements.append(element)
    return elements


def metadata_content(original, patch):
    tree = ET.parse(patch)
    root = tree.getroot()
    for child in root:
        if child.text:
            original[child.tag] = [child.text]
        else:
            original[child.tag] = []
            for piece in child:
                original[child.tag].append(piece.tag + ':' + piece.text)
    return original


def find_content(container):
    tree = ET.parse(container)
    root = tree.getroot()
    for child in root.iter():
        if 'full-path' in child.attrib:
            content = child.attrib['full-path']
            return content


def process(arg, cwd=None):
    proc = subprocess.Popen(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = proc.communicate()
    returncode = proc.returncode
    if returncode != 0:
        raise Exception(err)

if __name__ == '__main__':
    main('chelovek_v_futlyare_sbornik_.epub', 'testbook.xml', 'finalform')
