from flask import Flask,jsonify,request
from flask import url_for,abort,make_response
from flask_restful import Resource,Api,reqparse

app = Flask(__name__)
api = Api(app)


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


def make_public_task(task):
    """将id以url的形式返回,以便客户端可以随时使用"""
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['url'] = url_for('tasks', _external=True) +'/{}'.format(task['id'])
        else:
            new_task[field] = task[field]
    return new_task

@app.errorhandler(404)
def not_found(error):
    """404错误"""
    return make_response(jsonify({'error':'sorry Resources not found'}))


class TaskListAPI(Resource):
    def __init__(self):
        """处理数据验证,可以设置参数的类型,是否为必要参数,默认值等
        参数“标题”是必须的,定义一个缺少“标题”的错误信息。当客户端缺少这个参数的时候，
        Flask-RESTful 将会把这个错误信息作为响应发送给客户端。“描述”字段是可选的，当缺少这个字段的时候，默认的空字符串将会被使用
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',type = str,required = True,
                                   help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description',type = str,default = '',location = 'json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return jsonify({'tasks': list(map(make_public_task, tasks))})

    def post(self):
        args = self.reqparse.parse_args()
        title = args.get('title')
        description = args.get('description')
        done = args.get('done',False)
        id = tasks[-1]['id'] + 1
        tasks.append({'id':id,'title':title,'description':description,'done':done})
        return jsonify({'code':0,'task':make_public_task(tasks[-1])})


class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',type = str,location = 'json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = list(filter(lambda t: t['id'] == int(id), tasks))
        if len(task) == 0:
            if is_abort:
                abort(404)
            else:
                return jsonify({'code': -1, 'msg': 'task is not exits'})
        return {'code': 0, 'tasks': make_public_task(task[0])}

    def put(self, id):
        task = list(filter(lambda t: t['id'] == int(id), tasks))
        if len(task) == 0:
            if is_abort:
                abort(404)
        args = self.reqparse.parse_args()
        task[0]['title'] = args.get('title', task[0]['title'])
        task[0]['description'] = args.get('description', task[0]['description'])
        task[0]['done'] = args.get('done', task[0]['done'])

        return {'code': 0, 'task': make_public_task(task[0])}


    def delete(self, id):
        task = list(filter(lambda t: t['id'] == int(id), tasks))
        if len(task) == 0:
            if is_abort:
                abort(404)
            else:
                return {'code': -1, 'msg': 'task is not exits'}
        tasks.remove(task[0])
        return {'code': 0, 'task': make_public_task(task[0])}

api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint = 'tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint = 'task')


if __name__ == '__main__':
    app.run("0.0.0.0",8088,debug=True)
