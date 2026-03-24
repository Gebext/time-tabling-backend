import os
import re

def clean_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Remove # comments (but leave shebang)
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if line.strip().startswith('#!'):
            new_lines.append(line)
            continue
        # Remove # and everything after, then rstrip
        line = re.sub(r'#.*$', '', line).rstrip()
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    # Remove docstrings (triple quotes)
    content = re.sub(r'\"\"\"[\s\S]*?\"\"\"', '', content)
    content = re.sub(r'\'\'\'[\s\S]*?\'\'\'', '', content)
    
    # Finally, collapse extra newlines
    # 3 or more newlines -> 2 newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    with open(path, 'w') as f:
        f.write(content.strip() + '\n')

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        if 'venv' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                clean_file(os.path.join(root, file))

if __name__ == "__main__":
    process_directory('app')
