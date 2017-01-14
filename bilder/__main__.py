from pathlib import Path

import shutil
import subprocess

import os
import jinja2
import yaml
import json


from config import config

import content
import section

# compile SCSS

try:
    Path('static/css').mkdir(parents=True)
except FileExistsError:
    pass

os.system('sass -I sass/ sass/styles.scss static/css/styles.css')

# setup output directory

try:
    Path('output').mkdir()
except FileExistsError:
    pass

# copy static tree

for path in Path('static').glob('**/*'):
    target = Path('output') / path.relative_to('static')

    if not path.is_file():
        continue

    if target.exists() and path.stat().st_mtime <= target.stat().st_mtime:
        continue

    if target.exists():
        target.unlink()
    else:
        target.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(str(path), str(target))

# collect content

content_nodes = []

for path in Path('content').glob('**/*.md'):
    content_nodes.append(content.MarkdownContentNode(path))

# for path in Path('content').glob('**/*.html'):
#     content_nodes.append(content.HTMLContentNode(path))
#
# for path in Path('content').glob('**/*.jpg'):
#     content_nodes.append(content.JPEGContentNode(path))

# render content

for node in content_nodes:
    for target in node.targets():
        target.render()

# collect sections

for data in config.sections:
    for target in section.SectionNode(data, content_nodes).targets():
        target.render()
