===============================
grpc-web-proto-compile
===============================

.. image:: https://github.com/romnn/grpc-web-proto-compile/workflows/test/badge.svg
        :target: https://github.com/romnn/grpc-web-proto-compile/actions
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/grpc-web-proto-compile.svg
        :target: https://pypi.python.org/pypi/grpc-web-proto-compile
        :alt: PyPI version

.. image:: https://img.shields.io/github/license/romnn/grpc-web-proto-compile
        :target: https://github.com/romnn/grpc-web-proto-compile
        :alt: License

.. image:: https://codecov.io/gh/romnn/grpc-web-proto-compile/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnn/grpc-web-proto-compile
        :alt: Test Coverage

""""""""

This is a small script tailored to be used in CI environments and piplines to completely take care of generating typescript grpc stubs from protobuf files.

.. code-block:: console

    $ pip install grpc_web_proto_compile

To compile a directory with your proto files, simply run:

.. code-block:: console

    $ grpc_web_proto_compile path/to/your/proto/sources ./out
    $ grpc_web_proto_compile --help # For a list of available options

If you cloned the repository, the command looks like:

.. code-block:: console
    
    $ git clone https://github.com/romnn/grpc-web-proto-compile
    $ cd grpc-web-proto-compile/
    $ python -m grpc_web_proto_compile.cli ./tests/sample/ ./out

Development
-----------

For detailed instructions see `CONTRIBUTING <CONTRIBUTING.rst>`_.

Tests
~~~~~~~
You can run tests with

.. code-block:: console

    $ invoke test
    $ invoke test --min-coverage=90     # Fail when code coverage is below 90%
    $ invoke type-check                 # Run mypy type checks

Linting and formatting
~~~~~~~~~~~~~~~~~~~~~~~~
Lint and format the code with

.. code-block:: console

    $ invoke format
    $ invoke lint

All of this happens when you run ``invoke pre-commit``.

Note
-----

This project is still in the alpha stage and should not be considered production ready.
