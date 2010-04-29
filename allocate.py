import pycassa, hashlib, struct, uuid, time

client=pycassa.connect()
Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')
Poste=pycassa.ColumnFamily(client, 'localpost', 'post')
PostOrder=pycassa.ColumnFamily(client, 'localpost', 'postorder')


def _long(ts):
	return struct.pack('>d', long(ts))

def addUser(user):
	Users.insert(user.id, user.dumps())
	UserName.insert(user.name, {'id': user.id})

def addPost(post):
	Poste.insert(post.id, post.dumps())
	PostOrder.insert(post.author, {post._ts: post.id})

class User:
	def __init__(self, name, password):
		self.name=name
		self.password=hashlib.sha1(password).hexdigest()
		self.id=str(uuid.uuid4())

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
		self.id=str(uuid.uuid4())
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

		



	
# {'zzqNate':'lolfag', 'peter':'bear', 'diggs':'diggs', 'linda':'linda', 'sasucker':'da', 'gwoolhurme', 'gwouel', 'gus':'gus', 'tenaciousp':'tenp'}
#u={'Frostfist':'ffist', 'Pontifica':'pont', 'Shadereign':'sreign', 'SlowCow':'slow', 'Stimpsy':'stimp', 'Rizenbul':'riz', 'geheim':'geh', 'EarthQuail':'eq', 'shadowyrn':'swyn'}
