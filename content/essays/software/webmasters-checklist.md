---
date: 2016-07-21T00:00:00Z
license: CC BY 4.0
title: Webmaster's Checklist
---

Not a webmaster at your day job? Got a cool idea for a site? This list is for you. It'll help you make sure you've covered all your bases before you deploy.

Go forth and make cool stuff!

## How to use this list

The checklist is broken down by theme, and the themes are in roughly chronological order of when I'd advise you to start thinking about them. Some tasks are easier to do before you start building content, and others after. For many, it doesn't really matter.

## Licensing

A license tells people what they can and cannot do with content on your site.

<input id='choose-a-license' type='checkbox'>
<label for='choose-a-license'>
**Choose a license (or licenses) for your content**
</label>

Since you're not a lawyer (right?) you should use a standard license rather than writing your own. A standard license is also easier for others to use, since many people will recognize a license by name and recall its terms.

You should choose a license based on the terms it offers users of your content. Think about whether you want people to be able to reprint your content, modify it, or sell it, and whether they should be required to attribute you.

For code, consider an open source license that will allow others to use your code in their projects. GitHub has a site called [choosealicense.com](https://choosealicense.com) that can help you choose a license for code.

For text, images, and media, consider a [Creative Commons](https://creativecommons.org/choose) license. CC licenses encourage sharing. There are several with different terms.

If you don't want to permit any sharing of the content, you can reserve all rights. This is the default in most jurisdictions, but you should still state it explicitly. Use a phrase like this:

> © 2016 &lt;your name&gt;. All rights reserved.

<input id='cite-your-license' type='checkbox'>
<label for='cite-your-license'>
**Correctly cite this license on each page of your site**
</label>

The footer is a good place to put license info. It should be visible on each page, so visitors arriving via links or search engines won't have to go digging on your site to find your content license.

## Usability

<input id='javascript-optional' type='checkbox'>
<label for='javascript-optional'>
**JavaScript should be optional**
</label>

Your site doesn't have to be as pretty when running in a browser that has JavaScript disabled, but it should still be functional. Test this by turning off JavaScript in your browser settings and then viewing your site.

<input id='user-friendly-urls' type='checkbox'>
<label for='user-friendly-urls'>
**Create user-friendly URLs**
</label>

Static URLs like `example.com/blog/2015/05/19/how-to-care-for-snails` are more user friendly than URLs which use the query parameters to generate their content, like `example.com/blog.php?post_id=71`.

<input id='permalinks' type='checkbox'>
<label for='permalinks'>
**URLs should be permanent**
</label>

If your URLs imply anything about the technology the site is built with, they're not permanent. This means file extensions like `.php` and `.html` should be hidden (use your web server configuration to do this).

Make sure that if you rebuild your site using different tools, you'll easily be able to preserve the old URLs.

When designing the layout of your site, think about what URLs make sense to end users, not what makes coding the site easier. Any URL scheme is easy to build with just a little research and ingenuity. Decide what the URL should look like first, then figure out how to build the site based on that.

<input id='dont-break-browser' type='checkbox'>
<label for='dont-break-browser'>
**Don't hijack fundamental browser behavior**
</label>

  Nothing is more annoying than a website that disables text selection, or right click, or changes the scroll behavior. Browsers provide basic functionality that is generally inherited from native behaviors of the user's operating system. Changing these to site-specific behaviors is jarring and will alienate visitors.

## Internationalization

- **Use UTF-8**

  No matter what language you're writing in, using UTF-8 means everyone will be able to view your content without getting a bunch of garbage characters.

  Use `<meta charset='UTF-8'>` at the very top of the `<head>` section of all pages, and make sure your web server is configured to set the  `Content-Type` header to `text/html; charset=utf-8` when serving files with a `.html` suffix (binary content like images should use the appropriate MIME-type for their encoding).

- **Set the document language**

  `<html lang='en'>` will tell browsers and search engines that your page is in English. See [this list](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for other two-letter language codes.

## Accessibility

- **Use semantic HTML**

  This means using HTML tags to indicate the role of different parts of the content in the site. HTML5 has many new tags, such as `<article>`, `<section>`, `<nav>`, `<header>`, `<footer>`, and `<aside>`. Use them to divide text into meaningful chunks. This helps those using a screen reader (a program that helps the blind and vision impaired interact with computers) understand what the different parts of your document are.

  Also be sure to use CSS for styling rather than semantic tags. For example, use heading tags hierarchically, like a table of contents. Don't use an `<h3>` for your page title and an `<h1>` for a subsection just because you want the subsection to appear bigger. Use CSS for that.

- **Use `aria-label`s**

  Adding an `aria-label` property to an HTML tag indicates to screen readers what the purpose of the tag is. It can help make "anonymous" tags meaningful to those who have vision disabilities.

  For example, a close button might be styled as an `X`. This is visually meaningful, but a screen reader might read the button aloud as "X", when really it would be clearer to have it say "close". An `aria-label='close'` could be used to provide a hint to the screen reader about the meaning of the button.

- **Use `alt` text on images**

  Using the `alt` property on images helps those who can't see an image understand its content. The description should be short, but clearly describe the content. Think of it like a human-readable file name, not an essay detailing the content.

  Don't put `alt` text on images that are purely part of the site's styling and not part of the content (e.g. backgrounds, banners, section separators, etc.) because a screen reader will pause on these to announce the alt text, hindering navigation. Ideally, these decorative images would be replaced by semantic HTML (`<header>`, `<hr>`, etc.) and styled with CSS.

- **Test for colorblindness**

  About 4.5% of the world population affected by colorblindness. Make sure your site is still navigable when simulating different types of colorblindness. [colorfilter.wickline.org](http://colorfilter.wickline.org/) has a tool to assist with this.

## Security

- **Use HTTPS**

  This is non-optional. With free SSL certificates from [Let's Encrypt](https://letsencrypt.org), there's no excuse for HTTP. Your content should be served over HTTPS and _only_ HTTPS.

  The performance impact of HTTPS is negligible. From [Imperial Violet](https://www.imperialviolet.org/2010/06/25/overclocking-ssl.html) (Adam Langley's blog):

  > In January this year (2010), Gmail switched to using HTTPS for everything by default. [...] In order to do this we had to deploy _no additional machines and no special hardware_. On our production frontend machines, SSL/TLS accounts for less than 1% of the CPU load, less than 10KB of memory per connection and less than 2% of network overhead.

## Mobile

- **Determine whether your site should be mobile-friendly**

  It's worth noting that with CSS3 it's really easy to make a site mobile-friendly. Complicated sites (e.g. Amazon.com) have thousands of lines of CSS3 to define their mobile layouts, but for a simple site (like yours) it should really only take a few lines. My blog is mobile-friendly and it only has about a dozen lines of CSS related to mobile.


## SEO

Search engine optimization (SEO) is the process of adding metadata to your content (usually in the form of invisible HTML tags) to tell search engines like Google what's on your page, and how it relates to other pages on the site.

SEO is a buzzword in the commercial website sector, and you'll often see it touted as a way to boost sales or advertising traffic. But even if your site is purely informational, with no commercial intent, it's still in your interests (and the interests of those who would want to see your content) to make sure search engines can understand your site.

- **Use `<meta name='description' content='...'>`**

  This tag lets you summarize the content of the page. Each page should have a unique description; don't use the same description across the whole site. Search engines often use the description as a preview when showing search results. Keep it short &ndash; less than 160 characters is ideal.

  It's okay to omit this tag, and it makes sense to do so on pages with lots of content (such as an index page with previews of many articles or products). If the tag isn't present, search engines will grab a preview automatically, and will favor parts of the page that match the terms a user searched for.

- **Make a `robots.txt` file**

  This file should live at `example.com/robots.txt`. It tells search engine crawlers (the programs that traverse the internet link-by-link, indexing web sites) what they should and shouldn't index. Well-behaved programs respect it, but it's _not a security measure_, just an advisory document. Here's a simple one that allows access to everything.

  ```
  User-agent: *
  Disallow:
  ```

- **Provide a `sitemap.xml`**

  This is usually generated by your site build system. It's an XML map that tells web crawlers what content exists on your site.

  It's not necessary, but it helps to ensure all your content is discovered by a search engine. It's especially valuable if your site is large or if its content isn't highly interlinked (blogs often fall into the latter category).

## Deployment

- **Make your deployment repeatable**

  Your site should live in a version-controlled repository. Wherever you're hosting your site, make sure that you can run a command from that repository to build whatever needs to be built, and deploy whatever needs to be deployed.

  This could be a Dockerfile, or just a tarball, but the goal is to eliminate the possibility of introducing bugs to the site when deploying by hand (bugs introduced this way are _really_ annoying to track down).

- **Set up a health monitor**

  You can write your own microservice and run it in the cloud somewhere, or use something cheap and prebuilt like [Updown.io](https://updown.io).

## Miscellaneous

- **Have a backup!**

  Putting your site on a repository hosting site ([GitLab](https://gitlab.com) has free private repositories if you don't want the world to see your source code) is good insurance, but you'll still want to have a backup on a physical hard drive, just like you (hopefully!) do for your other important data.
