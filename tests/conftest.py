import pytest
import os


@pytest.fixture(scope='session')
def xml_file_path():
    xml_file = os.path.join(os.path.dirname(__file__), 'files/ApplicationVersions.xml')

    return xml_file


@pytest.fixture(scope='session')
def faulty_xml_file_path():
    xml_file = os.path.join(os.path.dirname(__file__), 'files/Faulty.xml')

    return xml_file
