import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: var = paragraph.add_run(arg)
    # Replace with: var = paragraph.add_run()\nvar.text = arg
    def repl(match):
        indent = match.group(1)
        var = match.group(2)
        obj = match.group(3)
        arg = match.group(4)
        return f"{indent}{var} = {obj}.add_run()\n{indent}{var}.text = {arg}"

    new_content = re.sub(r'^(\s*)(\w+)\s*=\s*(\w+)\.add_run\((.+?)\)$', repl, content, flags=re.MULTILINE)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed {filepath}")

fix_file('create_presentation.py')
fix_file('update_presentation_script.py')
