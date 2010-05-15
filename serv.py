from gevent import monkey; monkey.patch_all()
from gevent.wsgi import WSGIServer
import gevent
import web, pycassa
from odict import OrderedDict

client=pycassa.connect()
render=web.template.render('templates/')
urls=(
	'/user/(.*)', 'User',
	'/list', 'ListUser',
)

Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')
Post=pycassa.ColumnFamily(client, 'localpost', 'post')
PostOrder=pycassa.ColumnFamily(client, 'localpost', 'postorder', dict_class=OrderedDict)

class ListUser:
	def GET(self):
		return render.index([u[1] for u in Users.get_range()])

class User:
    def GET(self, name):
        def get_userid(name):
            try:
                return Users.get(UserName.get(name)['id'])
            except pycassa.NotFoundException:
                return False

        def get_posts(userid):
            try:
                posts=[Post.get(id) for id in PostOrder.get(userid).values()]
                for post in posts:
                    post['first']=post['body'].split(' ')[0]
                    post['body_remainder']=' '.join(post['body'].split(' ')[1:])
                return posts
                #return [Post.get(id) for id in PostOrder.get(userid).values()]
            except pycassa.NotFoundException:
                return []

        user=get_userid(name)
        if user:
            return render.base_template(user, get_posts(user['id']))

if __name__=='__main__':
    app=web.application(urls, globals())#.wsgifunc()
    print 'serving on 8088'
    #WSGIServer(('', 8088), app).serve_forever()
    app.run()
