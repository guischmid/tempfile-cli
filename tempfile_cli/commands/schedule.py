import argparse
import subprocess
import shutil

def register(subparsers: argparse._SubParsersAction) -> None:
    """Register the ``schedule`` subcommand to install a cron job."""
    parser = subparsers.add_parser("schedule", help="Install a cron job for automatic cleaning")
    parser.add_argument(
        "interval",
        nargs="?",
        choices=["daily", "weekly"],
        default="daily",
        help="Set the cleaning interval (default: daily)",
    )
    parser.set_defaults(handler=handle)

def handle(args: argparse.Namespace) -> None:
    """Install a daily or weekly cron entry for automatic cleaning."""
    if not shutil.which("tempfile"):
        print("❌ 'tempfile' command not found in PATH. Please install it first.")
        return

    cron_timing = "@daily" if args.interval == "daily" else "@weekly"
    cron_command = f"tempfile clean"
    cron_line = f"{cron_timing} {cron_command}"

    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True,
            check=False,
        )
        current_cron = result.stdout if result.returncode == 0 else ""

        if cron_line in current_cron:
            print("✅ Cron job already installed.")
            return

        new_cron = f"{current_cron.strip()}\n{cron_line}\n"

        subprocess.run(
            ["crontab", "-"],
            input=new_cron,
            text=True,
            check=True,
        )
        print(f"✅ Installed {args.interval} cleaning cron job:")
        print(f"   {cron_line}")

    except Exception as e:
        print(f"❌ Failed to install cron job: {e}")
