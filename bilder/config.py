from pathlib import Path
import yaml

class Config(object):
    def __init__(self, path):
        self.data = yaml.load(path.open())

    @property
    def baseurl(self):
        try:
            return Path(self.data['baseurl'])
        except KeyError:
            return Path('/')

    @property
    def author(self):
        return self.data['author']

    @property
    def sections(self):
        if 'sections' in self.data:
            return self.data['sections']
        else:
            return []

config = Config(Path('config.yaml'))
