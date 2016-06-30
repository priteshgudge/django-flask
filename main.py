# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from data.models import *


#Add user
#user = User(name="Pritesh", email="mail@priteshgudge.com")
#user.save()

# Application logic
first_user = User.objects.all()[0]

print(first_user.name)
print(first_user.email)

for user in User.objects.all():
	print user.name,user.email
	
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]


db_task =Task(id=1,title='Buy Groceries',
			description='Milk, Cheese, Pizza, Fruit, Tylenol',
			done=False)
db_task.save()

db_task =Task(id=2,title='Learn Python',
			description='Meed to find a good Python tutorial on the web',
			done=False)
db_task.save()
db_task.id = 3
db_task.save()
	
tasks = Task.objects.all()

for task in tasks:
	print task
