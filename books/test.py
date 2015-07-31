import os


class Example(object):
    def __init__(self):
        self.module_dir = os.path.dirname(__file__)

    def get_test_file_path(self, relative_path):
        return os.path.join(self.module_dir, 'test_data', relative_path)


e = Example()
print e.get_test_file_path('meta1.xml')
