# -*- coding: utf-8 -*-

"""Console script for grpc_web_proto_compile."""
import os
import sys

import click

import grpc_web_proto_compile.grpc_web_proto_compile


def valid_dir(ctx: click.core.Context, param: click.core.Parameter, value: str) -> str:
    if os.path.exists(value) and os.path.isdir(value):
        return value
    raise click.BadParameter(
        'Directory "' + value + '" does not exist.', ctx=ctx, param=param
    )


@click.command()
@click.argument("proto_source_dir", callback=valid_dir, type=click.Path())
@click.argument("output_dir", type=click.Path())
@click.option(
    "--js_out_options",
    default="import_style=commonjs,binary",
    help=("options for the javascript proto compiler"),
)
@click.option(
    "--grpc_web_out_options",
    default="import_style=typescript,mode=grpcwebtext",
    help=("options for the grpc web proto compiler"),
)
@click.option(
    "--clear_output_dir",
    "-clear",
    is_flag=True,
    default=False,
    help=("whether to clear the output directory before compilation"),
)
@click.option(
    "--verbosity",
    default=0,
    help=("level of verbosity when printing to stdout (the higher the more output)"),
)
def main(
    proto_source_dir: str,
    output_dir: str,
    js_out_options: str,
    grpc_web_out_options: str,
    clear_output_dir: bool,
    verbosity: int,
) -> int:
    """Console script for grpc_web_proto_compile."""
    try:
        grpc_web_proto_compile.grpc_web_proto_compile.proto_compile(
            proto_source_dir=proto_source_dir,
            output_dir=output_dir,
            js_out_options=js_out_options,
            grpc_web_out_options=grpc_web_out_options,
            clear_output_dir=clear_output_dir,
            verbosity=verbosity,
        )
    except Exception as e:  # pragma: no cover
        raise click.ClickException(str(e))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
