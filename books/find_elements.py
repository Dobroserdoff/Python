
def some_by_attr(parent, tag_name, attr_name, attr_value):
    return filter_some_by_attr(some_by_tag(parent, tag_name), attr_name, attr_value)


def some_by_tag(parent, tag_name):
    elements = []
    for elem in parent:
        if elem.tag == tag_name:
            elements.append(elem)
    return elements


def filter_some_by_attr(elements_to_filter, attr_name, attr_value):
    elements = []
    for elem in elements_to_filter:
        if elem.attrib[attr_name] == attr_value:
            elements.append(elem)
    return elements


def one_by_attr(parent, tag_name, attr_name, attr_value):
    result = some_by_attr(parent, tag_name, attr_name, attr_value)
    if len(result) == 0:
        raise Exception(u'Tag %s not found' % tag_name)
    if len(result) > 1:
        raise Exception(u'Found multiple %s tags' % tag_name)
    return result[0]