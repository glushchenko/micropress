# Micropress

Micropress – Python blog generator for hackers.  

## Install

``pip install micropress``  
``micropress init`` — install config in home (~/.microrc) and default templates in ~/Documents/Micropress/ directory.   

## Config

``vim ~/.microrc``

## Usage 

``micropress generate`` — save public and generated content into build directory.   
``micropress sync`` — upload content in production server.  

## Uninstall

``pip uninstall micropress``  
``rm ~/.microrc``  
``rm -r ~/Documents/Micropress``  

--

## Установка

``pip install micropress``
``micropress init`` — копирует начальный конфиг в домашнюю директорию (~/.microrc) и шаблоны по умолчанию в ~/Documents/Micropress/.

## Конфиг

vim ~/.microrc

    [system]
    # авторство, по умолчанию этот ник используется как логин в дискасе
    author = Micropress 
    
    # хост, в моём случае fluder.co, нужен для всех ссылок
    host = host.name 
    
    # название блога в шаблонах
    name = Micropress Blog 
    
    # таймзон, используется для строгого определения времени в RSS, 120 — означает GMT+2
    timezone_offset = 0 
    
    # количество постов на страницу
    post_per_page = 10 

    [storage]
    # сюда собирается блог после генерации
    build = ~/tmp/micropress
    
    # статические файлы, которые копируются в билд перед генерацией, robots.txt и т.д.
    public = ~/Documents/Micropress/public 
    
    # шаблоны
    templates = ~/Documents/Micropress/templates
    
    # страницы вне ленты
    pages = ~/Documents/Micropress/sources/pages
     
    # посты в ленте
    posts = ~/Documents/Micropress/sources/posts 

    [sync]
    # сюда выкладываем то, что есть в билд директории (через rsync)
    to = remote.host.name:/path/to/www

    [locale]
    # локализация месяцев
    month = Января, Февраля, Марта, Апреля, Мая, Июня, Июля, Августа, Сентября, Октября, Ноября, Декабря
    
    # дней недели
    days = Пн, Вт, Ср, Чт, Пт, Сб, Вс

## Шаблоны

Синтаксис шаблонов построен на [Jinja2](http://jinja.pocoo.org/docs/). Вы можете использовать в полной мере все фичи 
этого шаблонизатора.

## Использование 

``micropress generate`` — сгенерировать страницы по набранным новостям и шаблонам (копируется в ~/Documents/Micropress/build/ по умолчанию)     
``micropress sync`` — выложить контент на свой сервер (путь указывается в конфиге [sync] to).  

## Удаление

``pip uninstall micropress``  
``rm ~/.microrc``  
``rm -r ~/Documents/Micropress``  

