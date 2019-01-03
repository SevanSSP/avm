import unittest
import os
from avm import registered_applications, exe_path


# path to application listing file
xml = os.path.join(os.path.dirname(__file__), 'data', 'ApplicationVersions.xml')


class FirstTestCase(unittest.TestCase):
    def test_number_of_registered_applications(self):
        self.assertEqual(12, len(registered_applications(appverxml=xml)))

    def test_sima_path(self):
        self.assertEqual("C:\programs\sima_35_00\Sima.exe", exe_path("sima", "3.5.0", appverxml=xml))

    def test_prefem_path(self):
        self.assertEqual("C:\programs\prefem_71_07\\bin\prefem.EXE", exe_path("prefem", "7.1.7", appverxml=xml))


if __name__ == '__main__':
    unittest.main()
