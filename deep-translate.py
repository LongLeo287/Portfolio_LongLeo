import json
import time
from deep_translator import GoogleTranslator

# Initialize translator
translator = GoogleTranslator(source='vi', target='en')

with open('assets/data/projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Hardcoded overrides to fix some bad translations
overrides = {
    'Ảnh Chân Dung / Sự Kiện': 'Portrait / Event Photography',
    'Bộ': 'Set',
    'Ảnh Nghệ Thuật': 'Artistic Photography',
    'Nhiếp ảnh': 'Photography',
    'GÓC MÁY GỌN GÀNG': 'TIDY SETUP',
    'Màn Hình': 'Monitor',
    'ĐÁNG NGHE KHÔNG': 'WORTH LISTENING TO'
}

def translate_text(text):
    if not text:
        return text
    
    # Check overrides first
    for k, v in overrides.items():
        if k in text:
            text = text.replace(k, v)
            
    # Try translating with API
    try:
        # Don't translate if it already looks completely English (simple heuristic)
        if all(ord(c) < 128 for c in text) and not any(w in text.lower() for w in ['màn hình', 'bộ', 'ảnh', 'góc', 'máy', 'nghe']):
            return text
            
        translated = translator.translate(text)
        time.sleep(0.5) # Avoid rate limits
        return translated
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text

count = 0
for p in data:
    if isinstance(p.get('title'), dict) and p['title']['vi'] == p['title']['en']:
        vi_text = p['title']['vi']
        print(f"Translating: {vi_text}")
        en_text = translate_text(vi_text)
        p['title']['en'] = en_text
        print(f"  -> {en_text}")
        count += 1
        
    if isinstance(p.get('client'), dict) and p['client']['vi'] == p['client']['en']:
        vi_client = p['client']['vi']
        if vi_client == 'Dự Án Cá Nhân':
            p['client']['en'] = 'Personal Project'
        elif vi_client == 'Nhiếp ảnh':
            p['client']['en'] = 'Photography'
        elif vi_client == 'Thiết kế':
            p['client']['en'] = 'Design'
        else:
            en_client = translate_text(vi_client)
            p['client']['en'] = en_client

with open('assets/data/projects.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Translated {count} titles!")
