from pathlib import Path
from jinja2 import Environment, FileSystemLoader

import datetime
import lxml.etree
import lxml.html
from lxml.cssselect import CSSSelector

import shutil
import subprocess

import os
import jinja2
import markdown
import yaml
import json


jinja_env = Environment(loader=FileSystemLoader('layouts'))

MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.smarty'
]

config = None
pages = []

class Target(object):
    def __init__(self, path):
        self.path = path

class HTMLTarget(Target):
    def __init__(self, source):
        self.source = source

    def render(self):
        if self.path.exists():
            self.path.unlink()
        else:
            self.path.parent.mkdir(parents=True, exist_ok=True)

        self.path.touch()

        output = self.template.render(**self.env)

        self.path.write_bytes(output.encode('utf8'))


class Page(object):
    @property
    def config(self):
        if self.language:
            return config[self.language]
        else:
            return config

    @property
    def template(self):
        raise NotImplementedError

    @property
    def url(self):
        url = self.config.baseurl / self.target.relative_to('output')

        if self.target.name == 'index.html':
            return url.parent
        else:
            return url

    @property
    def slug(self):
        return self.url.stem

    @property
    def title(self):
        return self.frontmatter['title']

    @property
    def language(self):
        return None
        #
        # if len(self.path.suffixes) > 1:
        #     return self.path.suffixes[0]
        # else:
        #     return None

    def is_stale(self):
        return True

    def render(self):
        """
        Render the page and write its output file(s) to the output directory
        """
        if not self.template:
            print("skipping {} (no template)".format(self.name))
            return

        # if not self.is_stale():
        #     print("skipping {} (not stale)".format(self.path))
        #     return

        print(self.target)

        try:
            self.target.parent.mkdir(parents=True)
        except FileExistsError:
            pass

        self.target.touch()

        with self.target.open('wb') as f:
            output = self.template.render(**self.env)
            f.write(output.encode('utf8'))

class ContentPage(Page):
    @property
    def target(self):
        try:
            return Path('output').joinpath(Path(self.frontmatter['url']))
        except KeyError:
            return Path('output') / self.path.relative_to('content').with_suffix('.html')

    @property
    def template(self):
        for parent in self.path.relative_to('content').parents:
            try:
                return jinja_env.get_template(str(parent / 'single.jinja'))
            except jinja2.exceptions.TemplateNotFound:
                continue
        raise Exception("no 'single' template for {}".format(self.path))

    @property
    def env(self):
        return {
            'site': self.config.data,
            'page': self.data,
        }


class TextContentPage(ContentPage):
    def __init__(self, path):
        with path.open() as f:
            line = f.readline()
            assert line == '---\n'

            frontmatter = []

            while True:
                line = f.readline()

                if line == '---\n':
                    break
                else:
                    frontmatter.append(line)

            frontmatter = ''.join(frontmatter)

            self.frontmatter = yaml.load(frontmatter)
            self.raw_content = f.read()

        self.path = path
        self.section = str(path.relative_to('content').parent)

    @property
    def author(self):
        try:
            return self.frontmatter['author']
        except:
            return self.config.author

    @property
    def date(self):
        date = self.frontmatter.get('date')

        if type(date) is datetime.datetime:
            return date
        elif type(date) is datetime.date:
            return datetime.datetime(date.year, date.month, date.day)

    @property
    def license(self):
        return self.frontmatter.get('license')

    @property
    def data(self):
        return {
            'type': 'content',
            'title': self.title,
            'author': self.author,
            'date': self.date,
            'language': self.language,
            'section': self.section.split('/'),
            'url': str(self.url),
            'slug': self.slug,
            'excerpt': self.excerpt,
            'license': self.license,
        }

    @property
    def env(self):
        page = self.data
        page['content'] = self.content
        return {
            'site': self.config.data,
            'page': page,
        }


class MarkdownContentPage(TextContentPage):
    @property
    def excerpt(self):
        return markdown.markdown(
            next(filter(lambda s: s, self.raw_content.split('\n'))),
            extensions=MARKDOWN_EXTENSIONS)

    @property
    def content(self):
        return markdown.markdown(
            jinja_env.from_string(self.raw_content).render(site=self.config.data, page=self.data),
            extensions=MARKDOWN_EXTENSIONS)


