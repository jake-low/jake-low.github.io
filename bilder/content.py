from pathlib import Path

import datetime
import markdown
import json
import subprocess
import yaml

import base

import jinja2
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.smarty'
]

class ContentNode(base.Node):
    def targets(self):
        seen = []

        for section in self.path.relative_to('content').parents:
            template_directory = Path('templates') / section

            if template_directory.exists():
                for template in template_directory.glob('single.*'):
                    if template.name not in seen:
                        seen.append(template.name)
                        yield ContentTarget(self, template)


class ContentTarget(base.Target):
    def __init__(self, content, template):
        self.content = content
        self.suffix = template.suffix
        self.template = jinja_env.get_template(str(template.relative_to('templates')))

    def is_stale(self):
        return True

    @property
    def path(self):
        return Path('output') / self.content.path.relative_to('content').with_suffix(self.suffix)

    @property
    def env(self):
        return {
            'site': self.content.config.data,
            'page': self.content.data,
        }


class TextContentNode(ContentNode):
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
    def title(self):
        return self.frontmatter['title']

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
            # 'language': self.language,
            'section': self.section.split('/'),
            # 'url': str(self.url),
            # 'slug': self.slug,
            'excerpt': self.excerpt,
            'license': self.license,
        }

    @property
    def env(self):
        return {
            'site': self.config.data,
            'page': {**self.data, 'content': self.content}
        }


class MarkdownContentNode(TextContentNode):
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


class HTMLContentNode(TextContentNode):
    @property
    def excerpt(self):
        tree = lxml.html.fromstring(self.raw_content)
        sel = CSSSelector('p')
        return lxml.etree.tostring(sel(tree)[0]).decode('utf8')

    @property
    def content(self):
        return jinja_env.from_string(self.raw_content).render(site=self.config.data, page=self.data)


class JPEGContentNode(ContentNode):
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
