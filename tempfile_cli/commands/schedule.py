import os
import sys
import subprocess
from pathlib import Path

def register(subparsers):
    """Register the ``schedule`` subcommand to install a cron job."""
    parser = subparsers.add_parser("schedule", help="Install a cron job for automatic cleaning")
    parser.set_defaults(handler=handle)
    parser.add_argument(
        "interval",
        nargs="?",
        choices=["daily", "weekly"],
        help="Set the cleaning interval (default: daily)"
    
    )

def handle(args):
    """Install a daily or weekly cron entry for automatic cleaning."""
    # Determine python executable and main.py path
    python_exec = sys.executable
    project_dir = Path(__file__).resolve().parent.parent
    main_path = project_dir / "main.py"

    if args.interval == "daily":
        cron_timing = "@daily"
    elif args.interval == "weekly":
        cron_timing = "@weekly"
    else:
        cron_timing = "@daily"  # fallback
        
    cron_line = f"{cron_timing} tempfile clean"

    if not main_path.exists():
        print("❌ Could not locate main.py")
        return

    cron_line = "@daily tempfile clean"

    try:
        # Read current crontab
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current_cron = result.stdout if result.returncode == 0 else ""

        if cron_line in current_cron:
            print("✅ Cron job already installed.")
            return

        # Add new line
        new_cron = current_cron.strip() + "\n" + cron_line + "\n"

        # Apply new crontab
        subprocess.run(["crontab", "-"], input=new_cron, text=True)
        print("✅ Installed daily cleaning cron job:")
        print(f"   {cron_line}")

    except Exception as e:
        print("❌ Failed to install cron job:", e)
