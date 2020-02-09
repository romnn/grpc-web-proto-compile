=====
Usage
=====

To use grpc-web-proto-compile in your CI pipeline:

.. code-block:: console

    $ grpc_web_proto_compile path/to/your/proto/sources ./out

You can also configure compiler options:

.. code-block:: console

    $ grpc_web_proto_compile --clear_output_dir --verbosity=1 --js_out_options="import_style=commonjs,binary" --grpc_web_out_options="import_style=typescript,mode=grpcwebtext" path/to/your/proto/sources ./out