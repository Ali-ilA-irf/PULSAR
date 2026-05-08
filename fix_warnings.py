import os
import glob

files = glob.glob('*.py')

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'width="stretch"' in content:
        content = content.replace('width="stretch"', 'width="stretch"')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")

print("Done")
