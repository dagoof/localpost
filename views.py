import time, struct, os
from utils import render_template, Users, UserName, Posts, PostOrder

class ListUser:
    def GET(self):
        return render_template('index_template.html', users=[u[1] for u in Users.get_range()])

class User:
    def GET(self, name):
        def get_userid(name):
            try:
                return Users.get(UserName.get(name)['id'])
            except:
                return False
        def get_posts(userid):
            try:
                posts=[]
                for post in PostOrder.get(userid, column_reversed=True).values():
                    p=Posts.get(post)
                    p['tstring']=time.strftime(' %I:%M%P %B %d', time.localtime(sum(struct.unpack('>d',p['_ts']))/1e6)).replace(' 0', ' ')
                    posts.append(p)
                return posts
            except:
                return []
        user=get_userid(name)
        if user:
            return render_template('user_template.html', user=user, posts=get_posts(user['id']))

class Note:
    def GET(self, postid):
        try:
            post=Posts.get(postid)
            post['tstring']=time.strftime(' %I:%M%P %B %d', time.localtime(sum(struct.unpack('>d',post['_ts']))/1e6)).replace(' 0', ' ')
            user=Users.get(post['user_id'])
            print post
        except pycassa.NotFoundException:
            post,user={'body':'Not found','id':'404'},{'name':'404'}
            print post,user
        return render_template('user_template.html', user=user, posts=[post])
