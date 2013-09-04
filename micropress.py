#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, math, sys, time
from os import path, listdir, makedirs, system, remove
from jinja2.loaders import FileSystemLoader
from jinja2 import Environment
from werkzeug import script
from markdown2 import markdown
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urllib import unquote
from datetime import datetime, tzinfo, timedelta
from shutil import copyfile

PATH = path.realpath(path.join(path.dirname(path.abspath(__file__)), ".."))
TEMPLATE_PATH = path.join(PATH, "templates/")
SOURCES_PATH = path.join(PATH, "sources/")
POSTS_PATH = path.join(SOURCES_PATH, "posts/")
PAGES_PATH = path.join(SOURCES_PATH, "pages")
PUBLIC_PATH = path.join(PATH, "public/")

BLOG_PATH = path.join(PUBLIC_PATH, "blog")
CATEGORIES = path.join(BLOG_PATH, "categories")
ARCHIVES = path.join(BLOG_PATH, "archives")

sys.path.append(PATH)
from config import *

class Entry:
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

class Category(Entry):
    pass

class TZ(tzinfo):
    def utcoffset(self, dt): 
        return timedelta(minutes=TIMEZONE_OFFSET)
    
class Date(Entry):
    def get_full(self):
        day = int(self.day)
        month = int(self.month) - 1
        weekday = WEEKDAYS[self.get_datetime().weekday()]
        return weekday + ', ' + str(day) + ' ' + LIST[month] + ' ' + str(self.year)

    def get_half(self):
        day = int(self.day)
        month = int(self.month) - 1
        weekday = WEEKDAYS[self.get_datetime().weekday()]
        return weekday + ', ' + str(day) + ' ' + LIST[month]

    def get_iso(self):
        return self.get_datetime().isoformat()

    def get_datetime(self):
        return datetime(int(self.year), int(self.month), int(self.day), int(self.minute), int(self.second), tzinfo=TZ())

class Post(Entry):
    def get_full(self):
        return self.content + self.description

    def get_url(self):
        return 'http://' + HOST + '/blog/' + self.date.year + '/' + self.date.month + '/' + self.date.day + '/' + \
            self.name + '/'

    def has_excluded_cats(self, exclude = EXCLUDE_CATEGORY):
        for category in self.categories:
            if category.name in exclude:
                return True;
        return False;

class Page(Entry):
    pass

class Press:
    def generate(self):
        self.load()
        self.load_first_press()
        print "Parsing done ..."
        self.gen_articles()
        print "Generation done ..."
        self.gen_pages()
        self.gen_categories()
        self.gen_archives()
        self.gen_feed()
        self.gen_subfeeds()
        self.gen_static()

    def load_first_press(self):
        year = datetime.now().year;
        for post in self.posts:
            if int(post.date.year) < year:
                year = post.date.year
        self.first_press = year

    def gen_articles(self):
        for post in self.posts:
            post_path = path.join(BLOG_PATH, post.date.year, post.date.month, post.date.day, post.name)
            rendered = self.render('article.html', post=post)
            self.write(post_path, rendered)

    def gen_pages(self):
        posts_filtered = []
        for post in self.posts:
            if post.has_excluded_cats():
                continue
            posts_filtered.append(post)
        size = len(posts_filtered)
        pages = math.ceil(float(size)/POST_PER_PAGE) if size > POST_PER_PAGE else 1
        i = 1
        while i <= pages:
            offset = i*POST_PER_PAGE - 10
            posts = posts_filtered[offset:offset+10]
            rendered = self.render('index.html', posts=posts, page=i, total_pages=pages)
            to = PUBLIC_PATH if i == 1 else path.join(BLOG_PATH, 'page', str(i))
            self.write(to, rendered)
            i += 1

    def gen_categories(self):
        categories = self.sort_by_categories(self.posts)
        for key, value in categories.iteritems():
            category_path = path.join(CATEGORIES, key.lower())
            print category_path
            rendered = self.render('categories.html', years=self.sort_by_years(value), categories=key)
            self.write(category_path, rendered)

    def gen_archives(self):
        rendered = self.render('categories.html', years=self.sort_by_years(self.posts, True))
        self.write(ARCHIVES, rendered)

    def gen_feed(self):
        posts_filtered = []
        for post in self.posts:
            if post.has_excluded_cats():
                continue
            posts_filtered.append(post)
        rendered = self.render('atom.xml', posts=posts_filtered)
        self.write(PUBLIC_PATH, rendered, 'atom.xml')

    def gen_subfeeds(self):
        feeds = self.sort_by_feeds(self.posts)
        for key, value in feeds.iteritems():
            category_path = path.join(CATEGORIES, key.link.lower())
            rendered = self.render('atom.xml', posts=value, category=key)
            self.write(category_path, rendered, 'atom.xml')

    def gen_static(self):
        for page in self.pages:
            rendered = self.render('page.html', page=page)
            self.write(path.join(PUBLIC_PATH, page.name), rendered)

    def render(self, template, **kwargs):
        template = self.get_base_template(template)
        config = {
            'host': HOST,
            'name': NAME,
            'author': AUTHOR,
            'date': "%s&mdash;%s" % (self.first_press, datetime.now().year),
            'pages': self.pages,
            'datetime_now': datetime.now().replace(tzinfo = TZ(), microsecond=0)
        }
        return template.render(dict(kwargs.items() + config.items()))

    def write(self, to, rendered, additional = 'index.html'):
        if not to.endswith('/'):
            to = to + '/'
        if not path.exists(path.dirname(to)):
            makedirs(path.dirname(to))
        with open(path.join(to, additional), "w") as file:
            file.write(rendered.encode('utf-8'))

    def get_base_template(self, name):
        template = Environment(loader=FileSystemLoader(path.join(PATH, TEMPLATE_PATH)))
        return template.get_template(name)

    def sort_by_years(self, posts, archive=False):
        years = {}
        include = {}
        if archive:
            for post in posts:
                if not (post.has_excluded_cats()):
                    include[post.date.year] = True
        for post in posts:
            if not archive or post.date.year in include:
                if not years.has_key(post.date.year):
                    years[post.date.year] = []
                if archive and (post.has_excluded_cats()):
                    pass
                else:
                    years[post.date.year].append(post)
        return reversed(sorted(years.iteritems()))

    def sort_by_categories(self, posts):
        categories = {}
        for post in posts:
            for category in post.categories:
                if not categories.has_key(category.link):
                    categories[category.link] = []
                categories[category.link].append(post)
        return categories
    
    def sort_by_feeds(self, posts):
        feeds = {}
        for post in posts:
            if not feeds.has_key(post.categories[0]):
                feeds[post.categories[0]] = []
            feeds[post.categories[0]].append(post)
        return feeds

