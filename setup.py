from setuptools import find_packages
from setuptools import setup

LIBRARY = "mesos"

__version__ = "notset"
with open(f"{LIBRARY}/version.py", mode="r") as v:
    vers = v.read()
exec(vers)  # nosec

with open("README.md", mode="r", encoding="UTF8") as rm:
    long_description = rm.read()

try:
    with open("requirements.txt", "r") as f:
        required = f.read().splitlines()
except:
    with open(f"{LIBRARY}.egg-info/requires.txt", "r") as f:
        required = f.read().splitlines()

setup_config = {
    "name": LIBRARY,
    "version": __version__,
    "description": "MySQL compatible interface for Opteryx.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "maintainer": "@joocer",
    "author": "@joocer",
    "author_email": "justin.joyce@joocer.com",
    "packages": find_packages(include=[LIBRARY, f"{LIBRARY}.*"]),
    "python_requires": ">=3.8",
    "install_requires": required,
    "entry_points": {
        "console_scripts": ["mesos=mesos.command:main"],
    },
}

setup(**setup_config)
