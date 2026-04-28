import os, json, yaml

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))

TRANSLATION_FILES_DIR = os.path.join(SCRIPT_DIR, 'data', 'translation_files')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'data', 'translationFiles.json')
SCHEMAS_DIR = os.path.join(SCRIPT_DIR, 'PZ_Translation_Schemas', r"{key}.schema.json")
DEFAULT_SETTINGS_FILE = os.path.join(SCRIPT_DIR, 'settings.json')

translation_files = {}
for filename in os.listdir(TRANSLATION_FILES_DIR):
    if filename.endswith('.yaml'):
        key = os.path.splitext(filename)[0]
        file_path = os.path.join(TRANSLATION_FILES_DIR, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
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

            with open(SCHEMAS_DIR.format(key=key), 'w', encoding='utf-8') as schema_file:
                json.dump(schema, schema_file, indent=2, ensure_ascii=False)


for file_key, file_data in translation_files.items():
    # remove unnecessary fields
    file_data.pop('version', None)

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
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
    "url": r"https://raw.githubusercontent.com/pz-wiki-modding/pz-translation-data/refs/heads/main/PZ_Translation_Schemas/{fileName}.schema.json",
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