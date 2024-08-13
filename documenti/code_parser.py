import os
import fnmatch

def generate_combined_file(codebase_directory):

    # Initialize an empty string to store the combined content
    combined_content = ""

    # List of directories and files to skip
    SKIP_DIRS = [
        '.git', '.svn', '.hg', 'node_modules', 'vendor', 'bin', 'obj', '__pycache__',
        'venv', 'env', '*.egg-info', 'dist', 'build', 'target', 'Debug', 'Release',
        '.idea', '.vscode', '.settings', 'out', 'coverage', 'tmp', 'log', 'vendor', '.astro',
        'cache', 'logs', 'tmp', '.mypy_cache', 'site', 'static', 'public', 'media'
    ]

    SKIP_FILES = [
        '*.log', '*.tmp', '*.bak', '*.swp', '*.swo', '*.pyc', '*.pyo', '*.class', '*.dll',
        '*.so', '*.a', '*.o', '*.exe', '*.bin', '*.out', '*.pid', '*.seed', '*.lock', '*.pdb',
        '*.iml', 'package-lock.json', 'yarn.lock', '*.map', '*.jar', '*.war', '*.ear', '*.lib',
        '*.ilk', '*.exp', '*.gem', '.bundle', 'composer.lock', '*.xcuserstate', '*.xcscheme',
        '*.app', '*.ipa', '*.dSYM', '*.apk', '*.aab', '*.jks', '*.csv', '*.json', '*.xml', '*.md',
        'Dockerfile', 'docker-compose.yml', '*.class', '*.pyc', '*.webp', '*.svg', '*.gif', '*.jpg', '*.jpeg',
        '*.png', '*.bmp', '*.ico', '*.tiff', '*.ai', '*.psd', '*.xcf', '*.mov', '*.mp4', '*.avi', '*.mkv',
        '*.mp3', '*.wav', '*.flac', '*.aac', '*.ogg', '*.m4a', '*.3gp', '*.wmv', '*.zip', '*.tar', '*.gz',
        '*.bz2', '*.7z', '*.rar', '*.iso', '*.dmg', '*.log', '*.swp', '*.swo', '*.bak', '*.tmp', '*.old', '*.orig',
        '*.htm', '*.html', '*.xhtml', '*.css', '*.scss', '*.sass', '*.less', '*.js.map', '*.d.ts', '*.min.js',
        '*.min.css', '*.lock', '*.pot', '*.po', '*.mo', '*.properties', '*.ini', '*.config', '*.prefs',
        '*.idx', '*.dat', '*.log.*', '*.backup', '*.old', '*.sql', '*.dump', '*.bak', '*.swp', '*.gpg', '*.pem',
        '*.crt', '*.key', '*.pub', '*.asc', '*.sig', '*.sf', '*.md5', '*.sha1', '*.sha256', '*.sha512', '*.asc',
        '*.gitignore'
    ]

    # Traverse the codebase directory
    for root, dirs, files in os.walk(codebase_directory):
        # Skip directories in skip_dirs
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:
            # Skip files in skip_files
            if any(fnmatch.fnmatch(file, pattern) for pattern in SKIP_FILES):
                continue

            file_path = os.path.join(root, file)
            # Open each file and append its contents to the combined content string
            try:
                with open(file_path, 'r', encoding='ISO-8859-1') as input_file:
                    combined_content += f"\n\n# File: {file_path}\n\n"
                    combined_content += input_file.read()
            except Exception as e:
                print(f"Could not read file {file_path}. Error: {e}")


    # Count the number of lines in the combined output
    num_lines = combined_content.count('\n')

    # Check if the number of lines exceeds the limit
    if num_lines >= 29000:
        raise ValueError(f"The combined output of the codebase has {num_lines} lines, which exceeds the limit of 29000 lines.")

    # Write the combined content into the output file
    output_file_path = "./codebase.txt"
    with open(output_file_path, 'w', encoding='ISO-8859-1') as output_file:
        output_file.write(combined_content)

    # print(f"All files in {codebase_directory} have been written to {output_file_path}.")
    
    # Return the combined content
    return combined_content