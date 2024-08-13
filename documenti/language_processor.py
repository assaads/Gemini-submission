import re

def choose_languages(project_name):
    languages = [
        "Deutsch", "Español", "日本語", 
        "Français", "Italiano", "Bahasa Indonesia",
        "简体中文", "Português do Brasil",
        "Português",  "한국어","Türkçe",
        'Русский', 'हिंदी', 'Dansk', 'Українська'
    ]
    print("Choose from the following languages (English is always included by default):")
    
    for i, lang in enumerate(languages):
        print(f"{i+1}. {lang}")
        
    selected_indexes = input("Enter the numbers of your preferred languages, separated by commas: ").split(',')

    # Validate the selected languages
    for i in selected_indexes:
        if int(i) < 1 or int(i) > len(languages):
            raise ValueError(f"Invalid option: {i}. Please enter numbers between 1 and {len(languages)}.")
    
    # English is always included by default
    selected_languages = ["English"]
    selected_languages += [languages[int(i)-1] for i in selected_indexes]
    
    update_config(selected_languages, project_name)

    return selected_languages

def update_config(selected_languages, project_name):
    # Define the language labels and language codes
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

    # Initialize the locales string with English as the default language
    locales_string = """
        // English docs in `src/content/docs/en/`
        'en': {
          label: 'English',
        },"""

    # Add each selected language to the locales string
    for lang in selected_languages:
        if lang == "English":
            continue
        lang_code = language_labels[lang]
        locales_string += f"""
        // {lang} docs in `src/content/docs/{lang_code}/`
        '{lang_code}': {{
          label: '{lang}',
          lang: '{lang_code}',
        }},"""
    
    
    # Specify the directory path
    directory_path = f"../{project_name}-doc/"

    # Read the original code from the file
    with open(f'{directory_path}/astro.config.mjs', 'r') as f:
        original_code = f.read()

    # Insert the locales into the original code
    modified_code = re.sub(r"title: 'My Gemini Documentation',", "title: 'My Gemini Documentation',\n    defaultLocale: 'en',\n    locales: {" + locales_string + "\n    },", original_code)

    # Write the modified code back to the file
    with open(f'{directory_path}/astro.config.mjs', 'w') as f:
        f.write(modified_code)
