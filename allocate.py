import pycassa, hashlib, struct, uuid

client=pycassa.connect()
Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')

def addUser(user):
	Users.insert(user.id, user.dumps())
	UserName.insert('id', {user.name: user.id})

class User:
	def __init__(self, name, password, cc=None):
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
	
# {'zzqNate':'lolfag', 'peter':'bear', 'diggs':'diggs', 'linda':'linda', 'sasucker':'da', 'gwoolhurme', 'gwouel', 'gus':'gus', 'tenaciousp':'tenp'}
#u={'Frostfist':'ffist', 'Pontifica':'pont', 'Shadereign':'sreign', 'SlowCow':'slow', 'Stimpsy':'stimp', 'Rizenbul':'riz', 'geheim':'geh', 'EarthQuail':'eq', 'shadowyrn':'swyn'}
