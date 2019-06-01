First Crack - A simple static blogging engine written in Python
===============================================================

Given a directory of plain text files formatted in Markdown, First Crack will generate a static website of over a thousand pages in less than two seconds.

## Dependencies

First Crack does not rely on any third-party tools, code, or frameworks. Because I started this project in 2011, though, with Python 2, you will need Python 2.\* to use my blogging engine. I plan to port it to Python 3 soon. Use with versions other than 2.\* at your own risk.

## Installation

Because First Crack has no dependencies, installation is a breeze: just clone the repository.

```
$ git clone https://github.com/zacjszewczyk/FirstCrack.git
$ cd FirstCrack
```

That's it.

## Setup

First Crack requires that you set up a configuration file before it will generate your site. This is a one-time thing and consists of filling out a few variables. First Crack will generate a skeleton config file when you run it for the first time. Do this with the following commands:

```
$ chmod 755 ./blog.py
$ ./blog.py
```

You have to fill in the config file before First Crack will build your site, so do this by opening ./EDITME in your editor of choice. You can do this in the terminal with vi, using the following command:

```
$ vi ./EDITME
```

The config file, EDITME, looks like this:

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

Assign a value to each variable, save the file, and then build your site.

## Usage

To build a website with FirstCrack, enter the following command:

```
$ ./blog.py
```

First Crack ships with two example content files, which it uses to build an example website. View that site by opening the index.html file in the local directory, or by entering the following command:

```
$ open local/index.html
```

## Advanced Usage

First Crack has a few advanced features that make managing a website easier, which are accessible in the "Authoring" mode. To enter "Authoring" mode, use the following command:

```
$ ./blog.py -a
```

First Crack will display a menu of available commands, along with an explanation of each. Enter "-h" at any time to view the help menu. You can also run any of these commands directly from your command line. For example, to clear all structure files, use the following command:

```
$ ./blog.py -R
```

## Background and Motivation

I started this project in 2011. After trying many content management systems, I decided to roll my own. After a few months of work, I began running my website on something I called First Crack. Over the years, that project morphed into the one you see before you today.

## License

This project, like [my website](https://zacs.site/) and [all my other projects](https://zacs.site/projects.html), is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). Read more about the license, and my other disclaimers, [at my website](https://zacs.site/disclaimers.html).