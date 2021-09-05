"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
import shutil
from ruamel.yaml import YAML
import pprint

from invoke import task
import webbrowser
from pathlib import Path

Path().expanduser()
yaml = YAML()

ROOT_DIR = Path(__file__).parent
SETUP_FILE = ROOT_DIR.joinpath("setup.py")
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("grpc_web_proto_compile")
TOX_DIR = ROOT_DIR.joinpath(".tox")
TRAVIS_CONFIG_FILE = ROOT_DIR.joinpath(".travis.yml")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [SOURCE_DIR, TEST_DIR]]


def _delete_file(file):
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        try:
            file.unlink()
        except FileNotFoundError:
            pass


@task(help={"check": "Checks if source is formatted without applying changes"})
def format(c, check=False):
    """Format code"""
    python_dirs_string = " ".join(PYTHON_DIRS)
    black_options = "--diff" if check else ""
    c.run("pipenv run black {} {}".format(black_options, python_dirs_string))
    isort_options = "--recursive {}".format("--check-only" if check else "")
    c.run("pipenv run isort {} {}".format(isort_options, python_dirs_string))


@task
def lint(c):
    """Lint code"""
    c.run("pipenv run flake8 {}".format(SOURCE_DIR))


@task
def test(c, min_coverage=None):
    """Run tests"""
    pytest_options = "--cov-fail-under={}".format(min_coverage) if min_coverage else ""
    c.run("pipenv run pytest --cov={} {}".format(SOURCE_DIR, pytest_options))


@task
def type_check(c):
    """Check types"""
    c.run("pipenv run mypy")


def _create(d, *keys):
    current = d
    for key in keys:
        try:
            current = current[key]
        except (TypeError, KeyError):
            current[key] = dict()
            current = current[key]


@task
def install_hooks(c):
    """Install pre-commit hooks"""
    c.run("pipenv run pre-commit install -t pre-commit")
    c.run("pipenv run pre-commit install -t pre-push")


@task
def pre_commit(c):
    """Run all pre-commit checks"""
    c.run("pipenv run pre-commit run --all-files")


@task(
    pre=[test],
    help=dict(
        publish="Publish the result (default False)",
        provider="The provider to publish (default codecov)",
    ),
)
def coverage(c, publish=False, provider="codecov"):
    """Create coverage report"""
    if publish:
        # Publish the results via provider (e.g. codecov or coveralls)
        c.run("pipenv run {}".format(provider))
    else:
        # Build a local report
        c.run("pipenv run coverage html -d {}".format(COVERAGE_DIR))
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task(help={"output": "Generated documentation output format (default is html)"})
def docs(c, output="html"):
    """Generate documentation"""
    c.run("pipenv run sphinx-apidoc -o {} grpc_web_proto_compile".format(DOCS_DIR))
    c.run(
        "pipenv run sphinx-build -b {} {} {}".format(
            output.lower(), DOCS_DIR, DOCS_BUILD_DIR
        )
    )
    if output.lower() == "html":
        webbrowser.open(DOCS_INDEX.as_uri())
    elif output.lower() == "latex":
        c.run("cd {} && make".format(DOCS_BUILD_DIR))


@task
def clean_docs(c):
    """Clean up files from documentation builds"""
    c.run("rm -fr {}".format(DOCS_BUILD_DIR))


@task
def clean_build(c):
    """Clean up files from package building"""
    c.run("rm -fr build/")
    c.run("rm -fr dist/")
    c.run("rm -fr .eggs/")
    c.run("find . -name '*.egg-info' -exec rm -fr {} +")
    c.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(c):
    """Clean up python file artifacts"""
    c.run("find . -name '*.pyc' -exec rm -f {} +")
    c.run("find . -name '*.pyo' -exec rm -f {} +")
    c.run("find . -name '*~' -exec rm -f {} +")
    c.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(c):
    """Clean up files from testing"""
    _delete_file(COVERAGE_FILE)
    shutil.rmtree(TOX_DIR, ignore_errors=True)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests, clean_docs])
def clean(c):
    """Runs all clean sub-tasks"""
    pass


@task(clean)
def dist(c):
    """Build source and wheel packages"""
    c.run("python setup.py sdist")
    c.run("python setup.py bdist_wheel")


@task(pre=[clean, dist])
def release(c):
    """Make a release of the python package to pypi"""
    c.run("twine upload dist/*")
