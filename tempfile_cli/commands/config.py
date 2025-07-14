import argparse
from tempfile_cli.core.utils import load_config, save_config

def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the ``config`` subcommand for managing preferences."""
    parser = subparsers.add_parser("config", help="Get or set user preferences")
    parser.add_argument("action", choices=["get", "set"], help="Get or set a config value")
    parser.add_argument("key", help="The config key to access")
    parser.add_argument("value", nargs="?", help="The value to set (only for 'set')")
    parser.set_defaults(handler=handle)

def handle(args: argparse.Namespace) -> None:
    """Retrieve or update configuration values."""
    config = load_config()

    if args.action == "get":
        value = config.get(args.key)
        if value is None:
            print(f"❌ Key '{args.key}' not found.")
        else:
            print(f"{args.key} = {value}")

    elif args.action == "set":
        if args.value is None:
            print("❌ You must provide a value to set.")
            return
        config[args.key] = args.value
        save_config(config)
        print(f"✅ {args.key} set to {args.value}")
