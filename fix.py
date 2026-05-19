import json

with open('replacements.json', 'r', encoding='utf-8-sig') as f:
    replacements = json.load(f)

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for k, v in replacements.items():
    text = text.replace(f'<h3>{k}</h3>', f'<h3>{v}</h3>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Done.')
