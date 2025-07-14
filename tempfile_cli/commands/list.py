import argparse
from datetime import datetime
from tempfile_cli.core.utils import load_metadata, TEMPFILE_DIR
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)


def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the ``list`` subcommand to show stored tempfiles."""
    parser = subparsers.add_parser("list", help="List all tempfiles")
    parser.add_argument("--tag", help="Only show notes containing this tag")
    parser.set_defaults(handler=handle)


def handle(args: argparse.Namespace) -> None:
    """Display stored tempfiles with optional tag filtering."""
    try:
        metadata = load_metadata()
    except FileNotFoundError:
        print("No tempfiles found.")
        return

    if not metadata:
        print("No tempfiles found.")
        return

    if args.tag:
        filtered_metadata = {
            fname: info
            for fname, info in metadata.items()
            if args.tag in info.get("tags", [])
        }
    else:
        filtered_metadata = metadata

    if not filtered_metadata:
        print(f"No tempfiles found with tag '{args.tag}'.")
        return

    # Sort by created date
    entries = sorted(
        filtered_metadata.items(),
        key=lambda item: datetime.fromisoformat(item[1].get("created")),
    )

    print("🗒️ Tempfiles:\n")
    for fname, info in entries:
        file_path = TEMPFILE_DIR / fname
        try:
            size_kb = file_path.stat().st_size / 1024 if file_path.exists() else 0
            status = "✅ exists" if file_path.exists() else "❌ missing"
        except FileNotFoundError:
            size_kb = 0
            status = "❌ missing"

        created = datetime.fromisoformat(info["created"]).strftime("%Y-%m-%d %H:%M")
        expires = datetime.fromisoformat(info["expires"]).strftime("%Y-%m-%d %H:%M")
        tags = ", ".join(info.get("tags", []))

        print(f"{Fore.GREEN}📄 {fname}{Style.RESET_ALL}")
        print(f"{Style.DIM}    created: {created}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    expires: {expires}{Style.RESET_ALL}")
        if tags:
            print(f"{Fore.MAGENTA}    tags   : {tags}{Style.RESET_ALL}")
        print(f"    status : {status}")
        print(f"    size   : {size_kb:.1f} KB\n")

