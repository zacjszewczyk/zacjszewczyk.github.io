First Crack - A simple static blogging engine written in Python
===============================================================

Given a directory of a thousand [Markdown](http://daringfireball.net/projects/markdown/) files, First Crack will generate a full-featured, lightweight, static website in less than two seconds. For a live demo, check out [my website](https://zacs.site/). I have used First Crack as the back-end for my site since 2011.

## Table of Contents
* [Front-End Features](#front-end-features)
* [Back-End Features](#back-end-features)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Directory Structure](#directory-structure)
* [Setup](#setup)
* [Usage](#usage)
* [Advanced Usage](#advanced-usage)
* [Making a New Post](#making-a-new-post)
* [Background and Motivation](#background-and-motivation)
* [License](#license)

## Front-End Features

* **Lightweight** - First Crack builds a lightweight, minimalist website. A typical page loads less than 80KB of data--for comparison, a typical Medium post loads over 3000KB.
* Full-featured - Who says a static site generator can't have cool features? One of my favorites is the Post Archives. This page makes finding a certain article easy by displaying every post you have ever published. It also allows you to view a list of posts by year and month, too. Each post's byline also includes links to the year and month it was published, so you can easily narrow your search with just a few clicks.
* **Beautiful blog** - I built First Crack to be a blogging engine, and it remains true to that core today. The blog it builds presents clean articles in an aesthetically pleasing manner, whether viewed on a large desktop computer of a small mobile phone. I designed the default layout to remove the need for "Reader Views", by showing you exactly what you need and nothing you don't.
* **Custom landing page** - I like to think of personal websites as a public resume. As such, they ought to help you put your best foot forward--and First Crack allows you to do just that, with a custom landing page. Use this page to talk about yourself, your projects, and anything else--and let your viewers check out your blog later. Don't make your thoughts on Agile the first thing a new employer sees.

## Back-End Features

* **No dependencies** - I wrote First Crack in vanilla Python. First Crack has no dependencies. 
* **Fast** - I put a lot of work into optimizing every single operation First Crack executes, and it shows: given a thousand unique Markdown files, First Crack will generate individual pages for each article, and archive pages broken up by month and year published, in less than two seconds. As of the June 2019 release, First Crack does this in around 1.25 seconds, with a warm cache.
* **Easy to use** - To build a website with First Crack, drop a few Markdown files into the `Content` directory and run `blog.py`. That's it, First Crack takes care of the rest.
* **Platform-agnostic** - Don't worry about spinning up a special server if you use First Crack: even the most basic, bare-bones, underpowered web server can handle serving the static site this engine builds.

## Dependencies

First Crack does not rely on any third-party tools, code, or frameworks. It uses Python 3.7.3, although you may have to adjust the path to the Python binary. Thanks to a bug in my development environment, I have to point my Python 3 projects to `#!/usr/local/bin/python3` rather than the usual `#!/usr/bin/python3`. If you have Python 3 installed alongside Python 2 in the `/usr/bin/` directory, simply change the first line of the Python files in this project to `#!/usr/bin/python3`.

## Installation

Because First Crack has no dependencies, installation is a breeze: just clone the repository. Open a shell and type the following commands:

```
$ git clone https://zjszewczyk@bitbucket.org/zjszewczyk/firstcrack-public.git
$ cd FirstCrack
```

That's it.

## Directory Structure

On install, First Crack consists of this README, five Python scripts, a `system` directory that houses the content for four static pages, a `Content` directory with two example content files, and a `local` directory where First Crack will store all structure files. For now, `local` just has the main CSS file for the site. Check out the tree below for a more succinct explanation.

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

That's it. First Crack ships with two example content files, which it uses to build an example website. View that site by opening the `index.html` file in the `local` directory, or by entering the following command:

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