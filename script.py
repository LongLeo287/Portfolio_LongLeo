
import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.findall(r'<div class="portfolio-body"><p class="client">(.*?)</p><h3>(.*?)</h3></div>', text)
with open('output.txt', 'w', encoding='utf-8') as f:
    for i, m in enumerate(matches):
        f.write(f'{i+1}. [{m[0]}] {m[1]}\n')

