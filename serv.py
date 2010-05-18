import web, views

urls=(
    '/user/(.*)', 'views.User',
    '/note/([\w-]+)', 'views.Note',
    '/list', 'views.ListUser',
)

if __name__=='__main__':
    app=web.application(urls, globals())
    print 'serving on 8088'
    app.run()
