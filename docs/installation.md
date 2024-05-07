# Installation

## Requirements

This library is compatible with **Python 3.11**.

Please make sure that you are using a correct version of Python before
installing the library.

```shell
python --version
```

## Installing a library

!!! info "This library is not yet available on PyPI"
    You can install it directly from the GitHub repository. See the
    instructions for a specific package manager below.

This library can be installed using `pip`, `poetry`, or any other popular
Python package manager as a Git dependency.

### Using `pip`

For installing the library using `pip`, you can use the following command:

=== "SSH"

    ```shell
    pip install git+ssh://git@github.com/volur-ai/python-volur-ai-sdk.git@main
    ```

=== "HTTPS"

    ```shell
    pip install git+https://github.com/volur-ai/python-volur-ai-sdk.git@main
    ```

For more information on installing packages from Git repositories using `pip`,
please refer to the [VCS Support][pip-vcs-support] section of the `pip`
documentation.

[pip-vcs-support]: https://pip.pypa.io/en/stable/topics/vcs-support

### Using `poetry`

For installing the library using `poetry`, you can use the following command:

=== "SSH"

    ```shell
    poetry add git+ssh://git@github.com/volur-ai/python-volur-ai-sdk.git@main
    ```

=== "HTTPS"

    ```shell
    poetry add git+https://github.com/volur-ai/python-volur-ai-sdk.git@main
    ```

For more information on installing packages from Git repositories using
`poetry`, please refer to the [`git`-dependencies][poetry-git-dependencies]
section of the `poetry` documentation.

[poetry-git-dependencies]: https://python-poetry.org/docs/dependency-specification/#git-dependencies
