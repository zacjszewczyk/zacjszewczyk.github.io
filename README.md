First Crack - A simple static blogging engine written in Python
===============================================================

Given a directory of plain text files formatted in [Markdown](http://daringfireball.net/projects/markdown/), First Crack will generate a static website of over a thousand pages in less than two seconds. For a live demo, check out [my website](https://zacs.site/). I have used First Crack as the back-end for my site since 2011, and today I re-release the code base to the world.

## Dependencies

First Crack does not rely on any third-party tools, code, or frameworks. It uses Python 3.7.3, although you may have to adjust the path to the Python binary. Thanks to a bug in my development environment, I have to point my Python 3 projects to `#!/usr/local/Cellar/python/3.7.3/bin/python3`. If you have Python 3 installed alongside Python 2 in the `/usr/bin/` directory, simple change the first line of the Python files in this project to `/usr/bin/python3`.

## Installation

Because First Crack has no dependencies, installation is a breeze: just clone the repository. Open a shell and type the following commands:

```
$ git clone https://zjszewczyk@bitbucket.org/zjszewczyk/firstcrack-public.git
$ cd FirstCrack
```

That's it.

## Directory Structure

```
FirstCrack
|____README.md # This file.
|____blog.py # The blog engine.
|____Markdown.py # The Markdown parser.
|____colors.py # ASCII color code function.
|____ModTimes.py # Method to compare mod times of two input files.
|____Hash.py # Method to hash two input files and return equality.
|
|____system # Directory containing content used to populate select front-end files.
| |____index.html # Content for the home page.
| |____disclaimers.html # Content for the disclaimers page.
| |____projects.html # Content for the projects page.
| |____template.htm # Base HTML template file.
|
|____Content # Directory containing content files. All must end in .txt.
| |____Test Linkpost.txt # An example linkpost,
| |____Test Original Article.txt # An example article.
|
|____local # Directory for First Crack output. Structure files will go in here.
| |____blog # Directory containing all article HTML files.
| |____assets # Directory for images, CSS files, and documents.
| | |____main.css # The main CSS file for the site.
```

## Setup

First Crack requires that you set up a configuration file before it will generate your site. This is a one-time thing and consists of filling out a few variables. First Crack will generate a skeleton config file when you run it for the first time. Do this with the following commands:

```
$ chmod 755 ./blog.py
$ ./blog.py
```

You have to fill in the config file before First Crack will build your site, so do this by opening `EDITME` in your editor of choice. You can do this in the terminal with `vi`:

```
$ vi ./EDITME
```

The config file, `EDITME`, looks like this:

```
# FirstCrack configuration document
# The following variables are required:
## base_url - The base URL for your website, i.e. https://zacs.site
## byline - The name of the author, as it will display on all posts
## full_name - The full, legal name of the content owner
## meta_keywords - Any additional keywords you would like to include in the META keywords tag
## meta_appname - The desired app name, stored in a META tag
## twitter - URL to your Twtitter profile
## instagram - URL to your Instagram profile
base_url = 
byline = 
full_name = 
meta_keywords = 
meta_appname = 
twitter = 
instagram = 
```

Assign a value to each variable, save the file, and then build your site. My first two lines look like this:

```
base_url = https://zacs.site/
byline = Zac J. Szewczyk
```

## Usage

To build a website with First Crack, enter the following command:

```
$ ./blog.py
```

First Crack ships with two example content files, which it uses to build an example website. View that site by opening the `index.html` file in the `local` directory, or by entering the following command:

```
$ open local/index.html
```

## Advanced Usage

First Crack has a few advanced features that make managing a website easier, which are accessible in the "Authoring" mode. To enter "Authoring" mode, use the following command:

```
$ ./blog.py -a
```

First Crack will display a menu of available commands, along with an explanation of each. Enter `-h` at any time to view the help menu. First Crack will continue prompting you for input in this mode until you exit it with either `exit` or `!exit`. You can also run any of these commands directly from the command line. For example, to clear all structure files and rebuilt the entire site, use the following command:

```
$ ./blog.py -R
```

## Making a New Post

Like everything else, the process for making a new post is simple. See the files in the Content directory for examples of a linkpost and an original article. To make a new post, save a text file in the Content directory and build the site. First Crack will only build files that have changed since you last ran it, and then re-build the blog and archive pages as necessary. 

## Background and Motivation

I started this project in 2011. After trying many of the day's most popular content management systems, I decided to roll my own. I began running my website on something I called First Crack a few months later. Over the years, that project morphed into the one you see before you today.

I designed First Crack with ease of use, speed, and versatility in mind. I believe these goals are evident in the engine's dead-simple setup, its ability to build over one thousand pages in less than two seconds, and the lightweight website it produces.

After almost a decade, content management systems have gotten much better since I started this project. I have yet to find anything First Crack cannot do, though, or an engine that wins out in the design goals I mentioned above. I like working on First Crack, and I look forward to adding cool new features in the future.

## License

This project, like [my website](https://zacs.site/) and [all my other projects](https://zacs.site/projects.html), is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). Read more about the license, and my other disclaimers, [at my website](https://zacs.site/disclaimers.html).