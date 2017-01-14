from pathlib import Path

import base

import jinja2
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class SectionNode(base.Node):
    def __init__(self, data, pages):
        self.data = data

        self.pages = [page for page in pages
                 if page.section and page.section.startswith(self.name)]

        sort = self.config.data['sections'][0]['sort'] # FIXME select correct section
        reverse = False

        if sort[0] == '+':
            sort = sort[1:]
        elif sort[0] == '-':
            sort = sort[1:]
            reverse = True

        self.pages.sort(key=lambda x: getattr(x, sort))

        if reverse:
            self.pages.reverse()

    @property
    def name(self):
        return self.data['path'] # FIXME bad name

    def targets(self):
        template = None

        candidates = [Path('templates') / self.name / 'section.html']
        candidates += [Path('templates') / parent / 'section.html'
                      for parent in Path(self.name).parents]

        for candidate in candidates:
            if candidate.exists():
                template = candidate

        if not template:
            raise Exception("no template for section %r; one of the following must exist: %s" % (self.name, [str(c) for c in candidates]))

        # TODO paginate instead of just giving one target all the pages
        return [SectionTarget(self, self.pages, template)]

    @property
    def template(self):
        path = Path('sections') / (self.name + '.jinja')

        try:
            return jinja_env.get_template(str(path))
        except jinja2.exceptions.TemplateNotFound:
            for parent in path.parents:
                try:
                    return jinja_env.get_template(str(parent) + '.jinja')
                except jinja2.exceptions.TemplateNotFound:
                    continue
        #raise Exception("no section template for {}".format(self.name))
        return None

class SectionTarget(base.Target):
    def __init__(self, section, pages, template):
        self.section = section
        self.pages = pages
        self.template = jinja_env.get_template(str(template.relative_to('templates')))

    @property
    def path(self):
        page_number = self.paginator['current_page']

        if page_number == 1:
            return Path('output') / self.section.name / 'index.html'
        else:
            return Path('output') / self.section.name / 'page' / '{}.html'.format(page_number)

    @property
    def data(self):
        return {
            'type': 'section',
            'url': str(self.url),
        }

    @property
    def paginator(self):
        return {
            'pages': [page.data for page in self.pages],
            'current_page': 1,
            'total_pages': 1,
        }

    @property
    def env(self):
        return {
            'site': self.section.config.data,
            'page': self.data,
            'paginator': self.paginator,
        }
