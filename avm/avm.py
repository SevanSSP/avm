#!/usr/bin/python3
"""
Module for working with DNVGL Application Version Manager
"""
import logging
import os
from xml.dom import minidom
from xml.parsers.expat import ExpatError
from collections import OrderedDict

# configure logger
logger = logging.getLogger(__name__)


def exe_path(appname, version=None, appverxml=None):
    """
    Return absolute path to DNV GL application executable

    Parameters
    ----------
    appname : str
        Application name
    version : str, optional
        Application version, by default the application marked as default in
        Application Version Manager is used.
    appverxml : str, optional
        XML file listing application-versions. By default the file in APPDATA is applied.

    Returns
    -------
    str
        Absolute path to application executable

    Notes
    -----
    Based on parsing the 'ApplicationVersions.xml' in the AppData directory
    on your local machine.

    """
    # all registered applications
    try:
        appdata = registered_applications(appverxml=appverxml)
    except FileNotFoundError:
        logger.error("Failed to load application version data", exc_info=True)
        raise FileNotFoundError("Failed to load application version data")

    # get app data
    app = appdata.get(appname.lower())
    if app is None:
        logger.warning(f"Application '{appname}' is not registered in Application Version Manager.", exc_info=True)
        return None

    if version is not None:
        # requested specific version
        appversion = app.get(version.lower())
        if not appversion:
            logger.warning(f"Version '{version}' of application '{appname}' is not registered in Application "
                           f"Version Manager.")
            return None
        else:
            if appname.lower() == 'simo':
                path = os.path.join(appversion.get('installdir'), 'simo', 'bin', 'rsimo.exe')
            elif appname.lower() == 'riflex':
                path = os.path.join(appversion.get('installdir'), 'Riflex', 'bin', 'riflex.bat')
            else:
                path = appversion.get('exepath')
            versionnumber = appversion.get('versionnumber')

    else:
        # use default version
        path, versionnumber = None, None
        for _, appversion in app.items():
            if appversion.get('default'):
                if appname.lower() == 'simo':
                    path = os.path.join(appversion.get('installdir'), 'simo', 'bin', 'rsimo.exe')
                elif appname.lower() == 'riflex':
                    path = os.path.join(appversion.get('installdir'), 'Riflex', 'bin', 'riflex.bat')
                    print(path)
                else:
                    path = appversion.get('exepath')
                versionnumber = appversion.get('versionnumber')

        if path is None:
            logger.warning(f"There is no default version registered for application '{appname}' in Application "
                           f"Version Manager.")
            return None

    # verify that the executable path exists
    if not os.path.exists(path):
        logger.warning(
            f"The executable path '{path}' for application/version {appname}/{versionnumber} does not exist.")
        return None
    else:
        return f'"{path}"'


def installation_path(appname, version=None, appverxml=None):
    """
    Return installation path to DNV GL application

    Parameters
    ----------
    appname : str
        Application name
    version : str, optional
        Application version, by default the application marked as default in
        Application Version Manager is used.
    appverxml : str, optional
        XML file listing application-versions. By default the file in APPDATA is applied.

    Returns
    -------
    str
        Absolute path to installation directory

    Notes
    -----
    Based on parsing the 'ApplicationVersions.xml' in the AppData directory
    on your local machine.

    """
    # all registered applications
    try:
        appdata = registered_applications(appverxml=appverxml)
    except FileNotFoundError:
        logger.error("Failed to load application version data", exc_info=True)
        raise FileNotFoundError("Failed to load application version data")

    # get app data
    app = appdata.get(appname.lower())
    if app is None:
        logger.warning(f"Application '{appname}' is not registered in Application Version Manager.", exc_info=True)
        return None

    if version is not None:
        # requested specific version
        appversion = app.get(version.lower())
        if appversion is None:
            logger.warning(f"Version '{version}' of application '{appname}' is not registered in Application "
                           f"Version Manager.")
            return None
        else:
            path = appversion.get('installdir')
            versionnumber = appversion.get('versionnumber')

    else:
        # use default version
        path, versionnumber = None, None
        for _, appversion in app.items():
            if appversion.get('default'):
                path = appversion.get('installdir')
                versionnumber = appversion.get('versionnumber')

        if path is None:
            logger.warning(f"There is no default version registered for application '{appname}' in Application "
                           f"Version Manager.")
            return None

    # verify that the executable path exists
    if not os.path.exists(path):
        logger.warning(f"The path '{path}' for application/version {appname}/{versionnumber} does not exist.")
        return None
    else:
        return f'"{path}"'


def all_versions(appname, appverxml=None):
    """
    Get all versions of an application registered in Application Version Manager

    Parameters
    ----------
    appname : str
        Application name
    appverxml : str, optional
        XML file listing application-versions. By default the file in APPDATA is applied.

    Returns
    -------
    OrderedDict
        Registered applications and versions
    """
    # all registered applications
    try:
        appdata = registered_applications(appverxml=appverxml)
    except FileNotFoundError:
        logger.error("Failed to load application version data", exc_info=True)
        raise FileNotFoundError("Failed to load application version data")

    # get app data
    app = appdata.get(appname.lower())
    if app is None:
        logger.warning(f"Application '{appname}' is not registered in Application Version Manager.", exc_info=True)
        return None

    return app


