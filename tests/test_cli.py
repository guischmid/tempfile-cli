import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tempfile_cli.commands import new


def make_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    new.register(subparsers)
    return parser


def test_new_argparse():
    parser = make_parser()
    args = parser.parse_args(["new", "example.txt", "--tag", "a", "--tag", "b"])
    assert args.command == "new"
    assert args.name == "example.txt"
    assert args.tag == ["a", "b"]
    assert args.handler == new.handle
