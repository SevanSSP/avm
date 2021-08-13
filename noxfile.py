import nox


# override default sessions
nox.options.sessions = ["tests"]

@nox.session
def tests(session):
    """Run test suite."""
    # install dependencies
    session.run("poetry", "install", external=True)
    session.install("pytest")
    session.install("coverage")

    # unit tests
    testfiles = session.posargs or ["tests/"]
    session.run("coverage", "run", "-m", "pytest", *testfiles)
    session.notify("cover")


@nox.session
def cover(session):
    """Analyse and report test coverage."""
    session.install("coverage")
    # TODO: Add "--fail-under=99" once test coverage is improved
    session.run("coverage", "report", "--show-missing")
    session.run("coverage", "erase")


@nox.session
def blacken(session):
    """Run black code formatter."""
    session.install("black", "isort")
    files = ["avm", "tests", "noxfile.py"]
    session.run("black", *files, "--diff", "--color")
    session.run("isort", *files, "--diff")