def latest_version(appname, below=None, appverxml=None):
    """
    Get the latest version of an application registered in Application Version Manager

    Parameters
    ----------
    appname : str
        Application name
    below : str, optional, f"{major}[.{minor}[.{patch}]]"
        Version below which to return the latest version, by default the latest installed version is returned.
    appverxml : str, optional
        XML file listing application-versions. By default the file in APPDATA is applied.

    Returns
    -------
    str : f"{major}.{minor}.{patch}"
        Latest available version of the application, optionally below a certain version
    """

    if below is None:
        below_major = None
        below_minor = None
        below_patch = None
    else:
        below_txt = below.split('.')
        if len(below_txt) == 1:
            below_major = int(below_txt[0])
            below_minor = None
            below_patch = None
        elif len(below_txt) == 2:
            below_major = int(below_txt[0])
            below_minor = int(below_txt[1])
            below_patch = None
        elif len(below_txt) == 3:
            below_major = int(below_txt[0])
            below_minor = int(below_txt[1])
            below_patch = int(below_txt[2])
        else:
            raise ValueError(f'Incorrect version definition used: below={below}')

    candidate = None

    for version, _ in all_versions(appname, appverxml).items():
        version_major, version_minor, version_patch = map(int, version.split('.'))

        if not below_major or (
                version_major < below_major) or (
                version_major == below_major and below_minor and
                version_major == below_major and version_minor < below_minor) or (
                version_major == below_major and version_minor == below_minor and below_patch and
                version_major == below_major and version_minor == below_minor and version_patch < below_patch
        ):

            if not candidate:
                candidate = version
            else:
                candidate_major, candidate_minor, candidate_patch = map(int, candidate.split('.'))
                if candidate_major > version_major:
                    candidate = version
                    continue
                elif candidate_major == version_major and candidate_minor < version_minor:
                    candidate = version
                    continue
                elif candidate_major == version_major and candidate_minor == version_minor and (
                        candidate_patch < version_patch):
                    candidate = version
                    continue
                else:
                    continue

    if not candidate:
        raise ValueError(f'No {appname} version below {below} found')
    else:
        return candidate


def registered_applications(appverxml=None):
    """
    Get all applications registered in Application Version Manager

    Parameters
    ----------
    appverxml : str, optional
        XML file listing application-versions. By default the file in APPDATA is applied.

    Returns
    -------
    OrderedDict
        Registered applications and versions
    """
    # Try to locate the ApplicationVersions.xml in appdata, if it is not specified
    if appverxml is None:
        print('inside', os.getenv('APPDATA'))
        try:
            if os.path.exists(
                    os.path.join(os.getenv('appdata'), 'DNVGL', 'ApplicationVersionManager',
                                 'ApplicationVersions.xml')
            ):
                appverxml = os.path.join(os.getenv('appdata'), 'DNVGL', 'ApplicationVersionManager',
                                         'ApplicationVersions.xml')

            elif os.path.exists(
                    os.path.join(os.getenv('appdata'), 'DNV', 'ApplicationVersionManager',
                                 'ApplicationVersions.xml')
            ):
                appverxml = os.path.join(os.getenv('appdata'), 'DNV', 'ApplicationVersionManager',
                                         'ApplicationVersions.xml')
            else:
                raise FileNotFoundError("Unable to automatically find 'ApplicationVersions.xml'")
        except TypeError:
            logger.error("No environmental variable called 'APPDATA'. Unable to find 'ApplicationVersions.xml'.")
            raise TypeError("No environmental variable called 'APPDATA'. Unable to find 'ApplicationVersions.xml'.")

    # Verify the existence of the xml file
    if os.path.exists(appverxml):
        logger.debug(f"Using the xml file '{appverxml}'.")
    else:
        logger.error(f"The xml file '{appverxml}' does not exist.")
        raise FileNotFoundError(f"The xml file '{appverxml}' does not exist.")

    # parse document tree with application information
    try:
        apps = minidom.parse(appverxml).getElementsByTagName('Application')
    except (AttributeError, ExpatError) as e:
        logger.error(f"Failed to parse {appverxml}", exc_info=True)
        raise e

    # find specified application and version
    data = OrderedDict()
    for app in apps:
        appname = app.getAttribute('Name').lower()  # lowercase for increased robustness
        versions = app.getElementsByTagName('Version')
        appdata = OrderedDict()
        for version in versions:
            vnumber = version.getAttribute('VersionNumber').lower()  # lowercase for increased robustness
            exepath = version.getAttribute('ExeFilePath')
            installdir = version.getAttribute('InstallDir')
            platform = version.getAttribute('Platform')
            producttype = version.getAttribute('ProductType')
            category = version.getAttribute('Category')
            isdefault = True if version.getAttribute('IsDefault').lower() == 'true' else False
            appdata[vnumber] = OrderedDict(
                versionnumber=vnumber,
                exepath=exepath,
                default=isdefault,
                installdir=installdir,
                platform=platform,
                producttype=producttype,
                category=category
            )
            logger.debug(f"Application '{appname}' - version '{vnumber}'- is default {isdefault}")

        # add application data dict
        data[appname] = appdata

    return data
