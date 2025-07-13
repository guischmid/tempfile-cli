# tempfile-cli

 A minimalist scratchpad CLI that creates temporary text files in your terminal — with auto-expiration, optional tags, and a built-in cleanup system.

##  Features

- Create temporary `.txt` files with optional names
- Automatically expire and clean files after X days
- Tag and list notes
- Configure expiry defaults and cleanup behavior
- Edit files directly in your `$EDITOR`

---

## 🍺 Install via Homebrew

> Works on macOS and Linux (with Homebrew installed)

```bash
brew install guischmid/tap/tempfile
````
Then run:
```bash
tempfile new
tempfile list
```

## Build and run natively (Python 3.11+)

Clone and install in editable mode:
```bash
git clone https://github.com/guischmid/tempfile-cli.git
cd tempfile-cli
pip install -e .
```
Now you can run the CLI from anywhere
```bash
tempfile new "journal"
```
## Example Commands
```bash
tempfile new                # Creates a timestamped note and opens $EDITOR
tempfile new todo.txt       # Creates note named todo.txt
tempfile list               # Lists all notes with metadata
tempfile clean 10           # Deletes notes older than 10 days
tempfile config set expiry 14   # Sets default expiry to 14 days
```
## Files are stored in:
```bash 
~/.tempfiles/
```
With metadata in `~/.tempfiles/metadata.json`

## Roadmap
-[] Modular architecture
-[] Configurable default expiry
-[] Tag support (soon)
-[] Archive / keep forever mode
-[] Sync or backup to cloud folder
-[] Shell autocompletion

## License

MIT- use freely, contribute if you like