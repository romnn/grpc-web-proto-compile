#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `grpc_web_proto_compile` package."""

import os
import shlex
import shutil
import tempfile
import typing
from contextlib import contextmanager
from distutils.dir_util import copy_tree

import pytest
from click.testing import CliRunner

from grpc_web_proto_compile import cli, grpc_web_proto_compile

samples_path = os.path.join(os.path.dirname(__file__), "sample")


@contextmanager
def test_harness() -> typing.Iterator[typing.Tuple[str, str]]:
    with tempfile.TemporaryDirectory() as test_dir:
        proto_dir = os.path.join(test_dir, "protos")
        out_dir = os.path.join(test_dir, "out")
        copy_tree(samples_path, proto_dir)
        try:
            yield proto_dir, out_dir
        finally:
            # Cleanup will be taken care of by tempfile
            pass


def test_command_line_interface_verbosity() -> None:
    with test_harness() as (proto_dir, out_dir):
        assert os.path.exists(os.path.join(proto_dir, "person.proto"))
        runner = CliRunner()
        v0 = runner.invoke(
            cli.main, args=shlex.split(f"--verbosity=0 {proto_dir} {out_dir}")
        )
        v1 = runner.invoke(
            cli.main, args=shlex.split(f"--verbosity=1 {proto_dir} {out_dir}")
        )
        v2 = runner.invoke(
            cli.main, args=shlex.split(f"--verbosity=2 {proto_dir} {out_dir}")
        )
        assert v0.exit_code == v1.exit_code == v2.exit_code == 0
        assert len(v0.output) < len(v1.output) < len(v2.output)


def test_command_line_clear_output() -> None:
    runner = CliRunner()
    with test_harness() as (proto_dir, out_dir):
        copy_tree(samples_path, out_dir)
        assert os.path.exists(os.path.join(out_dir, "person.proto"))
        assert not os.path.exists(os.path.join(out_dir, "person_pb.js"))
        assert (
            runner.invoke(cli.main, args=["-clear", proto_dir, out_dir]).exit_code == 0
        )
        assert not os.path.exists(os.path.join(out_dir, "person.proto"))
        assert os.path.exists(os.path.join(out_dir, "person_pb.js"))


def test_command_line_interface() -> None:
    runner = CliRunner()
    missing_args = runner.invoke(cli.main)
    assert missing_args.exit_code != 0
    with test_harness() as (proto_dir, out_dir):
        no_sources = runner.invoke(cli.main, args=[out_dir, out_dir])
        assert no_sources.exit_code != 0
        valid = runner.invoke(cli.main, args=[proto_dir, out_dir])
        assert valid.exit_code == 0
        assert os.path.exists(os.path.join(out_dir, "person_pb.d.ts"))
        assert os.path.exists(os.path.join(out_dir, "person_pb.js"))
