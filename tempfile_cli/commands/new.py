import os
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from tempfile_cli.core.utils  import ensure_dir, load_metadata, save_metadata, TEMPFILE_DIR, METADATA_FILE, load_config

# Load user configuration
config = load_config()
default_days = int(config.get("default_days", 30))  # fallback = 30


def register(subparsers):
    """Register the ``new`` subcommand for creating a tempfile."""
    parser = subparsers.add_parser("new", help="Create a new tempfile")
    parser.add_argument("name", nargs="?", help="Optional name for the file")
    parser.add_argument("--tag", action="append", help="Add one or more tags")
    parser.set_defaults(handler=handle)


def handle(args):
    """Create a new tempfile, record metadata and open it."""
   

    # Ensure the directory exists
    ensure_dir(TEMPFILE_DIR)

    # Determine filename
    filename = args.name or datetime.now().strftime("%Y-%m-%d_%H%M")
    filename += ".txt"
    file_path = TEMPFILE_DIR / filename

    # Create the file
    file_path.touch(exist_ok=True)
    now = datetime.now()
    

    # Update metadata
    metadata = load_metadata()
    metadata[filename] = {
        "created": now.isoformat(),
        "expires": (now + timedelta(days=default_days)).isoformat(),
        "tags": args.tag or []
    }
    save_metadata(metadata)

    print(f"✅ Created: {file_path}")

    # Open file in editor
    editor = os.getenv("EDITOR", "nano")
    subprocess.call([editor, str(file_path)])
