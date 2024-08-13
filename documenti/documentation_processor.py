import os
import re
import json
from gemini_client import request_documentation
from documentation_snapshot import create_doc_snapshot

# Define the file where the documentation snapshot will be stored
DOCUMENTATION_SNAPSHOT_DIR = './snapshots/documentation-snapshot/'

def handler(project_name: str, language="", update=False):
    # Read the documentation sections and structure that we want from the following folder
    # IMPORTANT: Modify this folder (documentation_sections.json) in order to create your own structure and section name/description
    with open('documentation_sections.json', 'r') as f:
        input_dict = json.load(f)

    # Define the output directory
    dir = f"../{project_name}-doc/src/content/docs/"

    if language=="":
        # Creating project directory within the UI repo
        new_dir = os.path.join(dir)
        os.makedirs(new_dir, exist_ok=True)
        output_dir = f"../{project_name}-doc/src/content/docs/"
    else:
        # Creating project directory within the UI repo
        language_labels = {
            "English": "en",
            "Deutsch": "de",
            "Español": "es",
            "日本語": "ja",
            "Français": "fr",
            "Italiano": "it",
            "Bahasa Indonesia": "id",
            "简体中文": "zh-cn",
            "Português do Brasil": "pt-br",
            "Português": "pt",
            "한국어": "ko",
            "Türkçe": "tr",
            'Русский': 'ru',
            'हिंदी': 'hi',
            'Dansk': 'da',
            'Українська': 'uk'
        }
        language=language_labels.get(language)
        new_dir = os.path.join(dir, language, project_name)
        os.makedirs(new_dir, exist_ok=True)
        output_dir = f"../{project_name}-doc/src/content/docs/{language}/{project_name}"

    # snapshot_dir = os.path.join(DOCUMENTATION_SNAPSHOT_DIR, project_name)
    # Process the documentation structure and generate the documentation files
    if update == True:
        process_dict(input_dict, process_item, output_dir, language, update=True)
    else:
        process_dict(input_dict, process_item, output_dir, language)

    # Create a snapshot of the generated documentation
    create_doc_snapshot(output_dir, project_name)

def process_item(key, value, language, update):
    # This is where you can add your own logic to process each key-value pair
    print(f"Processing {key}")
    section_topic = f"{key}: {value}"
    return request_documentation(section_topic, language, update)

def sanitize_filename(s):
    # Remove characters that are generally not allowed in filenames
    s = re.sub(r'[<>:"/\\|?*]', '', s)
    
    # Replace multiple consecutive spaces with a single space
    s = re.sub(r'\s{2,}', ' ', s)
    
    # Strip leading and trailing spaces
    s = s.strip()
    
    return s

def process_dict(input_dict, process_func, output_dir, language, update=False, prefix=1):
    for key, value in input_dict.items():
        if isinstance(value, dict):
            # Sanitize the value for use in the filename
            sanitized_value = sanitize_filename(str(key))

            # If the value is a nested dictionary, create a new directory and process the nested dictionary
            new_dir = os.path.join(output_dir, f"{prefix}- {sanitized_value}")
            os.makedirs(new_dir, exist_ok=True)
            
            # Process the nested dictionary and pass the updated directories
            process_dict(value, process_func, new_dir, language, update, prefix=1)  # Reset prefix for new directory
        else:
            # Sanitize the value for use in the filename
            sanitized_value = sanitize_filename(str(key))
            # Process the key-value pair and write the result into a .md file
            result = process_func(key, value, language, update)
            filename = os.path.join(output_dir, f"{prefix}- {sanitized_value}.md")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result)

        prefix += 1

