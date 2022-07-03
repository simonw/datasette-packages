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

## With datasette-graphql

if you have version 2.1 or higher of the [datasette-graphql](https://datasette.io/plugins/datasette-graphql) plugin installed you can also query the list of packages using this GraphQL query:

```graphql
{
  packages {
    name
    version
  }
}
```
[Demo of this query](https://latest-with-plugins.datasette.io/graphql?query=%7B%0A%20%20packages%20%7B%0A%20%20%20%20name%0A%20%20%20%20version%0A%20%20%7D%0A%7D).

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-packages
    python3 -mvenv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
