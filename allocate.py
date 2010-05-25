import pycassa, hashlib, struct, uuid, time

client=pycassa.connect()
Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')
Posts=pycassa.ColumnFamily(client, 'localpost', 'Posts')
PostOrder=pycassa.ColumnFamily(client, 'localpost', 'Postorder')
FollowerOrder=pycassa.ColumnFamily(client, 'localpost', 'FollowerOrder')
Followers=pycassa.ColumnFamily(client, 'localpost', 'Followers')
Sessions=pycassa.ColumnFamily(client, 'localpost', 'Sessions')

def _long(ts):
    return struct.pack('>d', long(ts))

def addUser(user):
    Users.insert(user.id, user.dumps())
    UserName.insert(user.name, {'id': user.id})

def addPost(post):
    Posts.insert(post.id, post.dumps())
    PostOrder.insert(post.author, {post._ts: post.id})

def addSession(session):
    Sessions.insert(session.id, session.dumps())
    Users.insert(session.user_id, {'current_session':session.id})

class User:
    def __init__(self, name, password):
        self.name=name
        self.password=hashlib.sha1(password).hexdigest()
        self.id=uuid.uuid4().get_hex()

    def __repr__(self):
        return '<{object} {id}: {name}, {passw}>'.format(
            object=self.__class__.__name__,
            id=self.id,
            name=self.name,
            passw=self.password)

    def dumps(self):
        return {'name':self.name,
            'password':self.password,
            'id':self.id}

class Post:
    def __init__(self, author, body):
        self.author=UserName.get(author)['id']
        self.body=body
        self.id=uuid.uuid4().get_hex()
        self._ts=_long(int(time.time()*1e6))
    
    def __repr__(self):
        return '<{object} {id}: {author}, {body}>'.format(
            object=self.__class__.__name__,
            id=self.id,
            author=self.author,
            body=self.body[:50])

    def dumps(self):
        return {'user_id':self.author,
            'body':self.body,
            'id':self.id,
            '_ts':self._ts}

class Session:
    def __init__(self, user):
        self.user_id=user.get('id')
        self.user_name=user.get('name')
        self.id=uuid.uuid4().get_hex()
        self.status=user.get('type', 'member')

    def __repr__(self):
        return '<{object} {id}: {status} - {user}, {userid}>'.format(
            object=self.__class__.__name__,
            id=self.id,
            status=self.status,
            user=self.user_name,
            userid=self.user_id)

    def dumps(self):
        return {'user_id':self.user_id,
            'id':self.id,
            'status':self.status,
            'user_name':self.user_name}


# {'zzqNate':'lolfag', 'peter':'bear', 'diggs':'diggs', 'linda':'linda', 'sasucker':'da', 'gwoolhurme', 'gwouel', 'gus':'gus', 'tenaciousp':'tenp'}
#u={'Frostfist':'ffist', 'Pontifica':'pont', 'Shadereign':'sreign', 'SlowCow':'slow', 'Stimpsy':'stimp', 'Rizenbul':'riz', 'geheim':'geh', 'EarthQuail':'eq', 'shadowyrn':'swyn'}
