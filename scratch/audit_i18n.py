import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Get keys from HTML
html_keys = set(re.findall(r'data-i18n="([^"]+)"', html))
print(f"HTML data-i18n keys ({len(html_keys)}):")
for k in sorted(html_keys):
    print(f"  {k}")

# Get vi keys from JS
start = js.find("vi: {")
end = js.find("  en: {")
vi_block = js[start:end]
vi_keys = set(re.findall(r"    (\w+):", vi_block))
vi_keys -= {"vi", "categories"}
print(f"\nJS vi translation keys ({len(vi_keys)}):")
for k in sorted(vi_keys):
    print(f"  {k}")

# Find HTML keys missing from JS
missing_in_js = html_keys - vi_keys
if missing_in_js:
    print(f"\n!!! HTML keys MISSING from JS translations ({len(missing_in_js)}):")
    for k in sorted(missing_in_js):
        print(f"  {k}")
else:
    print("\nAll HTML i18n keys found in JS translations.")

# Check filter keys
filter_keys = set(re.findall(r'data-i18n="(filter_[^"]+)"', html))
print(f"\nFilter keys in HTML: {filter_keys}")
filter_in_js = [k for k in filter_keys if k in vi_block]
print(f"Filter keys in JS vi: {filter_in_js}")
