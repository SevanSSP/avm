import os

import pytest
import sys

from xml.parsers.expat import ExpatError

from avm import exe_path, installation_path, all_versions, latest_version, registered_applications, list_applications


def test_exe_path(xml_file_path, xml_input):
    _, subs = xml_input

    default_wadam_path = exe_path('wadam', appverxml=xml_file_path)
    assert default_wadam_path == f'"{subs["WADAM_EXE"]}"'

    v9_2_4_wadam_path = exe_path(appname='wadam', version='9.2.4', appverxml=xml_file_path)
    assert v9_2_4_wadam_path == f'"{subs["WADAM_924_EXE"]}"'

    not_there = exe_path(appname='dadam', appverxml=xml_file_path)
    assert not_there is None

    version_not_there = exe_path(appname='wadam', version='205.2.1', appverxml=xml_file_path)
    assert version_not_there is None

    file_not_there = exe_path(appname='wadam', version='9.5.2', appverxml=xml_file_path)
    assert file_not_there is None

    no_default = exe_path(appname='nodefault', appverxml=xml_file_path)
    assert no_default is None

    no_path = exe_path(appname='nopath', appverxml=xml_file_path)
    assert no_path is None

    simo_path = exe_path(appname='simo', appverxml=xml_file_path)
    assert simo_path == f'"{os.path.join(subs["SIMO_DIR"], "simo", "bin", "rsimo.exe")}"'
    assert simo_path == exe_path(appname='simo', version='4.20.4', appverxml=xml_file_path)

    riflex_path = exe_path(appname='riflex', appverxml=xml_file_path)
    assert riflex_path == f'"{os.path.join(subs["RIFLEX_DIR"], "Riflex", "bin", "riflex.bat")}"'
    assert riflex_path == exe_path(appname='riflex', version='4.20.4', appverxml=xml_file_path)

    with pytest.raises(FileNotFoundError):
        _ = exe_path(appname='wadam', appverxml='not_here')


def test_installation_path(xml_file_path, xml_input):
    _, subs = xml_input

    default_wadam_installation_path = installation_path('wadam', appverxml=xml_file_path)
    assert default_wadam_installation_path == f'"{subs["WADAM_DIR"]}"'
    assert default_wadam_installation_path == installation_path('wadam', version='9.5.3',
                                                                appverxml=xml_file_path)

    not_there = installation_path('dadam', appverxml=xml_file_path)
    assert not_there is None

    version_not_there = installation_path('wadam', version='205.2.1', appverxml=xml_file_path)
    assert version_not_there is None

    folder_not_there = installation_path('wadam', version='9.5.2', appverxml=xml_file_path)
    assert folder_not_there is None

    no_default = installation_path('nodefault', appverxml=xml_file_path)
    assert no_default is None

    with pytest.raises(FileNotFoundError):
        _ = installation_path('wadam', appverxml='not_here')


def test_all_versions(xml_file_path):
    all_ver = all_versions(appname='wadam', appverxml=xml_file_path)
    assert len(all_ver) == 6
    assert list(all_ver.keys()) == ['9.5.3', '9.5.1', '9.2.4', '9.5.2', '9.4.1', '9.4.9']

    all_not_there = all_versions(appname='dadam', appverxml=xml_file_path)
    assert all_not_there is None

    with pytest.raises(FileNotFoundError):
        _ = all_versions(appname='wadam', appverxml='not_here')


def test_latest_version(xml_file_path):
    latest_ver = latest_version(appname='wadam', appverxml=xml_file_path)
    assert latest_ver == '9.5.3'

    latest_below_10 = latest_version(appname='wadam', appverxml=xml_file_path, below='10')
    assert latest_below_10 == '9.5.3'

    latest_below_9_5 = latest_version(appname='wadam', appverxml=xml_file_path, below='9.5')
    assert latest_below_9_5 == '9.4.9'

    latest_below_9_5_3 = latest_version(appname='wadam', appverxml=xml_file_path, below='9.5.3')
    assert latest_below_9_5_3 == '9.5.2'

    with pytest.raises(ValueError):
        _ = latest_version(appname='wadam', below='10.5.10.5', appverxml='not_here')

    with pytest.raises(FileNotFoundError):
        _ = latest_version(appname='wadam', below='1.5.5', appverxml='not_here')


def test_registered_applications(xml_file_path, faulty_xml_file_path, monkeypatch):
    reg_apps = registered_applications(appverxml=xml_file_path)
    assert len(reg_apps) == 13

    with pytest.raises(FileNotFoundError):
        _ = registered_applications(appverxml='not_here')

    with pytest.raises(ExpatError):
        _ = registered_applications(appverxml=faulty_xml_file_path)

    with pytest.raises(FileNotFoundError):
        monkeypatch.setenv('appdata', 'not_here')
        _ = registered_applications()

    with pytest.raises(TypeError):
        if os.getenv('appdata'):
            monkeypatch.delenv('appdata')

        _ = registered_applications()


def test_list_applications(xml_file_path, capsys, monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['avm-list', fr'--xml-file={xml_file_path}'])
        list_applications()
        captured = capsys.readouterr()
        assert 115 * "=" in captured.out

    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['avm-list', '--all-versions', fr'--xml-file={xml_file_path}'])
        list_applications()
        captured = capsys.readouterr()
        assert 115 * "=" in captured.out

    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['avm-list', '--logging-level', 'debug', fr'--xml-file={xml_file_path}'])
        list_applications()
        captured = capsys.readouterr()
        assert 115 * "=" in captured.out
