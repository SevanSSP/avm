import pytest
import os
from string import Template


@pytest.fixture(scope='session')
def xml_input(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp('avm')

    subs = {
        'WADAM_DIR': tmp_path.joinpath('WADAM'),
        'WADAM_EXE': tmp_path.joinpath('WADAM', 'WADAM.txt'),
        'WADAM_924_EXE': tmp_path.joinpath('WADAM', 'WADAM_924.txt'),
        'NON_EXIST_DIR': os.path.join(tmp_path, 'NON_EXIST_DIR'),
        'NON_EXIST_EXE': os.path.join(tmp_path, 'NON_EXIST_DIR', 'NON_EXIST.txt'),
        'SIMO_DIR': os.path.join(tmp_path, 'SIMO'),
        'RIFLEX_DIR': os.path.join(tmp_path, 'RIFLEX'),
    }

    for key in ['WADAM_DIR', 'SIMO_DIR', 'RIFLEX_DIR']:
        os.makedirs(subs[key])

    for key in ['WADAM_EXE', 'WADAM_924_EXE']:
        open(subs[key], 'w').close()

    for key, file in zip(['SIMO_DIR', 'RIFLEX_DIR'], ['simo\\bin\\rsimo.exe', 'riflex\\bin\\riflex.bat']):
        open(subs[key]+file, 'w').close()

    return tmp_path, subs


@pytest.fixture(scope='session')
def xml_file_path(xml_input):
    xml_file_template = os.path.join(os.path.dirname(__file__), 'files/app_ver_template.xml')

    tmp_path, subs = xml_input

    with open(xml_file_template, 'r') as f:
        src = Template(f.read())
        result = src.substitute(subs)

    xml_file_path = os.path.join(tmp_path, 'app_ver.xml')
    with open(xml_file_path, 'w') as f:
        f.write(result)

    return xml_file_path


@pytest.fixture(scope='session')
def faulty_xml_file_path():
    xml_file = os.path.join(os.path.dirname(__file__), 'files/Faulty.xml')

    return xml_file
