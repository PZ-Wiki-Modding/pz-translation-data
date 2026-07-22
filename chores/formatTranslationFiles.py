import json, yaml
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent

TRANSLATION_FILES_DIR = SCRIPT_DIR / 'data' / 'translation_files'
OUTPUT_FILE = SCRIPT_DIR / 'out' / 'translationFiles.json'
DEPRECATED_SCHEMAS_DIR = SCRIPT_DIR / 'PZ_Translation_Schemas' / r"{key}.schema.json"
SCHEMAS_DIR = SCRIPT_DIR / 'out' / 'schemas' / r"{key}.schema.json"
DEFAULT_SETTINGS_FILE = SCRIPT_DIR / 'out' / 'settings.json'

translation_files = {}
for filename in TRANSLATION_FILES_DIR.iterdir():
    if filename.suffix == '.yaml':
        key = filename.stem
        with open(filename, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

            # add the data to the centralized json file
            translation_files[key] = data


            # generate the schema file

            # format the title based on the fileName field if it exists, otherwise use the key
            fileName = data.get('fileName', None)
            title = f"{fileName}.json Schema" if fileName else f"<{key}>.json Schema"

            # format patternProperties
            patternProperties = data.get('patternProperties', [])
            formattedPatternProperties = {}
            for pattern in patternProperties:
                formattedPatternProperties[pattern['pattern']] = {
                    "type": "string",
                    "description": pattern.get('description', '')
                }

            keys = data.get('keys', [])
            keys.append({
                "name": "$schema",
                "description": "A reference to the translation JSON schema file."
            })
            properties = {}
            for k in keys:
                properties[k['name']] = {
                    "type": "string",
                    "description": k.get('description', '')
                }

            schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": title,
                "description": data.get('description', ''),
                "type": "object",
                "patternProperties": formattedPatternProperties,
                "properties": properties,
                "additionalProperties": False,
            }

            def out(schema: dict, key: str, main: Path):
                # output schema file
                schema_file_path = main.with_name(main.name.format(key=key))
                schema_file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(schema_file_path, 'w', encoding='utf-8') as schema_file:
                    json.dump(schema, schema_file, indent=2, ensure_ascii=False)

            out(schema, key, SCHEMAS_DIR)
            out(schema, key, DEPRECATED_SCHEMAS_DIR)

for file_key, file_data in translation_files.items():
    # remove unnecessary fields
    file_data.pop('version', None)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(translation_files, f, indent=2, ensure_ascii=False)

DEFAULT_SETTINGS = {
    "json.schemas": [],
    "json.schemaDownload.trustedDomains": {
        "https://raw.githubusercontent.com/pz-wiki-modding/pz-translation-data": True
    }
}

TEMPLATE_FILE_SCHEMA_SETTING = {
    "fileMatch": [r"**/media/lua/shared/Translate/*/{fileName}.json"],
    "url": r"https://raw.githubusercontent.com/pz-wiki-modding/pz-translation-data/refs/heads/main/out/schemas/{fileName}.schema.json",
    "name": r"PZ {fileName} translation schema"
}

for file_key, file_data in translation_files.items():
    setting = TEMPLATE_FILE_SCHEMA_SETTING.copy()
    fileName = file_data.get('fileName', None)
    if not fileName:
        continue
    setting['fileMatch'] = [pattern.format(fileName=fileName) for pattern in setting['fileMatch']]
    setting['url'] = setting['url'].format(fileName=fileName)
    setting['name'] = setting['name'].format(fileName=fileName)
    DEFAULT_SETTINGS["json.schemas"].append(setting)

with open(DEFAULT_SETTINGS_FILE, 'w', encoding='utf-8') as settings_file:
    json.dump(DEFAULT_SETTINGS, settings_file, indent=2, ensure_ascii=False)