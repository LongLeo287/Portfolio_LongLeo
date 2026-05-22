import json

with open('assets/data/projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    'proj_036': 'CHILL SETUP: Segotep Slath Mini 🖥️',
    'proj_037': 'POPULAR CASE WITH 6 FANS: MSI MAG Forge 120A ❄️',
    'proj_038': 'BIZARRE 8-SIDED CASE: Thermaltake Tower 300 Gimmick or Class? 🤔',
    'proj_039': "WAIFU PC: A Weaboo's Dream Setup 😍",
    'proj_040': 'EURO SEASON PC BUILD: Ultra Clear VAR ⚽',
    'proj_041': '4K MONSTER: ASUS ROG Strix RTX 5080 🚀',
    'proj_042': 'TIDY SETUP: Cool ASUS ROG Pegboard 😎',
    'proj_043': '"BACK TO SCHOOL" PC: Study Hard - Play Harder 🎒',
    'proj_095': 'MSI 100Hz Best Seller Monitor Banner',
    'proj_098': 'Cyber Gaming PC Banner',
    'proj_128': 'Labubu Collection Poster',
    'proj_144': 'Happy Wednesday: For Pets & Owners',
    'proj_167': 'Artistic Photography (Set 1)',
    'proj_168': 'Artistic Photography (Set 2)',
    'proj_169': 'Artistic Photography (Set 3)',
    'proj_173': 'Artistic Photography (Set 7)'
}

for p in data:
    if p['id'] in translations:
        p['title']['en'] = translations[p['id']]
        
with open('assets/data/projects.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated featured items!")
