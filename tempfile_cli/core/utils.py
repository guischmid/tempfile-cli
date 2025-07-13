import json
from pathlib import Path

# Path to the directory that stores all temporary files
TEMPFILE_DIR = Path.home() / ".tempfiles"

# Path to the metadata.json file
METADATA_FILE = TEMPFILE_DIR / "metadata.json"

# Global user config
CONFIG_FILE = Path.home() / ".tempfile_config.json"

# Ensure the TEMPFILE_DIR exists
def ensure_dir(path: Path):
    """
    Ensure the given directory exists.
    Creates the directory (and parents) if needed.
    """
    path.mkdir(parents=True, exist_ok=True)

# Load and save metadata for tempfiles
def load_metadata():
    """
    Load metadata from metadata.json, or return empty dict if not found or broken.
    """
    try:
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_metadata(metadata: dict):
    """
    Save metadata dictionary to metadata.json.
    """
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)


# Load and save user configuration
def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_config(config: dict):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
