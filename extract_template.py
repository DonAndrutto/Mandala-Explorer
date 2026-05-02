import json

with open("index.html", "r") as f:
    content = f.read()

t_start = content.find('<script type="__bundler/template">')
t_start = content.find('>', t_start) + 1
t_end = content.find('</script>', t_start)

template_str = content[t_start:t_end].strip()
template_html = json.loads(template_str)

with open("template.html", "w") as f:
    f.write(template_html)
