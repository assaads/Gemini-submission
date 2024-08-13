import os
import json
import difflib
from documentation_snapshot import create_doc_snapshot, save_doc_snapshot
from gemini_client import define_format, send_existing_documentation, send_updated_code
from documentation_processor import handler

# Directories for storing snapshots
BASE_SNAPSHOT_DIR = './snapshots/'
CODEBASE_SNAPSHOT_DIR = os.path.join(BASE_SNAPSHOT_DIR, 'codebase-snapshot/')
DOCUMENTATION_SNAPSHOT_DIR = os.path.join(BASE_SNAPSHOT_DIR, 'documentation-snapshot/')

def detect_changes(current_snapshot, previous_snapshot):
    """Detect changes by comparing the current snapshot with the previous one and return the actual content of the modified and new files."""
    modified_files = {}
    new_files = {}

    for file, current_data in current_snapshot.items():
        if file == 'selected_languages':
            continue  # Skip checking the 'selected_languages' entry
        
        current_hash = current_data['hash']
        previous_data = previous_snapshot.get(file)

        if previous_data is None:
            # File is new
            new_files[file] = current_data['content']
        elif current_hash != previous_data['hash']:
            # File has been modified
            modified_files[file] = current_data['content']
    
    return modified_files, new_files

def get_file_content(file_path):
    """Retrieve the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def generate_change_description(old_content, new_content):
    """Generate a description of the changes between two versions of a file, formatted for AI understanding."""
    diff = difflib.unified_diff(old_content, new_content, lineterm='', n=0)
    changes = []
    
    old_line_num = 0
    new_line_num = 0
    
    for line in diff:
        if line.startswith('@@'):
            # Extract the line numbers from the diff header
            parts = line.split()
            old_line_num = int(parts[1].split(',')[0].replace('-', ''))
            new_line_num = int(parts[2].split(',')[0].replace('+', ''))
            changes.append(f"Change Context: {line}")
        elif line.startswith('-'):
            changes.append(f"Modified - Old Line {old_line_num}: {line[1:].strip()}")
            old_line_num += 1
        elif line.startswith('+'):
            if old_line_num is not None:
                changes.append(f"Modified - New Line {new_line_num}: {line[1:].strip()}")
                old_line_num = None  # Reset to None after a modification to correctly identify new additions
            else:
                changes.append(f"Added - New Line {new_line_num}: {line[1:].strip()}")
            new_line_num += 1
        else:
            old_line_num += 1
            new_line_num += 1

    return "\n".join(changes)


def update_documentation_for_changes(modified_files, new_files, codebase_directory, project_name, selected_languages):
    """
    Regenerate documentation for the files that have changed or are new.
    
    This function aggregates the changes, requests updated documentation sections from the AI,
    and updates the corresponding `.md` files based on the AI's response.
    
    Returns:
    - bool: False if combined_changes exceeds 29,000 lines, True otherwise.
    """
    if not modified_files and not new_files:
        print("No changes detected. Documentation is up to date.")
        return True
    
    if modified_files:
        print("Changes detected in the following files:")
        for file in modified_files:
            print(f"- {file}")
    
    if new_files:
        print("New files detected:")
        for file in new_files:
            print(f"- {file}")
    
    # Ensure AI knows the format by defining it before generating updates
    define_format()

    send_partial_codebase=True

    found_documentation = send_existing_documentation(project_name)

    if found_documentation == "":
        send_partial_codebase = False
    
    # Explanation for the AI at the top
    explanation = (
        "Please review the following changes between the old and new versions of the files in the codebase. "
        "Each change is shown with the original line number and content, followed by the new line number and content.\n\n"
        "Format:\n"
        "Old Line <line_number>: <original content>\n"
        "New Line <line_number>: <new content>\n\n"
        "Types of Changes:\n"
        "- 'Modified': A line that existed in the old version but has been changed.\n"
        "- 'Added': A completely new line that did not exist in the old version.\n\n"
        "Changes:\n"
    )

    # Prepare a combined description of all changes
    combined_changes = explanation

    # Combine the keys of modified_files and new_files
    combined_files = list(modified_files.keys()) + list(new_files.keys())

    if send_partial_codebase == True:
        for file in combined_files:
            file_path = os.path.join(codebase_directory, file)
            new_content = get_file_content(file_path)
            
            # For modified files, get old content; for new files, old content is empty
            if file in modified_files:
                old_content = load_previous_file_content(file, project_name)
            else:
                old_content = []
            
            # Generate change description
            change_description = generate_change_description(old_content, new_content)
            
            # Append to combined changes
            combined_changes += f"File: {file}\n"
            combined_changes += f"New Content:\n{''.join(new_content)}\n"
            combined_changes += f"Changes:\n{change_description}\n\n"

            # Check if combined_changes exceeds 29,000 lines
            if combined_changes.count('\n') > 29000:
                send_partial_codebase=False
                break

    if send_partial_codebase:
        send_updated_code(combined_changes)
    
    if len(selected_languages) == 1:
        selected_languages = ""
    handler(project_name, selected_languages, update=True)
    
    print("Updated documentation for the modified and new files.")
    
    return True



def load_previous_file_content(file_path, project_name):
    """
    Load the previous content of a file from the last codebase snapshot.

    Parameters:
    - file_path (str): The path to the file whose content needs to be retrieved.
    - project_name (str): The name of the project to locate the snapshot directory.

    Returns:
    - list: A list of strings representing the lines of the file content from the snapshot.
    """
    # Define the path to the snapshot file
    snapshot_file = os.path.join(CODEBASE_SNAPSHOT_DIR, project_name, f'{project_name}_codebase_snapshot.json')
    
    # Check if the snapshot file exists
    if os.path.exists(snapshot_file):
        # Load the snapshot
        with open(snapshot_file, 'r', encoding='utf-8') as f:
            snapshot = json.load(f)
        
        # Get the content for the given file path
        file_data = snapshot.get(file_path)
        
        if file_data:
            # Return the content as a list of lines
            return file_data['content'].splitlines(keepends=True)
        else:
            print(f"File {file_path} not found in snapshot.")
            return []
    else:
        print(f"Snapshot file {snapshot_file} not found for project: {project_name}")
        return []






