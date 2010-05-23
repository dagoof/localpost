import web, views

class Upperware:
    def __init__(self, app):
        self.wrapped_app=app
    def __call__(self, environ, start_response):
        for data in self.wrapped_app(environ, start_response):
            return data.upper()

urls=(
    '/user/(.*)', 'views.User',
    '/note/([\w-]+)', 'views.Note',
    '/list', 'views.ListUser',
    '/login', 'views.Login',
    '/new_note', 'views.NewNote',
)

if __name__=='__main__':
    app=web.application(urls, globals())
    print 'serving on 8088'
    app.run()
