import json
import base64
import gzip
import os

with open("index.html", "r") as f:
    content = f.read()

# Replace template
with open("template.html", "r") as f:
    template_html = f.read()
template_json_str = json.dumps(template_html).replace("</script>", "<\\/script>")

t_start = content.find('<script type="__bundler/template">')
t_start = content.find('>', t_start) + 1
t_end = content.find('</script>', t_start)

content = content[:t_start] + "\n" + template_json_str + "\n  " + content[t_end:]

# Replace manifest
manifest_start = content.find('<script type="__bundler/manifest">')
if manifest_start != -1:
    m_start = content.find('{', manifest_start)
    m_end = content.find('</script>', manifest_start)
    manifest_json = content[m_start:m_end].strip()
    manifest = json.loads(manifest_json)
    
    for uuid, entry in manifest.items():
        ext = 'bin'
        if 'application/json' in entry['mime']: ext = 'json'
        elif 'text/javascript' in entry['mime']: ext = 'js'
        elif 'text/css' in entry['mime']: ext = 'css'
        elif 'image/png' in entry['mime']: ext = 'png'
        elif 'image/svg+xml' in entry['mime']: ext = 'svg'
        
        filepath = f"unpacked/{uuid}.{ext}"
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                data = f.read()
                
            if entry.get('compressed'):
                data = gzip.compress(data)
                
            entry['data'] = base64.b64encode(data).decode('utf-8')
            
    new_manifest_str = json.dumps(manifest)
    content = content[:m_start] + new_manifest_str + "\n  " + content[m_end:]

with open("index.html", "w") as f:
    f.write(content)
