import os
import re

# Set the root directory (your 'test' folder)
root_directory = r'C:\Users\User\Desktop\test'
script_name = os.path.basename(__file__)  # Get the current script's filename

# Updated regex pattern to match sensitive information (like passwords, secret keys)
password_patterns = [
    re.compile(r'(?i)(secret_key\s*=\s*[\'"].+?[\'"])'),  # Matches 'SECRET_KEY = "..."'
    re.compile(r'(?i)(password\s*=\s*[\'"].+?[\'"])'),    # Matches 'PASSWORD = "..."'
    re.compile(r'(?i)(api_key\s*=\s*[\'"].+?[\'"])'),     # Matches 'API_KEY = "..."'
    re.compile(r'(?i)(token\s*=\s*[\'"].+?[\'"])'),       # Matches 'TOKEN = "..."'
    re.compile(r'(?i)(password\s*:\s*[\'"].+?[\'"])'),    # Matches 'password: "..."' (dictionary style)
    re.compile(r'(?i)(passwd\s*=\s*[\'"].+?[\'"])'),      # Matches 'PASSWD = "..."'
    re.compile(r'(?i)(password\s*=\s*Password\([\'"].+?[\'"]\))'),  # Matches 'Password = Password("...")'
]

# Function to find all Python files in the directory recursively
def find_python_files(root_dir):
    python_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py') and filename != script_name:  # Only scan Python files and skip this script
                python_files.append(os.path.join(dirpath, filename))
    return python_files

# Function to scan for passwords and secret keys in a Python file
def scan_file_for_passwords(filepath):
    passwords = []
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            for pattern in password_patterns:
                match = pattern.search(line)
                if match:
                    passwords.append(match.group(0))  # Capture the full matched line
    return passwords

# Function to load existing .env values into a dictionary
def load_env_variables(env_filepath):
    env_vars = {}
    if os.path.exists(env_filepath):
        with open(env_filepath, 'r') as env_file:
            for line in env_file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    return env_vars

# Function to update or write new passwords to the .env file without deleting previous content
def write_passwords_to_env(passwords, env_filepath):
    env_vars = load_env_variables(env_filepath)
    
    for password in passwords:
        key_value = password.split('=', 1) if '=' in password else password.split(':', 1)
        if len(key_value) == 2:
            key = key_value[0].strip()
            value = key_value[1].strip().strip("'\"")  # Remove quotes around value
            env_vars[key] = value  # Update the dictionary with the new or updated password

    # Write all environment variables (including new ones) without duplicating entries
    with open(env_filepath, 'w') as env:
        for key, value in env_vars.items():
            env.write(f"{key}={value}\n")
        print(f"Updated .env file with {len(env_vars)} entries.")

# Function to replace passwords with environment variable references and mask the value
def hide_passwords_in_file(filepath, passwords):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    for password in passwords:
        key_value = password.split('=', 1) if '=' in password else password.split(':', 1)
        if len(key_value) == 2:
            key = key_value[0].strip()
            # Replace the original password with a reference to an environment variable
            content = content.replace(password, f'{key} = os.environ.get("{key}", "***")')

    # Write the updated content back to the original file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
        print(f"Replaced passwords in {filepath} with environment variable references.")

# Main function to scan all Python file, write passwords to .env, and hide them in the original files
def main():
    print(f"Scanning for passwords in Python files inside: {root_directory}")
    python_files = find_python_files(root_directory)
    
    all_passwords = []
    for file in python_files:
        print(f"Scanning {file}...")
        passwords = scan_file_for_passwords(file)
        if passwords:
            all_passwords.extend(passwords)
            hide_passwords_in_file(file, passwords)  # Hide the passwords in the original file

    if all_passwords:
        print(f"Found {len(all_passwords)} potential passwords or secret keys.")
        env_filepath = os.path.join(root_directory, '.env')
        write_passwords_to_env(all_passwords, env_filepath)
        print(f"Passwords and secret keys have been written/updated to: {env_filepath}")
    else:
        print("No passwords or secret keys found.")

if __name__ == '__main__':
    main()
