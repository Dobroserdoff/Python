import uuid
import sys
import json
import epub
import zipfile
import xml.etree.ElementTree as ET
# -*- coding: UTF-8 -*-


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'chelovek_v_futlyare_sbornik_.epub'

    epub_zip = zipfile.ZipFile(filename)

    if len(sys.argv) > 2:
        patch = sys.argv[2]
    else:
        patch = 'testbook.json'

    try:
        content = epub.find_content(epub_zip.open('META-INF/container.xml'))
        result_json = parse_book_xml(epub_zip.read(content))
        out = open(patch, 'w')
        try:
            out.write(result_json)
        finally:
            out.close()
    finally:
        epub_zip.close()


def parse_book_xml(book_xml_string):
    root = ET.fromstring(book_xml_string)
    step_one = metadata_list(root)
    step_two = year_and_id_clean(step_one)
    metadata = elem_constr(step_two)
    result_dict = output(metadata)
    result_json = json.dumps(result_dict, indent=4, ensure_ascii=False, sort_keys=True).encode('utf-8')
    return result_json


def metadata_list(root):
    result = {}
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


def year_and_id_clean(result):
    unique = str(uuid.uuid4())
    if len(result['identifier']) > 1:
        for value in result['identifier']:
            if 'uuid' in value:
                result['identifier'] = [unique]
                break
    else:
        result['identifier'] = [unique]
    return result


def elem_constr(result):
    elements = []
    for key in result:
        while len(result[key]) > 1:
            if len(result[key][0]) > len(result[key][1]):
                del result[key][1]
                sys.stdout.write('Shorter duplicate of ' + result[key][0] + ' has been deleted\n')
            elif len(result[key][0]) < len(result[key][1]):
                del result[key][0]
                sys.stdout.write('Shorter duplicate of ' + result[key][1] + ' has been deleted\n')
            elif len(result[key][0]) == len(result[key][1]):
                del result[key][1]
                sys.stdout.write('Duplicate of ' + result[key][0] + ' has been deleted\n')
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
    main_dir = {}
    for item in elements:
        if item.text:
            if item.tag in main_dir:
                main_dir[item.tag].append(item.text)
            else:
                main_dir[item.tag] = [item.text]
        else:
            sub_dir = {}
            for piece in item:
                sub_dir[piece.tag] = piece.text
            main_dir[item.tag] = sub_dir
    for key in main_dir:
        if len(main_dir[key]) == 1:
            main_dir[key] = main_dir[key][0]
    return main_dir


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print >> sys.stderr, 'Error occured', e
        sys.exit(1)

    sys.exit(0)