### 参考文档：http://www.pythondoc.com/flask-restful/second.html
### ubuntu 部署Flask：https://www.jianshu.com/p/484bd73f1e80
       部署Django：https://blog.csdn.net/qq_16069927/article/details/82079259

### FlaskAPIFBV.py
#### 1.设计一个简单的Web service
    1.设定根URL来访问服务 如：http://[hostname]/todo/api/v1.0/
        在 URL 中包含应用的名称以及 API 的版本号。包含应用名称有助于提供一个命名空间以便区分同一系统上的其它服务。
        包含版本号能够帮助以后的更新
    2.显示服务暴露(展示)的资源
            HTTP 方法   URL                                              动作
        ==========  ===============================================  ==============================
        GET         http://[hostname]/todo/api/v1.0/tasks            检索任务列表
        GET         http://[hostname]/todo/api/v1.0/tasks/[task_id]  检索某个任务
        POST        http://[hostname]/todo/api/v1.0/tasks            创建新任务
        PUT         http://[hostname]/todo/api/v1.0/tasks/[task_id]  更新任务
        DELETE      http://[hostname]/todo/api/v1.0/tasks/[task_id]  删除任务
    3.将操作的数据的属性
        id: 任务的唯一标识符。数字类型。
        title: 简短的任务描述。字符串类型。
        description: 具体的任务描述。文本类型。
        done: 任务完成的状态。布尔值。
    4.使用FBV的处理方式完成请求
        @app.route('/todo/api/v1.0/tasks',methods=['GET'])
        @app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['GET'])
        @app.route('/todo/api/v1.0/tasks',methods=['post'])
        @app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['PUT'])
        @app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['DELETE'])
        请求的资源不存在返回404,返回友好的提示页面@app.errorhandler(404)
    5.不直接返回任务的ids，返回控制这些任务的完整的URI，以便客户端可以随时使用这些 URIs
        def make_public_task(task):pass
    6.加强 RESTful web service 的安全性
        要求客户端在每一次请求中提供认证的信息
        使用Flask自带的认证函数 Flask-HTTPAuth
        pip install flask-httpauth
        get_password 函数是一个回调函数，Flask-HTTPAuth 使用它来获取给定用户的密码。
        error_handler 回调函数是用于给客户端发送未授权错误代码
        需要认证的函数添加 @auth.login_required 装饰器
### FlaskAPICBV.py
        1.Flask中使用Flask-RESTful完成面向对象的API设计
            pip3 install flask-restful
        2.from flask_restful import Resource, Api
            app = Flask(__name__)
            api = Api(app)
        3.Flask-RESTful 提供了一个更好的方式来处理数据验证，它叫做 RequestParser 类
          对于每一个资源需要定义参数以及怎样验证它们
          from flask.ext.restful import reqparse
        4.添加认证：
            from flask.ext.httpauth import HTTPBasicAuth
            auth = HTTPBasicAuth()
            class TaskAPI(Resource):
                decorators = [auth.login_required]
				
###  jsonify 将数据序列化为JSON字符串
'''
from flask import Flask,request,render_template,jsonify

app=Flask(__name__)
@app.route('/index',methods=['GET','POST'])
def upload_file():
    return jsonify({'name':'jerd','sex':'man'})
if __name__ == '__main__':
    app.run()

### 返回的字符串中会多个换行符,调用接口后接受值为：'{"name":"jerd","sex":"man"}\n'
import requests
import json
URL = "http://127.0.0.1:5000/index"
headers = {
        'Content-Type': "application/json",
        'Accept-Charset': "utf-8",
    }
response = requests.request("POST", URL,  headers=headers)
data = response.text   #'{"name":"jerd","sex":"man"}\n'
json_data = json.loads(data) #{"name":"jerd","sex":"man"}
'''