class HTMLContentPage(TextContentPage):
    @property
    def excerpt(self):
        tree = lxml.html.fromstring(self.raw_content)
        sel = CSSSelector('p')
        return lxml.etree.tostring(sel(tree)[0]).decode('utf8')

    @property
    def content(self):
        return jinja_env.from_string(self.raw_content).render(site=self.config.data, page=self.data)


class JPEGContent(ContentPage):
    sizes = {
        'small': '20%',
        'medium': '30%',
        'large': '50%',
    }

    def __init__(self, path):
        self.path = path
        self.section = str(path.relative_to('content').parent)

        cmd = 'exiftool -All -j {}'.format(self.path)
        output = subprocess.check_output(cmd.split(' '))
        self.frontmatter = json.loads(output.decode('utf8'))[0]

    @property
    def images(self):
        images = {size: self.target.with_suffix('.{}.jpg'.format(size))
            for size in self.sizes}

        images['fullsize'] = self.target.with_suffix('.jpg')

        return images

    @property
    def title(self):
        return self.frontmatter.get('Title')

    @property
    def author(self):
        return 'FIXME'

    @property
    def date(self):
        return datetime.datetime.strptime(self.frontmatter['CreateDate'], '%Y:%m:%d %H:%M:%S')

    @property
    def location(self):
        location = (
            self.frontmatter.get('Sub-location'),
            self.frontmatter.get('City'),
            self.frontmatter.get('Province-State'),
            self.frontmatter.get('Country'),
        )

        if self.title and location[0] and location[0] in self.title:
            location = location[1:]

        return ', '.join(filter(lambda x: x is not None, location))

    @property
    def exif(self):
        make = self.frontmatter.get('Make')
        model = self.frontmatter.get('Model')

        if model.startswith(make):
            camera = model
        else:
            camera = ' '.join((make, model))

        if self.frontmatter.get('LensSerialNumber'):
            lens = self.frontmatter.get('Lens')
        else:
            lens = None

        return {
            'camera': camera,
            'lens': lens,
            'focal_length': self.frontmatter['FocalLength'],
            'aperture': self.frontmatter['Aperture'],
            'shutter_speed': self.frontmatter['ExposureTime'],
            'iso': self.frontmatter['ISO'],
        }

    @property
    def data(self):
        return {
            'type': 'content',
            'title': self.title,
            'author': self.author,
            'date': self.date,
            'location': self.location,
            'url': str(self.url),
            'slug': self.slug,
            'image': {name: str(Path('/') / path.relative_to('output')) for name, path in self.images.items()},
            'exif': self.exif,
        }

    def is_stale(self):
        # FIXME oh shit, 'stale' should be on targets, not sources.
        if not self.target.exists():
            return True
        else:
            return self.path.stat().st_mtime > self.target.stat().st_mtime

    def render(self):
        was_stale = self.is_stale()

        super(JPEGContent, self).render()

        if was_stale:
            shutil.copy(str(self.path), str(self.images['fullsize']))

            for name, path in self.images.items():
                if name != 'fullsize':
                    os.system('convert {source} -resize {size} {target}'.format(
                        source=str(self.path), size=self.sizes[name], target=str(path)))
        else:
            print("skipping resize for {} (not stale)".format(self.path))


class Taxonomy(object):
    def __init__(self, path):
        super(SingleLayout, self).__init__(path)
        self.section = str(path.relative_to('layouts').parent)

# load config(s)

global config

configs = []

for path in Path('.').glob('config*.yaml'):
    configs.append(Config(path))

if len(configs) == 1:
    config = configs[0]
else:
    config = {c.language: c for c in configs}

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
        path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(str(path), str(target))

# collect pages

global pages

for path in Path('content').glob('**/*.md'):
    pages.append(MarkdownContentPage(path))

for path in Path('content').glob('**/*.html'):
    pages.append(HTMLContentPage(path))

for path in Path('content').glob('**/*.jpg'):
    pages.append(JPEGContent(path))

for path in Path('content').glob('**'):
    if path.is_dir() and path != Path('content'):
        pages.append(SectionPage(path))

# render pages

for page in pages:
    page.render()
