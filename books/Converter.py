import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import uuid
# -*- coding: UTF-8 -*-

DEBUG = False


def main(filename):
    path = str(uuid.uuid4())
    os.mkdir(path)

    try:
        process(['unzip', filename, '-d' + path])
        content = find_content(path + '/META-INF/container.xml')
        result = convertor(path, content)
        out = open(path + '/' + content, 'w')
        try:
            out.write(result)
        finally:
            out.close()
        process(['zip', '-r', '../' + path, 'mimetype', 'META-INF', 'OEBPS'], cwd=path)
        os.rename(path + '.zip', 'new_' + filename)
    finally:
        if not DEBUG:
            if os.path.isdir(path):
                shutil.rmtree(path)


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


def convertor(unique, content):
    path = unique + '/' + content
    step_one, add_content = metadata_list(path)
    step_two = id_clean(step_one, unique)
    step_three = elem_constr(step_two)
    result = output(step_three, add_content)
    return result


def metadata_list(path):
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    result = {}
    add_content = []
    for child in root:
        if 'metadata' in child.tag:
            metadata = child

    namespace = '{http://purl.org/dc/elements/1.1/}'
    tags = ['title', 'language', 'identifier', 'date', 'creator']
    for elem in metadata.iter():
        for tag in tags:
            if namespace + tag == elem.tag:
                if tag in result:
                    result[tag].append(elem.text)
                else:
                    result[tag] = [elem.text]
    return result


def id_clean(result, unique):
    if len(result['identifier']) > 1:
        for value in result['identifier']:
            if 'uuid' in value:
                result['identifier'] = [unique]
                break
    else:
        result['identifier'] = [unique]
    return result


def creator_clean(text, attribute=None):
    words = text.split(' ')
    word = words[-1]
    attribute = 'p6:file-as="' + word + '" xmlns:p6="http://www.idpf.org/2007/opf"'
    return attribute


def elem_constr(result):
    elements = []
    for key in result:
        for value in result[key]:
            element = ET.Element('dc:' + key)
            element.text = value
            if key == 'creator':
                element.attrib = creator_clean(element.text)
            if key == 'identifier':
                element.attrib = 'id="Zero"'
            elements.append(element)
    return elements


def output(elements, add_content=None):
    metas = []
    for element in elements:
        if element.attrib:
            meta = '    <' + element.tag + ' ' + element.attrib + '>'
        else:
            meta = '    <' + element.tag + '>'
        meta += element.text
        meta += '</' + element.tag + '>\n'
        metas.append(meta)

    result = '<?xml version="1.0"?>\n<package version="2.0" ' \
             'xmlns="http://www.idpf.org/2007/opf" unique-identifier="Zero">\n  ' \
             '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'

    for i in metas:
        result += i.encode('utf-8')
    result += '  </metadata>\n  '
    if add_content:
        for piece in add_content:
            result += ET.tostring(piece)
    result += '</package>'
    return result


if __name__ == '__main__':
    main('chelovek_v_futlyare_sbornik_.epub')