# datasette-packages

[![PyPI](https://img.shields.io/pypi/v/datasette-packages.svg)](https://pypi.org/project/datasette-packages/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-packages?include_prereleases&label=changelog)](https://github.com/simonw/datasette-packages/releases)
[![Tests](https://github.com/simonw/datasette-packages/workflows/Test/badge.svg)](https://github.com/simonw/datasette-packages/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-packages/blob/main/LICENSE)

Show a list of currently installed Python packages

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-packages

## Usage

Visit `/-/packages` to see a list of installed Python packages.

Visit `/-/packages.json` to get that back as JSON.

## Demo

The output of this plugin can be seen here:

- https://latest-with-plugins.datasette.io/-/packages
- https://latest-with-plugins.datasette.io/-/packages.json

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-packages
    python3 -mvenv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
