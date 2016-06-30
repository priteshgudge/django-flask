#!flask/bin/python
import copy
from flask import Flask, jsonify, make_response, abort,request

app = Flask(__name__)

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from data.models import *
from django.db.models import Max
from django.core import serializers




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

@app.route('/todo/api/v1.0/tasks',methods=['GET'])
def get_tasks():
	tasks = Task.objects.all()
	tasks_pub = (make_public_task(task) for task in tasks)
	dictionaries = [ task.as_dict() for task in tasks_pub]
	return jsonify({'tasks': dictionaries})
		
@app.route('/todo/api/v1.0/tasks/<int:taskid>',methods=['GET'])
def get_task(taskid):
	tasks = Task.objects.all()
	task = [task for task in tasks if task.id == taskid]
	#print "Get Task"
	if len(task) == 0:
		abort(404) 
	task_pub = make_public_task(task[0])
	dictionaries = [task_pub.as_dict()]
	return jsonify({'tasks':dictionaries})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not Found'}),404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error':'Bad Request','description':
	'Send correct input'}),400)
	
@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def create_task():
	#print request.json
	if not request.json or not 'title' in request.json:
		abort(400)
	
	max = Task.objects.all().aggregate(Max('id'))['id__max']
	db_task = Task.objects.create(id = max+1,
					title = request.json['title'],
					description=request.json.get('description',""),
					done=False)

	db_task.save()
	task_pub = make_public_task(db_task)
	dictionaries = [ task_pub.as_dict()]
	return jsonify({'tasks':dictionaries})
	
@app.route('/todo/api/v1.0/tasks/<int:taskid>', methods=['PUT'])
def update_task(taskid):
	tasks = Task.objects.all()
	task = [task for task in tasks if taskid == task.id]
	
	if not len(task):
		abort(404)
	if not request.json:
		abort(400)
	if 'title' in request.json and type(request.json['title']) != unicode:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
	if 'done' in request.json and type(request.json[u'done']) is not bool:
		abort(400)
	task = task[0]
	task.title = request.json.get(u'title',task.title)
	task.description = request.json.get(u'description',task.description)
	task.done = request.json.get(u'done',task.done )
	task.save()
	task_pub = make_public_task(task)
	dictionaries = [ task_pub.as_dict()]
	return jsonify({'task':dictionaries})

@app.route('/todo/api/v1.0/tasks/<int:taskid>', methods=['DELETE'])
def delete_task(taskid):
	tasks = Task.objects.all()
	task = [task for task in tasks if taskid == task.id]
	
	if not len(task):
		abort(404)
	task[0].delete()
	return jsonify({'result':True})
	
from flask import url_for

def make_public_task(task):
	new_task = copy.deepcopy(task)

	new_task.uri = url_for('get_task',taskid=task.id,_external=True)
		
	return new_task
	

if __name__ == '__main__':
	app.run(debug=True)