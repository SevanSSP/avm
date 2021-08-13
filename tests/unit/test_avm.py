def test_number_of_registered_applications(setUp):
    assert 12 == len(setUp['apps'])


def test_sima_path(setUp):
    # Cannot use exe_path() which will trow an error since the exe-paths in the xml-file refer to typical
    # installation directory on laptops.
    assert "C:\programs\sima_35_00\Sima.exe" == setUp['apps']['sima']['3.5.0']['exepath']


def test_prefem_path(setUp):
    assert "C:\programs\prefem_71_07\\bin\prefem.EXE" == setUp['apps']['prefem']['7.1.7']['exepath']

