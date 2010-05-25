from utils import *
import simplejson
from allocate import Session, addSession
#render_template, Users, UserName, Posts, PostOrder, get_posts, get_userid, pack_post, RequireLogin, requirelogin
from forms import post_form, note_form
import hashlib
import web

class GenerateUsers:
    def GET(self, name):
        return simplejson.dumps([{u[1].get('name'):u[1].get('id')} for u in Users.get_range() if name in u[1].get('name')])

class ListUser:
    def GET(self):
        return render_template('index_template.html', users=[u[1] for u in Users.get_range()])

class User:
    def GET(self, name):
        user=get_userid(name)
        if user:
            return render_template('user_template.html', user=user, posts=get_posts(user['id']))

class Follow:
    @requireLogin
    def GET(self):
        return render_template('ajax_form.html')

class Login:
    def GET(self):
        f=post_form()
        return render_template('generic_form.html',f=f)

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
        return render_template('generic_form.html', f=f)

class Note:
    def GET(self, postid):
        try:
            post=pack_post(postid)
        except:
            post,user={'body':'Not found','id':'404'},{'name':'404'}
        return render_template('user_template.html', user={'name':post['user_name']}, posts=[post])

class NewNote:
    def GET(self):
        f=note_form()
        return render_template('generic_form.html', f=f)

    @requireLogin
    def POST(self):
        f=note_form()
        if f.validates():
            note_body=f.note_body.value
            user=get_current_user()
            addPost(Post(user.get('name'), note_body))
            raise web.seeother('/user/{u}'.format(u=user.get('name')))
        return render_template('generic_form.html',f=f)

class Timeline:
    @requireLogin
    def GET(self):
        user=get_current_user()
        return render_template('user_template.html', user=user, posts=get_timeline(user['id']))

class ToggleFollowing:
    @requireLogin
    def GET(self, name):
        followee=get_userid(name)
        user=get_current_user()
        if followee:
            Followers.insert(followee['id'], {user.get('id'):user.get('name')})
