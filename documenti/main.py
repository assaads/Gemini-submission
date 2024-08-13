import os
import json
from fe_builder import copy_directory, run_npm_install, update_github_link_in_files, update_project_title_in_config
from language_processor import choose_languages
from gemini_client import init
from code_parser import generate_combined_file
from documentation_processor import handler
from change_tracker import detect_changes, update_documentation_for_changes
from codebase_snapshot import create_snapshot_directory, create_snapshot, load_snapshot, save_snapshot

def main():
    # Get the codebase directory and project name from the user
    codebase_directory = input("Enter the path to the codebase directory (relative to the path of this program): ")
    project_name = input("Enter the name of the project: ")
    
    # Ask if the user wants to link the project to a GitHub repo
    # github_link = input("Do you want to link this project to a GitHub repository? If yes, enter the URL (leave blank for no): ").strip()
    
    # Update files with the GitHub link
    # update_github_link_in_files(github_link, project_name)

    # Update the project title in astro.config.mjs
    update_project_title_in_config(project_name)

    # Create or retrieve the snapshot directory for the project
    project_snapshot_dir = create_snapshot_directory(project_name)
    previous_snapshot_file_dir = os.path.join(project_snapshot_dir, f'{project_name}_codebase_snapshot.json')

    # Ask the user if they want to fully generate the documentation or update it
    mode_choice = input("Do you want to fully generate the documentation or update based on changes? (enter 'full' or 'update'): ").lower()

    if mode_choice == 'full' or mode_choice == 'f':
        selected_languages = None  # Trigger full generation
    elif (mode_choice == 'update' or mode_choice == 'u') and os.path.exists(previous_snapshot_file_dir):
        previous_snapshot = load_snapshot(project_name)
        selected_languages = previous_snapshot.get('selected_languages', ['English'])
    else:
        # If the user chose 'update' but no snapshot exists, treat it as a full generation
        print("No existing snapshot found. Proceeding with full documentation generation.")
        selected_languages = None

    if selected_languages is None:
        # Full documentation generation
        copy_directory(project_name)

        user_choice = input("Do you want to choose multiple languages (the default language is English)? (yes/no): ").lower()
        if user_choice == 'yes' or user_choice == 'y':
            selected_languages = choose_languages(project_name)

            # Create a snapshot of the codebase
            create_snapshot(codebase_directory, project_name, selected_languages)

            init(generate_combined_file(codebase_directory))
            # Process each selected language
            for lang in selected_languages:
                handler(project_name, lang)
            print(f"Full Documentation generation done")
        elif user_choice == 'no' or user_choice == 'n':
            selected_languages = ["English"]

            # Create a snapshot of the codebase
            create_snapshot(codebase_directory, project_name, selected_languages)

            init(generate_combined_file(codebase_directory))
            handler(project_name, "")
            print(f"Full Documentation generation done")
        else:
            raise ValueError("Invalid option. Please enter 'yes'/'y' or 'no'/'n'.")

    else:
        # Update documentation based on detected changes
        copy_directory(project_name)
        with open(previous_snapshot_file_dir, 'r') as file:
            previous_snapshot_file = json.load(file)
        current_snapshot = create_snapshot(codebase_directory, project_name, selected_languages, temporary=True)
        modified_files, new_files = detect_changes(current_snapshot, previous_snapshot_file)
        update_documentation_for_changes(modified_files, new_files, codebase_directory, project_name, selected_languages)
        save_snapshot(current_snapshot, project_name)
        print(f"Documentation updated based on code changes.")
    
    run_npm_install(project_name)

    print("Documentation generation done.")
    print("A folder with the website containing the documentation has been created")
    print("Go on that repo and type \"npm run dev\" to run it")
    print("Make sure to run \"npm run build\" to use the search function")
    print("This front-end is a static site build on Astro")
    print("go on https://docs.astro.build/en/guides/deploy/ to see how to deploy it on your favorite cloud provider")
    print("Thank you for using Documenti!")


if __name__ == "__main__":
    main()