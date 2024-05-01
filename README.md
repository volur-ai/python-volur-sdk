# Volur AI SDK

This is the Python SDK for the Volur AI platform. It provides a set of tools to
interact with the Volur AI API.

## Install

This library can be installed as a Python package using `pip` or any other
Python package manager (Poetry, Rye, uv, etc.).

```shell
pip install git+ssh://git@github.com/volur-ai/python-volur-ai-sdk.git@main
```

or using `https` protocol:

```shell
pip install git+https://github.com/volur-ai/python-volur-ai-sdk.git@main
```

## How to use the library

See the [documentation](https://congenial-carnival-wopj8rk.pages.github.io/).

To see the examples of how to use the library, please refer to the
`examples` folder.

## Prerequisites

When developing this SDK, you choose between **containerized** and **local** development.

### Pre-requisites for containerized development

- [Earthly][earthly] ([docs][earthly-documentation]).

### Pre-requisites for local development

- Python (>=3.11, <3.12),
- [just][just] ([docs][just-documentation]),
- [Poetry][poetry] ([docs][poetry-documentation]),
- [Poetry Upgrade Plugin][poetry-plugin-upgrade] ([docs][poetry-plugin-upgrade-documentation]),
- [buf][buf] ([docs][buf-documentation]),

[earthly]: https://github.com/earthly/earthly
[earthly-documentation]: https://docs.earthly.dev/
[just]: https://github.com/casey/just
[just-documentation]: https://just.systems/man/en/
[poetry]: https://github.com/python-poetry/poetry
[poetry-documentation]: https://python-poetry.org/docs/
[poetry-plugin-upgrade]: https://github.com/apoclyps/poetry-plugin-upgrade
[poetry-plugin-upgrade-documentation]: https://github.com/apoclyps/poetry-plugin-upgrade?tab=readme-ov-file#poetry-plugin-upgrade
[buf]: https://github.com/bufbuild/buf
[buf-documentation]: https://buf.build/docs/introduction

## Reference guide
The Client SDK Reference Guide can be found in the interactive notebook `client_SDK_reference_guide.ipynb`. Here you'll find general usage information about the SDK.

To open the notebook, simply run

```shell
poetry run jupyter notebook
```

and select the reference guide notebook.

You'll need an authentication token to be able to run the notebook. Please contact us and a token will be issued to you.

## Development

## Configure

This command will install required Python dependencies:

```shell
just configure
```

or

```shell
earthly +configure
```

### Formatting, linting, type checking and testing

We use a set of tools to improve the quality of our code:

- `ruff` as Python linter and code formatter,
- `mypy` for type checking

You can run these tools with `just` or `Earthly`.

#### Static validation

```shell
just validate
```

or

```shell
earthly +validate
```

#### Resolve auto-fixable issues

```shell
just fix
```

or

```shell
earthly +fix
```

### Run tests

```shell
just test
```

or

```shell
earthly +test
```

## Other useful commands

You can list all available recipes by running:

```shell
just
```

or

```shell
earthly ls
```

## Documentation

We use [`google`][google-docstrings]-style docstrings in our code. The
documentation is generated using:

[google-docstrings]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

- https://github.com/mkdocstrings/python,
- https://github.com/squidfunk/mkdocs-material.

### Generate documentation

We use the [mkdocs-gen-files](https://github.com/oprypin/mkdocs-gen-files) plugin to programmatically generate documentation
pages during build.

To generate documentation, run:

```shell
just build-docs
```

or

```shell
earthly +build-docs
```

#### Serve documentation website

> [!WARNING]
> It is not possible to use container based development for documentation serving.

```shell
just serve-docs
```

And then open your browser using the provided link in the output.

#### Accessing documentation

Documentation is available at [docs.volur.ai](https://docs.volur.ai).
