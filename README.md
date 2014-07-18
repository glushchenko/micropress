## Micropress

Micropress – Python blog generator for hackers.  

- open source  
- jinja templates  
- configurable directories and configs  
- smart file tree organization  
- markdown markup  
- auto detect changes and generation  
- auto upload  
- auto filling post time  
- live preview at [http://127.0.0.1:8080](http://127.0.0.1:8080)

### Install

``sudo pip install micropress``  
``micropress init`` — install default (~/.microrc) and default 
templates (~/Documents/Micropress/) directory.

### Config

``vim ~/.microrc``

    [system]
    author = fluder
    host = fluder.co
    name = Geek Blog
    timezone_offset = 120
    post_per_page = 10
    exclude_category = How-to

    [storage]
    build = ~/.build/micropress
    public = ~/Documents/Micropress/public
    templates = ~/Documents/Micropress/templates
    pages = ~/Documents/Micropress/sources/pages
    posts = ~/Documents/Micropress/sources/posts

    [sync]
    to = remote.host.name:/path/to/www # rsync path
    key = ~/.ssh/id_rsa # ssh key for autosync feature

    [locale]
    month = January, February, March, April, May, June, July, August, September, October, November, December
    days = Mon, Tue, Wed, Thu, Fri, Sat, Sun

### Usage 

``micropress add post-name`` then just write post, save and exit, working like a
charm.

#### Linux 

``micropress preview`` — start webserver preview  
``micropress watch`` — start file changes watcher  

#### Manual mode

``micropress generate`` — save public and generated content into build
directory.  
``micropress sync`` — upload content on production server.  

### Uninstall

``pip uninstall micropress``  
``rm ~/.microrc``  
``rm -r ~/Documents/Micropress``  
``launchctl unload -w co.fluder.micropress.watcher.plist``  
``launchctl unload -w co.fluder.micropress.preview.plist``  
``rm -r ~/Library/LaunchAgents/co.fluder.micropress.watcher.plist``  
``rm -r ~/Library/LaunchAgents/co.fluder.micropress.preview.plist``

### Templates 

Template engine is [Jinja2](http://jinja.pocoo.org/docs/), full support
features.

### Headers

    ---
    title: ""
    categories: View name/Link name
    time: -        # automatic change on save if autosync enabled
    autosync: true # automatic upload after edit
    ---
