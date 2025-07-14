import argparse
import os
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from tempfile_cli.core.utils import (
    ensure_dir,
    load_metadata,
    save_metadata,
    TEMPFILE_DIR,
    load_config,
)

# Load user configuration
config = load_config()
default_days = int(config.get("default_days", 30))


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the ``new`` subcommand for creating a tempfile."""
    parser = subparsers.add_parser("new", help="Create a new tempfile")
    parser.add_argument("name", nargs="?", help="Optional name for the file")
    parser.add_argument("--tag", action="append", help="Add one or more tags")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Create a new tempfile, record metadata and open it."""
    try:
        ensure_dir(TEMPFILE_DIR)
    except OSError as e:
        print(f"Error creating directory {TEMPFILE_DIR}: {e}")
        return

    filename = args.name or datetime.now().strftime("%Y-%m-%d_%H%M%S")
    if not filename.endswith(".txt"):
        filename += ".txt"

    file_path = TEMPFILE_DIR / filename

    if file_path.exists():
        print(f"File already exists: {file_path}")
        return

    try:
        file_path.touch(exist_ok=False)
        now = datetime.now()

        metadata = load_metadata()
        metadata[filename] = {
            "created": now.isoformat(),
            "expires": (now + timedelta(days=default_days)).isoformat(),
            "tags": args.tag or [],
        }
        save_metadata(metadata)

        print(f"✅ Created: {file_path}")

        editor = os.getenv("EDITOR", "nano")
        subprocess.call([editor, str(file_path)])

    except OSError as e:
        print(f"Error creating file {file_path}: {e}")
