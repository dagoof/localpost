from jinja2 import Environment,FileSystemLoader,PackageLoader
from odict import OrderedDict
import pycassa

client=pycassa.connect()
Users=pycassa.ColumnFamily(client, 'localpost', 'Users')
UserName=pycassa.ColumnFamily(client, 'localpost', 'UserName')
Posts=pycassa.ColumnFamily(client, 'localpost', 'post')
PostOrder=pycassa.ColumnFamily(client, 'localpost', 'postorder', dict_class=OrderedDict)

def render_template(template_name, **vars):
    jinja_env=Environment(loader=PackageLoader('serv', 'templates'))
    return jinja_env.get_template(template_name).render(vars)
