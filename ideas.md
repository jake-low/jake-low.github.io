
A piece of content has two inputs (the file and the template) and one or more outputs.

`content/foo.jpg`
-> `output/foo.small.jpg`
-> `output/foo.medium.jpg`
-> `output/foo.fullsize.jpg`
-> `output/foo.html`

`content/bar.md`
-> `output/bar.txt`
-> `output/bar.html`

---

Sections are generated one-to-one for _directories_ in the `content`. Sections can be nested inside other sections.

A section "contains" all of the content files found under it (recursively).

Sections are composed of pages. Each page is generated from:
- a template (e.g. `essays.jinja`)
- a list of ContentPage envs

Sections themselves have:
- pagination key, direction, count, etc.

they do _not_ have:
- a title (since any section template might be used to generate multiple section pages; e.g. `essays.jinja` generates `/essays/software` and `/essays/photography`)
- author, date, license, etc.

`content/lol/`
-> `output/lol/`
-> `output/lol/page/2`

A section has many inputs (one template and lots of content files) and many outputs (the various page files).

An individual section page (output) has many inputs also (one template file and a subset of the content files).

---

Taxonomies are like sections, but rather than being generated one-to-one for content directories, they're generated explicitly by creating a template in the `layouts/taxonomies` folder.

```
(contents of layouts/taxonomies/tag.jinja)
---
key: tags
sort: +date
paginate: 10
---
```

```
---
title: Some Post
date: 2006-04-01
tags:
  - april fool's
  - humor
---
...
```

A taxonomy has page groups for each value of the specified key found in content files. Each page group can contain one or more pages (assuming pagination of the taxonomy is enabled).

-> `output/tags` ("term list")
-> `output/tagged/april-fools/` ("term page")
-> `output/tagged/humor/`
-> `output/tagged/humor/page/2`

A taxonomy page depends on the taxonomy template and some subset (assuming pagination) of all content pages that are tagged with that page group's key.

TODO how to render a page which lists all the keys, and links to each key page?

What about this:

```
(layouts/taxonomies/tags/terms.jinja)
---
sort: +name
url: /tagged
# url defaults to /tags since that's the taxonomy name
# the terms page cannot be paginated (to avoid name collisions with terms)
---

{% for term in taxonomy.terms %}
  <li><a href='{{ term.url }}'>{{ term.name }}</a></li>
{% endfor %}
```

```
(layouts/taxonomies/tags/term.jinja)
---
sort: -date
paginate: 10
url: /tag/:term
# url defaults to /tags/:term
---

{% for page in term.pages %}
  <article>
    <h1><a href='{{ page.url }}'>{{ page.title }}</a></h1>
    <p>{{ page.excerpt }}</p>
  </article>
{% endfor %}
```

N.B. if you use the default values for `url` in both templates, then you can't have a term named `page`
