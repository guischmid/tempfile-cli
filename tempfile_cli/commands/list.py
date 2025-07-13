from datetime import datetime
from tempfile_cli.core.utils import load_metadata, TEMPFILE_DIR
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)


# List all tempfiles with their metadata
def register(subparsers):
    # Register the 'list' subcommand
    parser = subparsers.add_parser("list", help="List all tempfiles")
    parser.add_argument(
        "--tag",
        help="Only show notes containing this tag"
    )
    parser.set_defaults(handler=handle)

# Handle the 'list' command
def handle(args):
    metadata = load_metadata()
    if not metadata:
        print("No tempfiles found.")
        return

    filtered = {}
    if args.tag:
        # Only keep entries whose tags list contains args.tag
        for fname, info in metadata.items():
            tags = info.get("tags", [])
            if args.tag in tags:
                filtered[fname] = info
    else:
        filtered = metadata

    if not filtered:
        print(f"No tempfiles found with tag '{args.tag}'.")
        return

    entries = list(filtered.items())

    # Sort by created date (default)
    entries.sort(key=lambda item: item[1].get("created", ""))

    print("🗒  Tempfiles:\n")
    for fname, info in entries:
        # Calculate the size of a tempfile in KB
        file_path = TEMPFILE_DIR / fname
        size_kb = (
            file_path.stat().st_size / 1024
            if file_path.exists()
            else 0
        )
        created = datetime.fromisoformat(info["created"]).strftime("%Y-%m-%d %H:%M")
        expires = datetime.fromisoformat(info["expires"]).strftime("%Y-%m-%d %H:%M")
        tags = info.get("tags", [])
        status = "✅ exists" if file_path.exists() else "❌ missing"

        print(Fore.GREEN + f"📄 {fname}")
        print(Style.DIM + f"    created: {created}")
        print(Fore.CYAN + f"    expires: {expires}")
        if tags:
            print(Fore.MAGENTA + f"    tags   : {', '.join(tags)}")
        print(f"    status : {status}\n")
        print(f"    size   : {size_kb:.1f} KB")

