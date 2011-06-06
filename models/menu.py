# -*- coding: utf-8 -*-

response.title = 'SISVENTI'
response.subtitle = T('customize me!')

#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'you'
response.meta.description = 'Free and open source full-stack enterprise framework for agile development of fast, scalable, secure and portable database-driven web-based applications. Written and programmable in Python'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2007-2010'


response.menu = [
    (T('Home'), False, URL('default','index'), [])
    ]

response.menu+=[
    (T('This App'), False, URL('admin', 'default', 'design/%s' % request.application),
     [
            (T('Controller'), False,
             URL('admin', 'default', 'edit/%s/controllers/%s.py' \
                     % (request.application,request.controller=='appadmin' and
                        'default' or request.controller))),
            (T('View'), False,
             URL('admin', 'default', 'edit/%s/views/%s' \
                     % (request.application,response.view))),
            (T('Layout'), False,
             URL('admin', 'default', 'edit/%s/views/layout.html' \
                     % request.application)),
            (T('Stylesheet'), False,
             URL('admin', 'default', 'edit/%s/static/base.css' \
                     % request.application)),
            (T('DB Model'), False,
             URL('admin', 'default', 'edit/%s/models/db.py' \
                     % request.application)),
            (T('Menu Model'), False,
             URL('admin', 'default', 'edit/%s/models/menu.py' \
                     % request.application)),
            (T('Database'), False,
             URL(request.application, 'appadmin', 'index')),

            (T('Errors'), False,
             URL('admin', 'default', 'errors/%s' \
                     % request.application)),

            (T('About'), False,
             URL('admin', 'default', 'about/%s' \
                     % request.application)),

            ]
   )]
