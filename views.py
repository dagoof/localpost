from utils import *
from allocate import Session, addSession
#render_template, Users, UserName, Posts, PostOrder, get_posts, get_userid, pack_post, RequireLogin, requirelogin
from forms import post_form
import hashlib
import web

class ListUser:
    def GET(self):
        return render_template('index_template.html', users=[u[1] for u in Users.get_range()])

class User:
    def GET(self, name):
        user=get_userid(name)
        if user:
            return render_template('user_template.html', user=user, posts=get_posts(user['id']))

class Note:
    @requireLogin
    def GET(self, postid, **kwargs):
        try:
            post=pack_post(postid)
            user=Users.get(post['user_id'])
        except:
            post,user={'body':'Not found','id':'404'},{'name':'404'}
        return render_template('user_template.html', user=user, posts=[post], **kwargs)

class Login:
    def GET(self):
        f=post_form()
        return render_template('login.html',f=f)

    def POST(self):
        f=post_form()
        if f.validates():
            username, password=f.username.value, f.password.value
            user=get_userid(username)
            if user and user.get('password')==hashlib.sha1(password).hexdigest():
                s=Session(user)
                addSession(s)
                web.setcookie('localpost_sessionid', s.dumps().get('id'), 604800)
                raise web.seeother('/list')
        return render_template('login.html', f=f)
