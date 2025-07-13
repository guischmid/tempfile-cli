from datetime import datetime, timedelta
from tempfile_cli.core.utils  import load_metadata, save_metadata, TEMPFILE_DIR, load_config

def register(subparsers):
    # Register the 'clean' subcommand
    parser = subparsers.add_parser("clean", help="Delete old tempfiles")
    default_days = int(load_config().get("default_days", 30))  # fallback = 30
    parser.add_argument("days", nargs="?", type=int, default=default_days,
                        help=f"Delete files older than this many days (default: {default_days})")
    parser.set_defaults(handler=handle)

def handle(args):
    now = datetime.now()
    metadata = load_metadata()

    if not metadata:
        print("No tempfiles to clean.")
        return

    cutoff = now - timedelta(days=args.days)
    to_delete = [
        fname for fname, info in metadata.items()
        if datetime.fromisoformat(info["created"]) < cutoff
    ]

    if not to_delete:
        print(f"No tempfiles older than {args.days} days.")
        return

    for fname in to_delete:
        file_path = TEMPFILE_DIR / fname
        if file_path.exists():
            file_path.unlink()
            print(f"🗑  Deleted: {file_path}")
        del metadata[fname]

    save_metadata(metadata)
