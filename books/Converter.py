import xml.etree.ElementTree as ET
# -*- coding: UTF-8 -*-


def main(path):
    step_one = metadata_list(path)
    step_two = titles_clean(step_one)
    step_three = id_clean(step_two)
    step_four = elem_constr(step_three)
    output(step_four, path)


def metadata_list(path):
    tree = ET.ElementTree(file=path)
    root = tree.getroot()
    result = []
    for child in root:
        if 'metadata' in child.tag:
            metadata = child

    tags = ['title', 'language', 'identifier','date', 'creator']
    for elem in metadata.iter():
        for tag in tags:
            if tag in elem.tag:
                result.append({elem.tag[elem.tag.find('}') + 1:] : elem.text})
    return result


def titles_clean(result):
    titles = []
    for i in range(len(result)):
        if result[i].keys()[0] == 'title':
            titles.append(i)
    while len(titles) > 1:
        if result[titles[-1]].values()[0] == result[titles[-2]].values()[0]:
            del result[titles[-1]]
            del titles[-1]
        else:
            break
    return result


def id_clean(result):
    identifiers = []
    for j in range(len(result)):
        if result[j].keys()[0] == 'identifier':
            if 'uuid' not in result[j].values()[0]:
                identifiers.append(j)
            else:
                new_value = result[j].values()[0][result[j].values()[0].rfind(':') + 1:]
                result[j]['identifier'] = new_value
    if identifiers:
        for k in identifiers:
            del result[k]
    return result


def creator_clean(text):
    words = text.split(' ')
    word = words[-1]
    attribute = 'p6:file-as="' + word + '" xmlns:p6="http://www.idpf.org/2007/opf"'
    return attribute


def elem_constr(result):
    elements = []
    for dic in result:
        element = ET.Element('dc:' + str(dic.keys()[0]))
        element.text = dic.values()[0]
        if dic.keys()[0] == 'creator':
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
    main('Check/OEBPS/Content.opf')