class Octopress(Press):
    def load(self):
        self.posts = [self.parse_post(f) for f in reversed(listdir(POSTS_PATH))
            if path.isfile(path.join(POSTS_PATH, f)) and not f.startswith('.')
        ]
        self.pages = [self.parse_page(f) for f in reversed(listdir(PAGES_PATH))
            if path.isfile(path.join(PAGES_PATH, f))
        ]

    def parse_post(self, name):
        f = file(path.join(POSTS_PATH, name), "r")
        post = f.read().decode('utf-8')

        list = post.split('---')
        settings = list.pop(1)
        body = "".join(list)

        body_list = body.split('<!-- more -->')
        content = body_list.pop(0)
        description = "".join(body_list)

        time=re.search('(?<=time:).+', settings)
        if time:
            time = time.group(0).strip().split(':')

        categories = re.search('(?<=categories:).+', settings).group(0).strip()
        categoriesList = categories.split(',') if (',' in categories) else categories.split()

        for key, item in enumerate(categoriesList):
            categoryLink = categoryName = item.strip()
            if ('/' in item):
                splitted = item.split("/", 1)
                categoryLink = splitted[1].strip()
                categoryName = splitted[0].strip()
            categoriesList[key] = Category(link=categoryLink, name=categoryName)

        return Post(
            date=
                Date(
                    year=name[:4], 
                    month=name[5:7], 
                    day=name[8:10],
                    minute=time[0] if time else 0,
                    second=time[1] if time else 0
                ),
            name=name[11:-9],
            title=re.search('(?<=title:).+', settings).group(0).strip()[1:-1],
            content=markdown(content),
            description=markdown(description),
            categories=categoriesList
        )

    def parse_page(self, name):
        f = file(path.join(PAGES_PATH, name), "r")
        page = f.read().decode('utf-8')

        list = page.split('---')
        settings = list.pop(1)
        body = "".join(list)

        return Page(
            name=name[:-9],
            title=re.search('(?<=title:).+', settings).group(0).strip()[1:-1],
            content=markdown(body)
        )

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            action_generate()
            if self.path[-1:] == '/':
                self.path = self.path + 'index.html'
            f = open(PUBLIC_PATH + unquote(self.path))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return
        except IOError:
            self.send_error(404, 'File not found')

def action_sync():
    system("rsync -avrz %s %s" % (PUBLIC_PATH, SYNC_TO))
    print('Sync done ...')

def action_preview():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, Server)
    print('Http server is running ...')
    httpd.serve_forever()

def action_generate():
    engine = globals()[STRATEGY.title()]()
    engine.generate()

def action_gp():
    action_generate()
    action_preview()

def action_gs():
    action_generate()
    action_sync()

def action_add(name=('n', '')):
    post_dst = POSTS_PATH + time.strftime("%Y-%m-%d") + '-' + name + '.markdown'
    copyfile(TEMPLATE_PATH + 'base.markdown', post_dst)
    system("vim " + post_dst)

def action_rm(name=('r', '')):
    remove(POSTS_PATH + time.strftime("%Y-%m-%d") + '-' + name + '.markdown')

def action_commit():
    system("cd " + POSTS_PATH + "; git add . ; git commit -m 'up'; git push;")

if __name__ == '__main__':
    script.run()
