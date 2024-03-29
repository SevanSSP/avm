import nox
import tempfile
import os

# override default sessions
nox.options.sessions = ["lint", "tests"]


@nox.session
def lint(session):
    """Highlight syntactical and stylistic problems in the code."""
    session.install("flake8")
    session.run(
        "flake8",
        "avm/",
        "--count",
        "--select=E9,F63,F7,F82",
        "--show-source",
        "--statistics",
    )
    session.run(
        "flake8",
        "avm/",
        "--count",
        "--per-file-ignores=__init__.py:F401",
        "--exit-zero",
        "--max-complexity=10",
        "--max-line-length=127",
        "--statistics",
    )


@nox.session
def tests(session):
    """Run test suite."""
    # install dependencies
    req_path = os.path.join(tempfile.gettempdir(), 'requirements.txt')
    session.install("poetry")

    session.run(
        "poetry",
        "export",
        "--with=dev",
        "--format=requirements.txt",
        f"--output={req_path}",
        external=True,
    )
    session.install("-r", req_path)

    # run tests
    session.run("pytest", "-s", "tests", "--cov=avm", "--cov-report=term-missing", "--cov-fail-under=95")

    # install avm
    session.install(".", "--no-deps")

    # test CLI
    xml_file_path = os.path.join(os.getcwd(), 'tests', 'files', 'app_ver_short.xml')
    session.run("avm-list", fr'--xml-file={xml_file_path}')
    session.run("avm-list", "--all-versions", fr'--xml-file={xml_file_path}')
