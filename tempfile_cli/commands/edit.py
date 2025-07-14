import argparse
import os
import subprocess
from tempfile_cli.core.utils import TEMPFILE_DIR

def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the ``edit`` subcommand to open a tempfile."""
    parser = subparsers.add_parser("edit", help="Open an existing tempfile in your editor")
    parser.add_argument("name", help="Filename to edit (e.g. 2025-07-13_1834.txt)")
    parser.set_defaults(handler=handle)

def handle(args: argparse.Namespace) -> None:
    """Open the specified tempfile in the user's editor."""
    file_path = TEMPFILE_DIR / args.name

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    editor = os.getenv("EDITOR", "nano")
    try:
        subprocess.call([editor, str(file_path)])
    except FileNotFoundError:
        print(f"Editor '{editor}' not found. Please set your EDITOR environment variable.")
    except Exception as e:
        print(f"Error opening editor: {e}")
