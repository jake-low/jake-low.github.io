from config import config

"""
Let's talk architecture.

Bilder is basically a big pure function that takes a collection of inputs and produces another collection of outputs. It does this to assist you in building a static website: the inputs can be "content" of any kind (text, images, videos, structured data, etc.), as well as templates that dictate how to present that content as HTML. Bilder glues all of this together to produce a directory tree that you can serve with any webserver.

There are other projects that do this. Jekyll and Hugo are promiment ones. So why make another?

In short, flexibility. I started out with Jekyll. I became frustrated that I couldn't easily have several "blog-like" sections on my site. Jekyll has one first-class `_posts` folder that all posts must go in. In order to make a site with several categories of blog-like content, you either had to put all the content in the `_posts` folder and tag each one with a category, then build special category pages that paginate all content, filtered by this tag, OR you could put each category of content in its own "collection". However, collections aren't quite first-class, and don't have all the features of `_posts`.

So then I tried Hugo. Hugo has a `content` folder where you can put all your content, divided into subfolders as you please. The subfolders get mapped to a heirarchy of templates, allowing you to have several different blog-like sections of your site (for different categories or types of content, for example) but still get all the features of Hugo for each section (per-section taxonomies and metadata, different templates for each kind of content, etc.).

So what's wrong? Well, Hugo still can't do one thing: turn non-text content into HTML pages. The use case for me was photographs: I want to have a directory full of JPEGs get converted into a photo gallery page and individual photo pages, and I want to use the metadata in the JPEG itself (EXIF data) in the HTML page (so I could display the title and date of the photo, or details about how it was taken).

Similar arguments can be applied to other file types: If I was a musician, I'd want to put my tracks as MP3s or lossless FLACs in a directory (or a tree of directories, maybe one per album), and I'd want to generate an HTML page (or several) that let me listen to and download each track, but also view the track's title, length, collaborating artists, and so on, and I'd want that information to get pulled out of the audio file itself (the 'authoritative' source) rather than have to manually duplicate it in a sidecar file or similar.

That said, there are times when I'd want to use a sidecar file *in addition* to the metadata in the media file itself, because I might want to share information on my site about the media that doesn't quite fit in the media-specific metadata format. For example, if you want to make a site to distribute "Age of Empires II" custom scenario files, you'd likely want to display a description and authorship of each scenario on your site, even though that file format doesn't permit you to store either on the file itself. In this case, you'd have to use a sidecar file for that data.





"""

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
        Render the target and write its output file to the output directory
        """
        if not self.template:
            print("skipping {} (no template)".format(self.name))
            return

        if not self.is_stale():
            print("skipping {} (not stale)".format(self.path))
            return

        print(self.path)

        try:
            self.path.parent.mkdir(parents=True)
        except FileExistsError:
            pass

        self.path.touch()

        with self.path.open('wb') as f:
            output = self.template.render(**self.env)
            f.write(output.encode('utf8'))
