import shutil
import os
import subprocess
import re

def copy_directory(project_name):
    # Ensure the source directory exists
    src_path = os.getcwd() + "/front-end"
    
    if not os.path.exists(src_path):
        print(f"The source directory {src_path} does not exist.")
        return

    # Get the parent directory
    parent_dir = os.path.dirname(src_path)
    parent_dir = os.path.dirname(parent_dir)

    # Create the new directory name using the project name
    new_dir_name = f"{project_name}-doc"

    # Create the destination path with the new directory name
    dst_path = os.path.join(parent_dir, new_dir_name)
    
    # If the destination directory already exists, remove it
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)

    # Copy the directory
    shutil.copytree(src_path, dst_path)

    print(f"Copied directory {src_path} to {dst_path} as {new_dir_name}")

def run_npm_install(project_name):
    """Runs npm install in the specified repo."""
    repo_path = f"../{project_name}-doc/"
    print(f"running npm install in {repo_path}")
    try:
        subprocess.run(["npm", "install"], cwd=repo_path, check=True)
        print(f"npm install completed successfully in {repo_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running npm install in {repo_path}: {e}")
        print("The repo containing the documentation website was still created")
    except FileNotFoundError:
        print("npm is not installed or not found in the system PATH.")

import os

def update_github_link_in_files(github_link, project_name):
    directory_path = f"../{project_name}-doc/"
    
    # Update astro.config.mjs
    astro_config_file = os.path.join(directory_path, 'astro.config.mjs')
    try:
        with open(astro_config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {astro_config_file} not found.")
        return

    with open(astro_config_file, 'w', encoding='utf-8') as f:
        inside_social_block = False
        for line in lines:
            if "social:" in line:
                inside_social_block = True
                if github_link:
                    f.write("    social: {\n")
                    f.write(f"      github: '{github_link}'\n")
                    f.write("    },\n")
                # If no github_link is provided, skip writing the social block
            elif inside_social_block and "}," in line:
                inside_social_block = False
                continue  # Skip this line if we're inside the social block
            elif not inside_social_block:
                f.write(line)
    
    print(f"Updated {astro_config_file}")

    # Update index.mdx
    index_mdx_file = os.path.join(directory_path, 'src', 'content', 'docs', 'index.mdx')
    try:
        with open(index_mdx_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {index_mdx_file} not found.")
        return

    with open(index_mdx_file, 'w', encoding='utf-8') as f:
        github_section = False
        for line in lines:
            if "- text: check-out our github repo" in line:
                github_section = True
                if github_link:
                    f.write(f"- text: check-out our github repo\n")
                    f.write(f"  link: {github_link}\n")
                    f.write("  icon: github\n")
                # Skip the next two lines (link and icon) if no github_link is provided
            elif github_section and ("link:" in line or "icon:" in line):
                continue
            else:
                f.write(line)
            github_section = False
    
    print(f"Updated {index_mdx_file}")



import os

def update_github_link_in_files(github_link, project_name):
    directory_path = f"../{project_name}-doc/"
    
    # Update astro.config.mjs
    astro_config_file = os.path.join(directory_path, 'astro.config.mjs')
    try:
        with open(astro_config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {astro_config_file} not found.")
        return

    with open(astro_config_file, 'w', encoding='utf-8') as f:
        inside_social_block = False
        for line in lines:
            if "social:" in line:
                inside_social_block = True
                if github_link:
                    f.write("    social: {\n")
                    f.write(f"      github: '{github_link}'\n")
                    f.write("    },\n")
            elif inside_social_block and "}," in line:
                inside_social_block = False
                continue  # Skip this line if we're inside the social block
            elif not inside_social_block:
                f.write(line)
        if not github_link:
            f.write("\n")

    print(f"Updated {astro_config_file}")

    # Update index.mdx
    index_mdx_file = os.path.join(directory_path, 'src', 'content', 'docs', 'index.mdx')
    try:
        with open(index_mdx_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {index_mdx_file} not found.")
        return

    with open(index_mdx_file, 'w', encoding='utf-8') as f:
        skip_lines = False
        for line in lines:
            if "- text: check-out our github repo" in line:
                if github_link:
                    f.write(f"- text: check-out our github repo\n")
                    f.write(f"  link: {github_link}\n")
                    f.write("  icon: github\n")
                skip_lines = True  # Skip the following lines related to this block
            elif skip_lines:
                if not line.strip():  # Stop skipping after an empty line
                    skip_lines = False
            else:
                f.write(line)
    
    print(f"Updated {index_mdx_file}")




def update_project_title_in_config(project_name):
    """
    Update the title in the astro.config.mjs file to match the project name.
    
    Parameters:
    - project_name (str): The name of the project to set as the title.
    """
    config_file_path = f"../{project_name}-doc/astro.config.mjs"
    
    # Read the original file content
    with open(config_file_path, 'r', encoding='utf-8') as f:
        original_code = f.read()
    
    # Replace the title with the project name
    modified_code = re.sub(
        r"title: 'My Gemini Documentation',",
        f"title: '{project_name}',",
        original_code
    )
    
    # Write the modified content back to the file
    with open(config_file_path, 'w', encoding='utf-8') as f:
        f.write(modified_code)

