from flask import Flask,jsonify,request
from flask import url_for,abort,make_response
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

is_abort = True
tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@auth.get_password
def get_password(username):
    """认证函数"""
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def make_public_task(task):
    """将id以url的形式返回,以便客户端可以随时使用"""
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['url'] = url_for('get-task', _external=True) +'/{}'.format(task['id'])
        else:
            new_task[field] = task[field]
    return new_task

@app.errorhandler(404)
def not_found(error):
    """404错误"""
    return make_response(jsonify({'error':'sorry Resources not found'}))

@app.route('/todo/api/v1.0/tasks',methods=['GET'],endpoint="get-task")
def get_tasks():
    #return jsonify({'code':0,'tasks':tasks})
    return jsonify({'tasks': list(map(make_public_task, tasks))})

@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['GET'])
def getone_task(task_id):
    task = list(filter(lambda t:t['id'] == int(task_id),tasks))
    if len(task) == 0:
        if is_abort:
            abort(404)
        else:
            return jsonify({'code': -1, 'msg': 'task is not exits'})
    return jsonify({'code':0,'tasks':task[0]})

@app.route('/todo/api/v1.0/tasks',methods=['post'])
def create_task():
    if not request.json:
        abort(404)
    try:
        title = request.json['title']
        description = request.json['description']
    except KeyError as e:
        return jsonify({'code':-1,'msg':'key error'})

    id = tasks[-1]['id'] + 1
    tasks.append({'id':id,'title':title,'description':description,'done':False})
    return jsonify({'code':0,'task':tasks[-1]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['PUT'])
def update_task(task_id):
    if not request.json:
        abort(404)
    task = list(filter(lambda t:t['id'] == int(task_id),tasks))
    if len(task) == 0:
        if is_abort:
            abort(404)
        else:
            return jsonify({'code': -1, 'msg': 'task is not exits'})
    try:
        task[0]['title'] = request.json.get('title', task[0]['title'])
        task[0]['description'] = request.json.get('description', task[0]['description'])
        task[0]['done'] = request.json.get('done', task[0]['done'])
    except KeyError as e:
        return jsonify({'code':-1,'msg':'key error'})
    return jsonify({'code':0,'task':task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['DELETE'])
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == int(task_id), tasks))
    if len(task) == 0:
        if is_abort:
            abort(404)
        else:
            return jsonify({'code': -1, 'msg': 'task is not exits'})
    tasks.remove(task[0])
    return jsonify({'code':0,'task':task[0]})

if __name__ == '__main__':
    app.run("0.0.0.0",8088,debug=True)
