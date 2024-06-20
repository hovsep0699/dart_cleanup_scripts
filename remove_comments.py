import sys
import os
import re
import subprocess

def remove_comments(input_file, output_file=None):
    if not input_file.endswith('.dart'):
        print(f"Error: '{input_file}' is not a Dart file (.dart)")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    # Regular expression to match comments outside strings and interpolated strings
    pattern = r'//.*?$|/\*[\s\S]*?\*/|("(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\'|\$\{[^}]*\})'

    def replacer(match):
        # If the match is a comment, replace with an empty string
        if match.group(0)[:2] == '//':
            return ''
        elif match.group(0)[:2] == '/*':
            # If the match is a /* */ style comment, replace with spaces to keep line numbers intact
            return '' * (len(match.group(0)))
        else:
            # If the match is within a string or interpolated string, keep it unchanged
            return match.group(0)

    # Apply the regular expression to remove comments
    new_content = re.sub(pattern, replacer, content, flags=re.MULTILINE)
    # Remove extra spaces after removing comments
    new_content = re.sub(r'\n\s*\n', '\n', new_content)  # Remove empty lines
    new_content = re.sub(r'\n\s+', '\n', new_content)   # Remove leading spaces on lines
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Comments removed from '{input_file}'. Output written to '{output_file}'.")
    else:
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Comments removed from '{input_file}'. Original file overwritten.")
    try:
        subprocess.run(['dart',  "format", input_file if output_file is None else output_file], check=True)
        print(f"Autoformatted '{input_file}' using dartfmt.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Warning: Failed to autoformat using dartfmt. Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python remove_comments.py <input.dart> [output.dart]")
        return

    input_file = sys.argv[1]

    if not os.path.isabs(input_file):
        input_file = os.path.abspath(input_file)

    if len(sys.argv) == 2:
        remove_comments(input_file)
    elif len(sys.argv) == 3:
        output_file = sys.argv[2]
        if not os.path.isabs(output_file):
            output_file = os.path.abspath(output_file)
        remove_comments(input_file, output_file)
    else:
        print("Usage: python remove_comments.py <input.dart> [output.dart]")

if __name__ == "__main__":
    main()
