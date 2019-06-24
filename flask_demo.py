import json
from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse

application  = Flask(__name__)
api = Api(application)

class JrWsgiServer():

    def http_exception(self, e):

        import traceback
        traceback.print_exc()

        if isinstance(e, TypeError) :
            return jsonify({"status": 400, "error": '不符合要求的参数错误'})

        if isinstance(e, AssertionError):
            return jsonify({"status": 400, "error": e.args[0]})

        return jsonify({"status": 500, "error": "Internal Server Error"})

    def http_ok(self, resp):
        return jsonify({"status": 200, "result": resp})

class TaskListAPI(Resource,JrWsgiServer):

    def get(self):
        try:
            data = {}
            # assert data,'数据不能为空'
            # name = data["name"]
            # c = 11 + "jockfi"
            resp = ["人生苦短 我用Python", ]
        except Exception as e:
            return self.http_exception( e )


        return  self.http_ok(resp)
            
    

api.add_resource(TaskListAPI, '/index', endpoint = 'tasks')



if __name__ == '__main__':
    application.run("0.0.0.0",8088,debug=True)
