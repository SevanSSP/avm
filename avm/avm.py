#!/usr/bin/python3
"""
Module for working with DNVGL Application Version Manager
"""
import logging
import os
from xml.dom import minidom
from collections import OrderedDict

# configure logger
logger = logging.getLogger(__name__)

# path to applicationversionmanager xml
APPVERXML = os.path.join(os.getenv('appdata'), 'DNVGL', 'ApplicationVersionManager', 'ApplicationVersions.xml')


def get_exe_path(appname, version=None):
    """
    Return absolute path to DNV GL application executable

    Parameters
    ----------
    appname : str
        Application name
    version : str, optional
        Application version, by default the application marked as default in
        Application Version Manager is used.

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
    appdata = get_registered_applications()

    app = appdata.get(appname.lower())

    if app is None:
        logger.error(f"Application '{appname}' is not registered in Application Version Manager.", exc_info=True)
        return None

    if version is not None:
        # requested specific version
        try:
            appversion = app.get(version.lower())
        except KeyError:
            logger.error(f"Version '{version}' of application '{appname}' is not registered in Application "
                         f"Version Manager.", exc_info=True)
            return None
        else:
            path = appversion.get('exepath')
            versionnumber = appversion.get('versionnumber')

    else:
        # use default version
        path, versionnumber = None, None
        for _, appversion in app.items():
            if appversion.get('default'):
                path = appversion.get('exepath')
                versionnumber = appversion.get('versionnumber')

        if path is None:
            logger.error(f"There is no default version registered for application '{appname}' in Application "
                         f"Version Manager.")
            return None

    # verify that the executable path exists
    if not os.path.exists(path):
        logger.warning(f"The executable path '{path}' for application/version {appname}/{versionnumber} does not exist.")
        return None
    else:
        return path


def get_registered_applications():
    """
    Get all applications registered in Application Version Manager

    Returns
    -------
    OrderedDict
        Registered applications and versions
    """
    # document tree with application information
    logger.debug(f"Parsing applications and versions from '{APPVERXML}'.")
    apps = minidom.parse(APPVERXML).getElementsByTagName('Application')

    # find specified application and version
    data = OrderedDict()
    for app in apps:
        appname = app.getAttribute('Name').lower()                  # lowercase for increased robustness
        versions = app.getElementsByTagName('Version')
        appdata = OrderedDict()
        for version in versions:
            vnumber = version.getAttribute('VersionNumber').lower() # lowercase for increased robustness
            exepath = version.getAttribute('ExeFilePath')
            isdefault = True if version.getAttribute('IsDefault').lower() == 'true' else False
            appdata[vnumber] = OrderedDict(versionnumber=vnumber, exepath=exepath, default=isdefault)
            logger.debug(f"Application '{appname}' - version '{vnumber}'- is default {isdefault}")

        # add application data dict
        data[appname] = appdata

    return data


def list_applications():
    """
    Get all applications registered in Application Version Manager
    """
    # todo: argparser
    # todo: get application details
    # todo implement logger and pipe it to standard out
    # todo: format output

    # import logging
    # import sys
    #
    # root = logging.getLogger()
    # root.setLevel(logging.DEBUG)
    #
    # handler = logging.StreamHandler(sys.stdout)
    # handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    # root.addHandler(handler)
    pass


def get_application_path():
    """
    Get path to application executable
    """
    # todo: argparser
    # todo: get application path
    # todo implement logger and pipe it to standard out
    # todo: format output
    pass

