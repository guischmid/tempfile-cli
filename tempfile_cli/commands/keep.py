import argparse
from pathlib import Path
from tempfile_cli.core.utils import (
    load_metadata,
    save_metadata,
    ensure_dir,
    TEMPFILE_DIR,
)

# Target directory for keeping important notes
KEEP_DIR = Path.home() / "Documents" / "tempfile_kept"

def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the ``keep`` subcommand for archiving a tempfile."""
    parser = subparsers.add_parser("keep", help="Move file to permanent location")
    parser.add_argument("name", help="Name of the file to keep")
    parser.set_defaults(handler=handle)

def handle(args: argparse.Namespace) -> None:
    """Move the given tempfile to a permanent location."""
    try:
        ensure_dir(KEEP_DIR)
    except OSError as e:
        print(f"Error creating directory {KEEP_DIR}: {e}")
        return

    metadata = load_metadata()

    filename = args.name
    source = TEMPFILE_DIR / filename
    target = KEEP_DIR / filename

    if not source.exists():
        print(f"❌ File not found: {source}")
        return

    try:
        source.rename(target)
        metadata.pop(filename, None)
        save_metadata(metadata)
        print(f"📦 Moved to: {target}")
    except OSError as e:
        print(f"Error moving file: {e}")
