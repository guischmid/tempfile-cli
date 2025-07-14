import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tempfile_cli.core import utils


def test_metadata_roundtrip(tmp_path, monkeypatch):
    metadata_file = tmp_path / "metadata.json"
    monkeypatch.setattr(utils, "METADATA_FILE", metadata_file)
    data = {"foo": 1, "bar": {"baz": 2}}
    utils.save_metadata(data)
    loaded = utils.load_metadata()
    assert loaded == data
