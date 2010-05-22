from jinja2 import Environment,FileSystemLoader,PackageLoader
from odict import OrderedDict
from allocate import User, Post, addUser, addPost
import pycassa, time, struct, os

client=pycassa.connect()
Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')
Posts=pycassa.ColumnFamily(client, 'localpost', 'Posts')
PostOrder=pycassa.ColumnFamily(client, 'localpost', 'Postorder', dict_class=OrderedDict)
Followers=pycassa.ColumnFamily(client, 'localpost', 'Followers')
Sessions=pycassa.ColumnFamily(client, 'localpost', 'Sessions')

def render_template(template_name, **vars):
    jinja_env=Environment(loader=PackageLoader('serv', 'templates'))
    return jinja_env.get_template(template_name).render(vars)

def get_userid(name):
    try:
        return Users.get(UserName.get(name).get('id'))
    except:
        return False

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

class RequireLogin:
    def __init__(self, function):
        self._function=function

    def logged_in(self):
        #Cookie shit
        return True
    def __call__(self, *args, **kwargs):
        if logged_in:
            return self._function(*args, **kwargs)
        else:
            raise web.seeother('/login')
