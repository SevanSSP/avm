import unittest
import os
from avm import registered_applications


class FirstTestCase(unittest.TestCase):
    def setUp(self):
        # path to application listing file
        self.xml = os.path.join(os.path.dirname(__file__), 'data', 'ApplicationVersions.xml')
        self.apps = registered_applications(appverxml=self.xml)

    def test_number_of_registered_applications(self):
        self.assertEqual(12, len(self.apps))

    def test_sima_path(self):
        # Cannot use exe_path() which will trow an error since the exe-paths in the xml-file refer to typical
        # installation directory on laptops.
        self.assertEqual("C:\programs\sima_35_00\Sima.exe", self.apps['sima']['3.5.0']['exepath'])

    def test_prefem_path(self):
        self.assertEqual("C:\programs\prefem_71_07\\bin\prefem.EXE", self.apps['prefem']['7.1.7']['exepath'])


if __name__ == '__main__':
    unittest.main()
