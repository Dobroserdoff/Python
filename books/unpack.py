import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import Converter
import uuid

DEBUG = False


def main(filename):
    path = str(uuid.uuid4())
    os.mkdir(path)

    try:
        process(['unzip', filename, '-d' + path])
        content = find_content(path + '/META-INF/container.xml')
        metadata_request = path + '/' + content
        step_one = Converter.metadata_list(metadata_request)
        step_two = Converter.id_clean(step_one, path)
        metadata = elem_constr(step_two)
        result = output(metadata)
        out = open('testbook.xml', 'w')
        try:
            out.write(result)
        finally:
            out.close()
    finally:
        if not DEBUG:
            if os.path.isdir(path):
                shutil.rmtree(path)


def elem_constr(result):
    elements = []
    for key in result:
        if key == 'title':
            while len(result[key]) > 1:
                if len(result[key][0]) > len(result[key][1]):
                    del result[key][1]
                else:
                    del result[key][1]
        for value in result[key]:
            element = ET.Element(key)
            element.text = value
            if key == 'creator':
                new_element = creator_clean(element)
                element = new_element
            if key == 'identifier':
                continue
            elements.append(element)
    return elements


def creator_clean(element):
    words = element.text.split(' ')
    word = words[-1]
    result = ET.Element('creator')
    display = ET.SubElement(result, 'display')
    display.text = element.text
    sort = ET.SubElement(result, 'sort')
    sort.text = word
    return result


def output(elements):
    metas = []
    for element in elements:
        meta = ET.tostring(element, 'utf-8') + '\n'
        metas.append(meta)

    result = '<?xml version="1.0"?>\n<book>\n'

    for i in metas:
        result += i
    result += '</book>'
    return result


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
    main('chelovek_v_futlyare_sbornik_.epub')