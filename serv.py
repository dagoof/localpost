import web, pycassa
from odict import OrderedDict

client=pycassa.connect()
render=web.template.render('templates/')
urls=(
	'/user/(.*)', 'User',
	'/list', 'ListUser',
)
app=web.application(urls, globals())

Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')
Post=pycassa.ColumnFamily(client, 'localpost', 'post')
PostOrder=pycassa.ColumnFamily(client, 'localpost', 'postorder', dict_class=OrderedDict)

class ListUser:
	def GET(self):
		return render.index([u[1] for u in Users.get_range()])

class User:
	def GET(self, Name):
		try:
			user=Users.get(UserName.get(Name)['id'])
		except:
			return render.fourohfour()
		else:
			try:
				posts=[Post.get(id) for id in PostOrder.get(user['id']).values()]
			except:
				posts=[]

		return render.base_template(user, posts)

if __name__=='__main__':
	app.run()
