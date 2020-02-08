===============================
grpc-web-proto-compile
===============================

.. image:: https://travis-ci.com/romnnn/grpc_web_proto_compile.svg?branch=master
        :target: https://travis-ci.com/romnnn/grpc_web_proto_compile
        :alt: Build Status

.. image:: https://img.shields.io/pypi/v/grpc_web_proto_compile.svg
        :target: https://pypi.python.org/pypi/grpc_web_proto_compile
        :alt: PyPI version

.. image:: https://img.shields.io/github/license/romnnn/grpc_web_proto_compile
        :target: https://github.com/romnnn/grpc_web_proto_compile
        :alt: License

.. image:: https://readthedocs.org/projects/grpc-web-proto-compile/badge/?version=latest
        :target: https://grpc-web-proto-compile.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/romnnn/grpc_web_proto_compile/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/romnnn/grpc_web_proto_compile
        :alt: Test Coverage

""""""""

Your short description here. `romnnn.github.io/grpc_web_proto_compile <https://romnnn.github.io/grpc_web_proto_compile>`_

.. code-block:: console

    $ pip install grpc_web_proto_compile

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
