# -*- coding: utf-8 -*-

"""Main module."""

import glob
import os
import platform
import shutil
import subprocess
import tempfile
import typing

protoc_version = "3.11.2"
grpc_web_plugin_version = "1.0.7"
protoc_release_base_url = (
    "https://github.com/protocolbuffers/protobuf/releases/download"
)
grpc_web_plugin_release_base_url = "https://github.com/grpc/grpc-web/releases/download"


def print_command(
    *cmd_args: typing.Any, verbosity: int = 0, **cmd_kwargs: typing.Any
) -> None:
    try:
        output = subprocess.check_output(*cmd_args, **cmd_kwargs).decode("utf-8")
        if verbosity > 1:
            print(output)
    except subprocess.CalledProcessError as e:  # pragma: no cover
        print(e.returncode)
        print(e.output)
        raise


def quote(s: str) -> str:
    return '"' + s + '"'


def proto_compile(
    proto_source_dir: str,
    output_dir: str,
    js_out_options: typing.Optional[str] = None,
    grpc_web_out_options: typing.Optional[str] = None,
    clear_output_dir: bool = False,
    verbosity: int = 0,
) -> None:
    abs_source = os.path.abspath(proto_source_dir)
    abs_output = os.path.abspath(output_dir)
    proto_files = glob.glob(abs_source + "/*.proto")
    if not len(proto_files) > 0:
        raise AssertionError(
            "Source directory " + abs_source + " must contain .proto file(s)"
        )

    tmp_dir = tempfile.mkdtemp()
    try:
        # Download correct files
        system = platform.system().lower()  # darwin
        system_alias = "osx" if system == "darwin" else system  # osx for darwin
        # url configs for windows
        if system == "windows":
            system_alias = "win64"
            machine_arch = ""
            machine_arch_grpc = "x86_64"
        else:
            machine_arch = platform.machine()
            machine_arch_grpc = platform.machine()

        if verbosity > 0:
            print(system_alias)
        protoc_release_url = protoc_release_base_url
        protoc_release_url += "/v" + protoc_version
        protoc_release_url += (
            "/protoc-"
            + protoc_version
            + "-"
            + system_alias
            + ("" if system == "windows" else "-")
            + machine_arch
            + ".zip"
        )

        grpc_web_plugin_release_url = grpc_web_plugin_release_base_url
        grpc_web_plugin_release_url += "/" + grpc_web_plugin_version
        grpc_web_plugin_release_url += (
            "/protoc-gen-grpc-web-"
            + grpc_web_plugin_version
            + "-"
            + system
            + "-"
            + machine_arch_grpc
            + (".exe" if system == "windows" else "")
        )

        download = dict(
            protoc=protoc_release_url, protoc_gen_grpc_web=grpc_web_plugin_release_url
        )

        for executable, url in download.items():
            filename = os.path.basename(url)
            is_zip = os.path.splitext(filename)[1].lower() == ".zip"
            download_command = str(" ").join(
                [
                    "wget",
                    "-O",
                    tmp_dir + "/" + (filename if is_zip else executable),
                    quote(url),
                ]
            )
            if verbosity > 0:
                print(download_command)
            print_command(
                download_command,
                stderr=subprocess.STDOUT,
                shell=True,
                verbosity=verbosity,
            )
            if is_zip:
                unzip_command = str(" ").join(
                    [
                        "unzip",
                        tmp_dir + "/" + filename,
                        "-d",
                        tmp_dir + "/" + executable,
                    ]
                )
                if verbosity > 0:
                    print(unzip_command)
                print_command(
                    unzip_command,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    verbosity=verbosity,
                )

        # Make executables
        for executable in [
            tmp_dir + "/protoc/bin/protoc",
            tmp_dir + "/protoc_gen_grpc_web",
        ]:
            chmod_command = str(" ").join(["chmod", "+x", executable])
            if verbosity > 0:
                print(chmod_command)
            print_command(
                chmod_command, stderr=subprocess.STDOUT, shell=True, verbosity=verbosity
            )

        print_command(
            "ls -la " + tmp_dir,
            stderr=subprocess.STDOUT,
            shell=True,
            verbosity=verbosity,
        )

        # Construct protoc compiler command
        # See: https://github.com/grpc/grpc-web
        proto_command = [
            tmp_dir + "/protoc/bin/protoc",
            "-I=" + abs_source,
        ] + proto_files
        proto_command.append(
            "--plugin=protoc-gen-grpc-web=" + tmp_dir + "/protoc_gen_grpc_web"
        )

        proto_command.append(
            "--js_out="
            + ((js_out_options + ":") if js_out_options else "")
            + abs_output
        )

        proto_command.append(
            "--grpc-web_out="
            + ((grpc_web_out_options + ":") if grpc_web_out_options else "")
            + abs_output
        )

        # Eventually clear the output dir
        if os.path.exists(abs_output) and clear_output_dir:
            shutil.rmtree(abs_output, ignore_errors=True)

        # Make sure the output path exists
        if not os.path.exists(abs_output):
            os.makedirs(abs_output)

        if verbosity > 0:
            print(str(" ").join(proto_command))
        print_command(
            str(" ").join(proto_command),
            stderr=subprocess.STDOUT,
            shell=True,
            verbosity=verbosity,
        )

    finally:
        # Remove temporary directory
        shutil.rmtree(tmp_dir, ignore_errors=True)
