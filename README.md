# Volur AI SDK
This is the client API SDK written in Python which we will send to customers to install so they can use the API to upload data. Here you'll find the client, in addition to some examples of how to use the library. 

## Prerequisites

- Python (>=3.11, <3.12),
- [Poetry][poetry] ([docs][poetry-documentation])

[poetry]: https://github.com/python-poetry/poetry
[poetry-documentation]: https://python-poetry.org/docs/
[azure-cli]: https://github.com/Azure/azure-cli
[azure-cli-documentation]: https://learn.microsoft.com/en-us/cli/azure/
[make]: https://github.com/mirror/make
[make-documentation]: https://www.gnu.org/software/make/manual/html_node/index.html

## Configure

This command will install required Python dependencies:

```shell
make configure
```

## Reference guide
The Client SDK Reference Guide can be found in the interactive notebook `client_SDK_reference_guide.ipynb`. Here you'll find general usage information about the SDK.

To open the notebook, simply run

```shell
poetry run jupyter notebook
```

and select the reference guide notebook.

You'll need an authentication token to be able to run the notebook. Please contact us and a token will be issued to you.

## Development

### Formatting, linting, type checking and testing

We use a set of tools to improve the quality of our code:

- `ruff` as Python linter and code formatter,
- `mypy` for type checking

You can run these tools with `Make`.

#### Static validation

```shell
make validate
```

#### Resolve auto-fixable issues

```shell
make validate-fix
```

## Documentation

### Generate pages for client docs

We use the [mkdocs-gen-files](https://github.com/oprypin/mkdocs-gen-files) plugin to programmatically generate documentation pages during build.

#### Build and serve docs

```shell
mkdocs build
```

```shell
mkdocs serve --dev-addr="0.0.0.0:8000"
```

The docs should be available on http://0.0.0.0:8000/.
