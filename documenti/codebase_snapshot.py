import os
import json
import fnmatch
import hashlib

BASE_SNAPSHOT_DIR = './snapshots/'
CODEBASE_SNAPSHOT_DIR = os.path.join(BASE_SNAPSHOT_DIR, 'codebase-snapshot/')

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

def hash_file(file_path):
    """Generate a hash for a given file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def create_snapshot_directory(project_name):
    """Ensure the snapshot directory for a project exists under the given base directory."""
    project_snapshot_dir = os.path.join(CODEBASE_SNAPSHOT_DIR, project_name)
    os.makedirs(project_snapshot_dir, exist_ok=True)
    return project_snapshot_dir

def create_snapshot(codebase_directory, project_name, selected_languages, temporary=False):
    """Create a snapshot of the codebase with file paths, their hashes, and actual content, and save selected languages."""
    project_snapshot_dir = CODEBASE_SNAPSHOT_DIR
    snapshot = {}
    
    for root, dirs, files in os.walk(codebase_directory):
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in SKIP_DIRS)]
        for file in files:
            if any(fnmatch.fnmatch(file, pattern) for pattern in SKIP_FILES):
                continue
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_hash = hash_file(file_path)
            relative_path = os.path.relpath(file_path, codebase_directory)
            
            # Store both the hashed content and actual content in the snapshot
            snapshot[relative_path] = {
                "hash": file_hash,
                "content": content
            }
    
    # Add the selected languages to the snapshot
    snapshot['selected_languages'] = selected_languages
    
    if temporary:
        return snapshot
    
    snapshot_file = os.path.join(project_snapshot_dir, project_name ,  f'{project_name}_codebase_snapshot.json')
    os.makedirs(os.path.dirname(snapshot_file), exist_ok=True)
    with open(snapshot_file, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=4)
    
    return snapshot_file



def load_snapshot(project_name):
    """Load the previous snapshot from a specific file."""
    project_snapshot_dir = CODEBASE_SNAPSHOT_DIR
    snapshot_file = os.path.join(project_snapshot_dir, project_name , f'{project_name}_codebase_snapshot.json')
    if os.path.exists(snapshot_file):
        with open(snapshot_file, 'r') as f:
            return json.load(f)
    return {}


def save_snapshot(snapshot, project_name):
    """Save the current documentation snapshot to the JSON file."""
    snapshot_file = os.path.join(CODEBASE_SNAPSHOT_DIR, project_name, f'{project_name}_codebase_snapshot.json')
    with open(snapshot_file, 'w') as f:
        json.dump(snapshot, f, indent=4)
