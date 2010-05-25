from jinja2 import Environment,FileSystemLoader,PackageLoader
from odict import OrderedDict
from allocate import User, Post, addUser, addPost
import pycassa, time, struct, os
import web

client=pycassa.connect()
Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')
Posts=pycassa.ColumnFamily(client, 'localpost', 'Posts')
PostOrder=pycassa.ColumnFamily(client, 'localpost', 'Postorder', dict_class=OrderedDict)
FollowerOrder=pycassa.ColumnFamily(client, 'localpost', 'FollowerOrder', dict_class=OrderedDict)
Followers=pycassa.ColumnFamily(client, 'localpost', 'Followers')
Sessions=pycassa.ColumnFamily(client, 'localpost', 'Sessions')

jinja_env=Environment(loader=PackageLoader('serv', 'templates'))

def render_template(template_name, **vars):
    def logged_in():
        return get_session(web.cookies().get('localpost_sessionid'))
    jinja_env.globals['logged_in']=get_session(web.cookies().get('localpost_sessionid'))
    return jinja_env.get_template(template_name).render(vars)

def get_userid(name):
    try:
        return Users.get(UserName.get(name).get('id'))
    except:
        return False

def get_session(sessionid):
    try:
        return Sessions.get(sessionid)
    except:
        return False

def get_current_user():
    return Users.get(get_session(web.cookies().get('localpost_sessionid')).get('user_id'))

def pack_post(postid):
    p=Posts.get(postid)
    p['tstring']=time.strftime(' %I:%M%P %B %d', time.localtime(sum(struct.unpack('>d',p['_ts']))/1e6)).replace(' 0', ' ')
    return p

def get_posts(userid):
    posts=[]
    try:
        for post in PostOrder.get(userid, column_reversed=True).values():
            p=Posts.get(post)
            posts.append(pack_post(post))
    except:
        #TODO: 404?
        print 'none found'
    finally:
        return posts

def get_timeline(userid):
    posts=[]
    try:
        for post in FollowerOrder.get(userid, column_reversed=True).values():
            p=Post.get(post)
            posts.append(pack_post(post))
    except:
        print 'none found'
    finally:
        return posts

def requireLogin(f):
    def call(*args, **kwargs):
        session=web.cookies().get('localpost_sessionid')
        if get_session(session):
            #kwargs.update({'logged_in':True})
            return f(*args, **kwargs)
        else:
            raise web.seeother('/login')
    return call

class RequireLogin:
    def __init__(self, function):
        self._function=function
    def logged_in(self):
        return web.cookies().get('sessionid')
    def __call__(self, *args, **kwargs):
        if self.logged_in():
            return self._function(self._function, *args, **kwargs)
        else:
            raise web.seeother('/login')
