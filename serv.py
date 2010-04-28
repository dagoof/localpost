import web, pycassa

client=pycassa.connect()
render=web.template.render('templates/')
urls=(
	'/user/(.*)', 'User',
	'/list', 'ListUser',
)
app=web.application(urls, globals())

Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')

class ListUser:
	def GET(self):
		return render.index([Users.get(un) for un in UserName.get('id').values()])
	#return render.index([u[1] for u in Users.get_range()])

class User:
	def GET(self, Name):
		try:
			name=Users.get(UserName.get('id')[Name])
		except:
			name=Users.get(UserName.get('id')['404'])

		return render.base_template({'name':name['name'], 'd':name, 'posts':['testpost', 'testpost2']})

if __name__=='__main__':
	app.run()
