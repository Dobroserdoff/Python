import xml.etree.ElementTree as ET
# -*- coding: UTF-8 -*-


def main(path):
    step_one = metadata_list(path)
    step_two = id_clean(step_one)
    step_three = elem_constr(step_two)
    output(step_three, path)


def metadata_list(path):
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    result = {}
    for child in root:
        if 'metadata' in child.tag:
            metadata = child

    namespace = '{http://purl.org/dc/elements/1.1/}'
    tags = ['title', 'language', 'identifier','date', 'creator']
    for elem in metadata.iter():
        for tag in tags:
            if namespace + tag in elem.tag:
                if tag in result:
                    result[tag].append(elem.text)
                else:
                    result[tag]=[elem.text]
    return result


def id_clean(result):
    if len(result['identifier']) > 1:
        for value in result['identifier']:
            if 'uuid' in value:
                result['identifier'] = [value[value.rfind(':')+1:]]
                break
    return result


def creator_clean(text):
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
            elements.append(element)
    return elements


def output(elements, path):
    metas = []
    for element in elements:
        if element.attrib:
            meta = '\t\t<' + element.tag + ' ' + element.attrib + '>'
        else:
            meta = '\t\t<' + element.tag + '>'
        meta += element.text
        meta += '</' + element.tag + '>\n'
        metas.append(meta)
    out = open('Test/NewContent' + path[:path.find('/')] + '.xml', 'w')
    header = '<?xml version="1.0"?>\n<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="Zero">' \
             '\n\t<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
    for i in metas:
        header += i.encode('utf-8')
    header += '\t</metadata>\n'
    header += '</package>'
    out.write(header)

if __name__ == '__main__':
    main('Test/NewContentLerm.xml')