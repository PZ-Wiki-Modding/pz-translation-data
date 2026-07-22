import json, yaml
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent

LANGUAGE_CODES_DIR = SCRIPT_DIR / 'data' / 'language_codes'
OUTPUT_FILE = SCRIPT_DIR / 'out' / 'languageCodes.json'

language_codes = {}
for filename in LANGUAGE_CODES_DIR.iterdir():
    if filename.suffix == '.yaml':
        key = filename.stem
        with open(filename, 'r', encoding='utf-8') as f:
            language_codes[key] = yaml.safe_load(f)

for file_key, file_data in language_codes.items():
    # remove unnecessary fields
    file_data.pop('version', None)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(language_codes, f, indent=2, ensure_ascii=False)