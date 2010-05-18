import web, pycassa, time, struct, os
from odict import OrderedDict
from jinja2 import Environment,FileSystemLoader

client=pycassa.connect()
#render=web.template.render('templates/')
def render_template(template_name, **context):
    extensions=context.pop('extensions', [])
    globals=context.pop('globals',{})
    jinja_env=Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        extensions=extensions,
    )
    jinja_env.globals.update(globals)
    return jinja_env.get_template(template_name).render(context)

urls=(
    '/user/(.*)', 'User',
    '/note/([\w-]+)', 'Note',
    '/list', 'ListUser',
)

Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')
Post=pycassa.ColumnFamily(client, 'localpost', 'post')
PostOrder=pycassa.ColumnFamily(client, 'localpost', 'postorder', dict_class=OrderedDict)

class ListUser:
    def GET(self):
        return render_template('index_template.html', users=[u[1] for u in Users.get_range()])

class User:
    def GET(self, name):
        def get_userid(name):
            try:
                return Users.get(UserName.get(name)['id'])
            except pycassa.NotFoundException:
                return False

        def get_posts(userid):
            try:
                posts=[]
                for post in PostOrder.get(userid, column_reversed=True).values():
                    p=Post.get(post)
                    p['tstring']=time.strftime(' %I:%M%P %B %d', time.localtime(sum(struct.unpack('>d',p['_ts']))/1e6)).replace(' 0', ' ')
                    posts.append(p)
                return posts
            except pycassa.NotFoundException:
                return []

        user=get_userid(name)
        if user:
            return render_template('user_template.html', user=user, posts=get_posts(user['id']))

class Note:
    def GET(self, postid):
        try:
            post=Post.get(postid)
            post['tstring']=time.strftime(' %I:%M%P %B %d', time.localtime(sum(struct.unpack('>d',post['_ts']))/1e6)).replace(' 0', ' ')
            user=Users.get(post['user_id'])
            print post
        except pycassa.NotFoundException:
            post,user={'body':'Not found','id':'404'},{'name':'404'}
            print post,user

        return render_template('user_template.html', user=user, posts=[post])

if __name__=='__main__':
    app=web.application(urls, globals())
    print 'serving on 8088'
    app.run()
