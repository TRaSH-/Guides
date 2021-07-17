import os
import jinja2
import json
import pathlib

# This script generates markdown files for Sonarr from the json files in this same folder.
# This is executed by `mkdocs` and the `mkdocs-simple-hooks` plugin (invoked from mkdocs.yml).

source_dir="docs/json/sonarr"
output_dir="docs/Sonarr/generated/"

def sonarr_markdown(*args, **kwargs):
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    for js in os.listdir(source_dir):
        if js.endswith(".json"):
            with open(os.path.join(source_dir, js)) as json_file:
                data = json.load(json_file)

                template = jinja2.Template("""<!-- markdownlint-disable-next-line MD041 -->
### {{ obj.name }}
{% if obj.note is defined %}
{{ obj.note }}
{% endif %}
{%- for i in obj.mustContain %}
Add this to your `Must contain (1)`
```bash
{{ i }}
```
{% endfor %}
{%- for i in obj.mustNotContain %}
Add this to your `Must not contain (2)`
```bash
{{ i }}
```
{% endfor %}
{%- for i in obj.preferred %}
{% if i.note is defined %}
{{ i.note | indent(4) }}
{% endif %}
Add this to your `Preferred (3)` with a score of [{{ i.score }}]
{%- for term in i.terms %}
<!-- markdownlint-disable-next-line MD046 -->
```bash
{{ term }}
```
{% endfor %}
{%- endfor %}
{%- if obj.optional is defined %}
#### Optional (this code was not well tested since the site does not use it)
* Must contain: `{{ (obj.optional.mustContain | default([])) | join(", ") }}`
* Must not contain: `{{ (obj.optional.mustNotContain | default([])) | join(", ") }}`
{%- for i in obj.optional.preferred %}
* Score: {{ i.score }}
{% if i.note is defined %}
{{ i.note | indent(4) }}
{% endif %}
{%- for term in i.terms %}
<!-- markdownlint-disable-next-line MD046 -->
```bash
{{ term }}
```
{% endfor %}
{%- endfor %}
{%- endif %}
""")
                template.stream(obj=data).dump(
                    f"{output_dir}{js.split('.')[0]}.mdt")
