import argparse
from tempfile_cli.commands import new, list, clean, keep, edit, config, schedule

def main():
    parser = argparse.ArgumentParser(description="Manage temporary scratchpad files.")
  
    subparsers = parser.add_subparsers(dest="command")

    new.register(subparsers)
    list.register(subparsers)
    clean.register(subparsers)
    keep.register(subparsers)
    edit.register(subparsers)
    config.register(subparsers)
    schedule.register(subparsers)

    args = parser.parse_args()
    

  
    if args.command:
        args.handler(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
