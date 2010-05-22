import web, views

urls=(
    '/user/(.*)', 'views.User',
    '/note/([\w-]+)', 'views.Note',
    '/list', 'views.ListUser',
    '/login', 'views.Login',
)

if __name__=='__main__':
    app=web.application(urls, globals())
    print 'serving on 8088'
    app.run()
