#!/usr/bin/env python3
"""Run the template community reader with this project's organized private destination."""
from pathlib import Path
import importlib.util
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
template = ROOT / '.claude/templates/community-sources/tools/fetch-reddit.py'
spec = importlib.util.spec_from_file_location('community_reader', template)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
reader.ROOT = str(ROOT)
original_folder = reader.cartella_di

def organized_folder(root, record, identifier):
    legacy = original_folder(root, record, identifier)
    return os.path.join(root, '_notes', '20-ricerca', 'acquisizioni-community', os.path.basename(legacy))

reader.cartella_di = organized_folder
if __name__ == '__main__':
    try:
        sys.exit(reader.principale())
    except reader.Errore as error:
        sys.stderr.write('Errore: ' + str(error) + '\n')
        sys.exit(1)
