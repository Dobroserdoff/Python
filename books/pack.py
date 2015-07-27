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
        step_one, add_content = Converter.metadata_list(metadata_request)
        step_two = Converter.id_clean(step_one, path)
        fix = metadata_content(step_two, patch)
        metadata = elem_constr(fix)
        fix_add_content(add_content)
        result = Converter.output(metadata, add_content)
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


def fix_add_content(content):
    for piece in content:
        if 'manifest' in piece.tag:
            for elem in list(piece):
                if 'fonts' in elem.attrib['href']:
                    piece.remove(elem)
                elif 'cover' in elem.attrib['href']:
                    piece.remove(elem)


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
