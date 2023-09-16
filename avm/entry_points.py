#!/usr/bin/python3
"""
Console entry points for the avm package
"""
import argparse
import logging
from .avm import registered_applications

# setup logging levels
LOGGING_LEVELS = dict(
    debug=logging.DEBUG,
    info=logging.INFO,
    warning=logging.WARNING,
    error=logging.ERROR,
)


def list_applications():
    """
    Get all applications registered in Application Version Manager
    """
    # create console argument parser
    parser = argparse.ArgumentParser(prog="avm-list",
                                     description="List applications registered in DNV GL Software's Application Version"
                                                 " Manager.")
    parser.add_argument("--all-versions", action="store_true",
                        help="List all versions, not just the ones marked as default.")
    parser.add_argument("--xml-file", dest='xml_file', action='store',
                        help="XML file listing application-versions.")

    parser.add_argument("-l", "--logging-level", default="info", choices=list(LOGGING_LEVELS.keys()),
                        help="Set logging level.")

    # parse command line arguments
    args = parser.parse_args()

    # grab and configure logger
    logger = logging.getLogger()
    logger.setLevel(LOGGING_LEVELS.get(args.logging_level))
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    ch.setFormatter(formatter)
    ch.setLevel(LOGGING_LEVELS.get(args.logging_level))
    logger.addHandler(ch)

    # get application version data
    data = registered_applications(appverxml=args.xml_file)

    # print application details to screen
    print(115 * "=")
    print("{:20} {:10} {:8} {}".format('Application', 'Version', 'Default', 'Executable'))
    print(115 * "-")
    for appname, app in data.items():
        for versionnumber, version in app.items():
            isdefault = version.get('default')
            exepath = version.get('exepath')
            defmark = '*' if isdefault else ''

            if args.all_versions:
                # list all versions
                print("{:20} {:10} {:8} {}".format(appname, versionnumber, defmark, exepath))
            if not args.all_versions and isdefault:
                # list only default versions
                print("{:20} {:10} {:8} {}".format(appname, versionnumber, defmark, exepath))
            else:
                logger.debug(f"Skipping non-default application/version '{appname}'/'{versionnumber}'")
                continue

    print(115 * "=")
