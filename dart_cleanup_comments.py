# process_dart_files.py
import sys
import os
import subprocess

def process_dart_files(directory):
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".dart"):
                filename = os.path.join(root, file)
                # Call remove_comments.py script with the current Dart file
                try:
                    # Call remove_comments.py script with the current Dart file
                    subprocess.run([sys.executable,  os.path.join(script_dir, 'remove_comments.py'), filename], check=True)
                    print(f"Processed {filename}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {filename}: {e}")
                except Exception as e:
                    print(f"Unexpected error processing {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_dart_files.py <project_directory>")
        sys.exit(1)

    project_directory = sys.argv[1]

    # Check if project_directory is a relative path, convert it to absolute
    if not os.path.isabs(project_directory):
        project_directory = os.path.abspath(project_directory)

    # Validate project_directory
    if not os.path.exists(project_directory):
        print(f"Error: {project_directory} does not exist.")
        sys.exit(1)
    process_dart_files(project_directory)
