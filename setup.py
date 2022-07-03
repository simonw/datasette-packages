from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-packages",
    description="Show a list of currently installed Python packages",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-packages",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-packages/issues",
        "CI": "https://github.com/simonw/datasette-packages/actions",
        "Changelog": "https://github.com/simonw/datasette-packages/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License",
    ],
    version=VERSION,
    packages=["datasette_packages"],
    entry_points={"datasette": ["packages = datasette_packages"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "datasette-graphql>=2.1"]},
    python_requires=">=3.7",
)
