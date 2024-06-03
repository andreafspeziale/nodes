from setuptools import setup, find_packages

setup(
    name="nodes",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "flask==3.0.3",
        "webargs==5.5.2",
    ],
    extras_require={
        "dev": [
            "mypy==1.10.0",
            "pytest==8.2.1",
            "black==24.4.2",
        ],
    },
)
