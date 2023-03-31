from setuptools import find_packages
from setuptools import setup

# Import __version__
exec(open("mysql_mimic/version.py").read())

setup(
    name="Mesos",
    version=__version__,
    description="A python implementation of the mysql server protocol",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kelsin/mysql-mimic",
    author="Christopher Giroir",
    author_email="kelsin@valefor.com",
    license="MIT",
    packages=find_packages(include=["mysql_mimic", "mysql_mimic.*"]),
    python_requires=">=3.6",
    install_requires=["sqlglot>=10.1.3"],
    extras_require={
        "dev": [
            "aiomysql",
            "mypy",
            "mysql-connector-python",
            "black",
            "coverage",
            "gssapi",
            "k5test",
            "pylint",
            "pytest",
            "pytest-asyncio",
            "sphinx",
            "sqlalchemy",
            "twine",
            "wheel",
        ],
        "krb5": ["gssapi"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: SQL",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
