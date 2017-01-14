from config import config

class Node(object):
    @property
    def config(self):
        return config

class Target(object):
    @property
    def url(self):
        url = config.baseurl / self.path.relative_to('output')

        if self.path.name == 'index.html':
            return url.parent
        else:
            return url

    @property
    def slug(self):
        return self.url.stem

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

        print(self.path)

        try:
            self.path.parent.mkdir(parents=True)
        except FileExistsError:
            pass

        self.path.touch()

        with self.path.open('wb') as f:
            output = self.template.render(**self.env)
            f.write(output.encode('utf8'))
