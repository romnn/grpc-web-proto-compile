===============================
grpc-web-proto-compile
===============================

.. image:: https://travis-ci.com/romnnn/grpc-web-proto-compile.svg?branch=master
        :target: https://travis-ci.com/romnnn/grpc_web_proto_compile
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/grpc-web-proto-compile.svg
        :target: https://pypi.python.org/pypi/grpc-web-proto-compile
        :alt: PyPI version

.. image:: https://img.shields.io/github/license/romnnn/grpc-web-proto-compile
        :target: https://github.com/romnnn/grpc-web-proto-compile
        :alt: License

.. image:: https://readthedocs.org/projects/grpc-web-proto-compile/badge/?version=latest
        :target: https://grpc-web-proto-compile.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/romnnn/grpc-web-proto-compile/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnnn/grpc-web-proto-compile
        :alt: Test Coverage

""""""""

This is a small script tailored to be used in CI environments and piplines to completely take care of generating typescript grpc stubs from protobuf files.

.. code-block:: console

    $ pip install grpc_web_proto_compile

To compile a directory with your proto files, simply run:

.. code-block:: console

    $ grpc_web_proto_compile path/to/your/proto/sources ./out

If you cloned the repository, the command looks like:

.. code-block:: console
    
    $ git clone https://github.com/romnnn/grpc-web-proto-compile
    $ cd grpc-web-proto-compile/
    $ python -m grpc_web_proto_compile.cli ./tests/sample/ ./out

See the `official documentation`_ for more information.

.. _official documentation: https://grpc-web-proto-compile.readthedocs.io

.. code-block:: python

    import grpc_web_proto_compile

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
