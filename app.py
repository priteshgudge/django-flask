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
	tasks_ser= serializers.serialize('json',tasks)
	#gen = [c['fields'] for c in tasks_ser]
	dictionaries = [ task.as_dict() for task in tasks ]
	#return HttpResponse(json.dumps({"data": dictionaries}), content_type='application/json')
	#return HttpResponse(json.dumps({"data": dictionaries}), content_type='application/json')
	return jsonify({'tasks': dictionaries})
	#return jsonify({'tasks':[make_public_task(task) for task in tasks]})
	
@app.route('/todo/api/v1.0/tasks/<int:taskid>',methods=['GET'])
def get_task(taskid):
	tasks = Task.objects.all()
	task = [task for task in tasks if task.id == taskid]
	print "Get Task"
	if len(task) == 0:
		abort(404) 
	return jsonify({'tasks':make_public_task(task[0])})

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
	
	max = Task.objects.all().aggregate(Max('id'))['rating__max']
	db_task = Task.objects.create(id = max+1,
					title = request.json['title'],
					description=request.json.get('description',""),
					done=False)
	#print task
	#tasks.append(task)
	db_task.save()
	return jsonify({'tasks':tasks})
	
@app.route('/todo/api/v1.0/tasks/<int:taskid>', methods=['PUT'])
def update_task(taskid):
	tasks = Task.objects.all()
	task = [task for task in tasks if taskid == task.id]
	#print task,len(task)
	#print request.json['title']
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
	#print task
	task.title = request.json.get(u'title',task.title)
	task.description = request.json.get(u'description',task.description)
	task.done = request.json.get(u'done',task.done )

	return jsonify({'task':task})

@app.route('/todo/api/v1.0/tasks/<int:taskid>', methods=['DELETE'])
def delete_task(taskid):
	task = [task for task in tasks if taskid == task.id]
	
	if not len(task):
		abort(404)
	task.delete()
	return jsonify({'result':True})
	
from flask import url_for

def make_public_task(task):
	new_task = copy.deepcopy(task)
	print "Here"

	new_task.uri = url_for('get_task',taskid=task.id,_external=True)
		
	return new_task
	

if __name__ == '__main__':
	app.run(debug=True)