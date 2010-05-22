from utils import render_template, Users, UserName, Posts, PostOrder, get_posts, get_userid, pack_post
from forms import post_form
import hashlib
import web

def login_met(name, passw):
    def password_valid(n, p):
        print get_userid(n), Users.get(get_userid(n).get('id')).get('password')
        if hashlib.sha1(p).hexdigest()==Users.get(get_userid(n).get('id')).get('password'):
            return True
        else:
            return False

    if get_userid(name) and password_valid(name, passw):
        return True
    else:
        return False

class ListUser:
    def GET(self):
        return render_template('index_template.html', users=[u[1] for u in Users.get_range()])

class User:
    def GET(self, name):
        user=get_userid(name)
        print user
        if user:
            print get_posts(user['id'])
            return render_template('user_template.html', user=user, posts=get_posts(user['id']))

class Note:
    def GET(self, postid):
        try:
            post=pack_post(postid)
            user=Users.get(post['user_id'])
        except:
            post,user={'body':'Not found','id':'404'},{'name':'404'}
        return render_template('user_template.html', user=user, posts=[post])

class Login:
    def GET(self):
        f=post_form()
        return render_template('login.html',f=f)

    def POST(self):
        f=post_form()
        if f.validates():
            print 'validated'
            username=f.username.value
            password=f.password.value
            user=get_userid(username)
            print username, password, user
            if user and user.get('password')==hashlib.sha1(password).hexdigest():
                sessionid=web.input(sessionid='300')
                web.setcookie('sessionid', sessionid, 3600)
                raise web.seeother('/list')
        print 'back to login @_@'
        return render_template('login.html', f=f)
