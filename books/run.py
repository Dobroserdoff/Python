import os
import subprocess
import xml.etree.ElementTree as ET
import Converter


def main(filename, path):
    if path in os.listdir('.'):
        process(['rm', '-r', path])

    process(['mkdir', path])
    process(['unzip', filename, '-d' + path])
    content = find_content(path + '/META-INF/container.xml')
    result = Converter.main(path + '/' + content)
    out = open(path + '/' + content, 'w')
    out.write(result)
    out.close()
    os.chdir(path)
    process(['zip', '-r', '../' + path, 'mimetype', 'META-INF', 'OEBPS'])
    process(['mv', '../' + path + '.zip', '../' + path + '.epub'])


def find_content(container):
    tree = ET.parse(container)
    root = tree.getroot()
    for child in root.iter():
        if 'full-path' in child.attrib:
            content = child.attrib['full-path']
            return content


def process(arg):
    proc = subprocess.Popen(arg)
    proc.wait()


if __name__ == '__main__':
    main('chelovek_v_futlyare_sbornik_.epub', 'Check')
