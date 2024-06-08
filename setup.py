from setuptools import setup, find_packages

__version__ = "0.0.0"

setup(
    name="nodes",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "flask==3.0.3",
        "webargs==8.4.0",
    ],
    extras_require={
        "dev": [
            "mypy==1.10.0",
            "pytest==8.2.1",
            "black==24.4.2",
            "pylint==3.2.2",
            "python-semantic-release==9.8.1",
        ],
    },
)
