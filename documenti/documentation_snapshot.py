import os
import json
import hashlib

DOCUMENTATION_SNAPSHOT_DIR = './snapshots/documentation-snapshot/'  # Ensure this matches change_tracker.py

# def hash_content(content):
#     """Generate a hash for a given content."""
#     return hashlib.md5(content.encode('utf-8')).hexdigest()

def create_doc_snapshot_directory(project_name):
    """Ensure the snapshot directory for a project exists under the given base directory."""
    project_doc_snapshot_dir = os.path.join(DOCUMENTATION_SNAPSHOT_DIR, project_name)
    os.makedirs(project_doc_snapshot_dir, exist_ok=True)
    return project_doc_snapshot_dir

def create_doc_snapshot(doc_directory, project_name):
    """Create a snapshot of the documentation with file paths and their contents."""
    snapshot_file_dir = create_doc_snapshot_directory(project_name)
    doc_snapshot = {}
    for root, _, files in os.walk(doc_directory):
        for file in files:
            if file.endswith(".md"):  # Assuming documentation files are in markdown format
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    relative_path = os.path.relpath(file_path, doc_directory)
                    doc_snapshot[relative_path] = content
    
    # Save the snapshot with the project name
    snapshot_file = os.path.join(snapshot_file_dir, f'{project_name}_doc_snapshot.json')
    os.makedirs(os.path.dirname(snapshot_file), exist_ok=True)
    with open(snapshot_file, 'w', encoding='utf-8') as f:
        json.dump(doc_snapshot, f, indent=4)
    return doc_snapshot

def save_doc_snapshot(doc_snapshot, project_name):
    """Save the current documentation snapshot to the JSON file."""
    snapshot_file = os.path.join(DOCUMENTATION_SNAPSHOT_DIR, project_name, f'{project_name}_doc_snapshot.json')
    with open(snapshot_file, 'w') as f:
        json.dump(doc_snapshot, f, indent=4)

