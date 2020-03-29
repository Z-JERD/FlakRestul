flask-知识点
- 配置文件
- before_request/after_request
- 路由系统
-视图
- 模板
- session
- flash
- 蓝图(blueprint)
flask-组件
- flask-session
- DBUtils
- wtforms


#安装Falsk pip install flask
#用flask写一个hello world文件
"""
from flask import Flask
app=Flask(__name__)
@app.route("/index")
def index():
    return "Hello Word"
if __name__=="__main__":
    app.run()

"""

#####################1.配置文件############################

"""
1.新建settings.py 存放配置文件
class Config(object):
    DEBUG = False
    SECRET_KEY = "asdfasdfasdf"
#上线环境
class ProductionConfig(Config):
    DEBUG = False
#开发环境
class DevelopmentConfig(Config):
    DEBUG = True
#测试环境
class TestingConfig(Config):
    TESTING = True
其他文件要引入配置文件中的内容 如：
 app.config.from_object('settings.DevelopmentConfig')
引入整个py文件：app.config.from_pyfile("settings.py")
"""


#####################2.before_request和after_request########


"""
before_request和after_request
相当于Django中的中间件
after_request的视图中必须有参数,且必须有返回值
1.before_request---->目标请求 ----->after_request
@app.before_request
def a1():
    print("a2")
@app.after_request
def c1(response):
    print("c1")
    return response
def index():
    print("index")
    return render_template("index.html")
执行顺序:a2--->index---->c1
2.在走before_request时如果返回了值,后面的before_request就不再执行,目标函数也不执行
会把after_request都走一遍
@app.before_request
def a1():
    print("a1")
@app.before_request   
def d1(response):
    print("d1")
    return response
@app.after_request
def c1(response):
    print("c1")
    return response
    return response
def index():
    print("index")
    return render_template("index.html")
执行顺序： a1--->d1--->c1


"""

#####################3.路由系统############################


"""
路由的两种注册方法：
    1.使用装饰器
        @app.route("/login")
    2. app.add_url_rule(rule='/login', view_func=index)
1.定义methods
	@app.route("/login",methods=['GET','POST'])
2.动态路由
	URL: http://www.xx.com/index/1/88
	@app.route('/index/<string:nid>/<int:num>')
    也可以 @app.route('/index/<nid>/<num>')
	  def index(a,b):pass
3.endpoint ,为url起别名，根据别名可以反向生成URL（默认endpoint是函数名）
  url_for：反向解析
  url_for()它把函数名称作为第一个参数。它可以接受任意个关键字参数，每个关键字参数对应URL中的变量
  1.自定义endpoint
  	@app.route('/user/<username>',endpoint="aaa")
	def profile(username):print(url_for('aaa',username='zhao')  /user/zhao
  2.使用默认的endpoint
	@app.route('/login')
	def login():pass
	@app.route('/user/<username>')
	def profile(username):pass
	with app.test():
		print(url_for('login')) /login
		print(url_for('login', next='/')) /login?next=/
		print(url_for('profile', username='zhao')) /user/zhao
4.支持自定义正则
@app.route('/index/<string:nid>/<int:num>/<regex("\d+"):xxxx>')
5.支持FBV和CBV
from flask import Flask,url_for,views
class IndexView(views.MethodView):
	methods = ['GET','POST']
	decorators = [auth, ]
	def get(self):
		return 'Index.GET'	
	def post(self):
		return 'Index.POST'
app.add_url_rule('/index', view_func=IndexView.as_view(name='ci')) name="ci" 指别名

"""

##########################4.视图############################

"""
from flask import request,render_template,redirect
1.请求：
	request.method 判断请求方式
	request.args 接收GET请求携带的参数数据
	request.cookies
	request.headers
	request.path   当前请求的路径
	request.full_path
	request.url
	request.files  接收文件
	obj = request.files['the_file_name']
	获取POST参数:
	    args = request.get_data()       接收值为bytes
	    args = request.get_json()       请求头发送参数为application/json格式, 才可以接收到 值为对象 
	    form_name = request.form        表单数据
2.响应：
	1.return "xxxx" 返回字符串
    2.return render_template("index.html",msg="xxx") 返回模板
      return render_template('html模板路径',**{"mag="xxx”,arg":12})
    3.return redirect() 重定向
    4.response = make_response(render_template('index.html'))
    5. response.set_cookie('key', 'value')
    6. response.delete_cookie('key')
    7.return send_file()
    def get_img(file_name):
    file_path = os.path.join(setting.RESOURCE_IMG_PATH,file_name)
    return send_file(file_path)
@app.route('/setco')
def setco():
    from flask import make_response
	obj = make_response("返回内容...")
    obj.set_cookie('a1','123')
    return obj
给视图添加装饰器：
        - 装饰器必须设置functools.wappers
        - 紧挨着放在视图之上

from functools import wraps
def is_login(func):
    @wraps(func) #保留函数元信息
    def inner(*args,**kwargs):
        user_info = session.get('user')
        if not user_info:
            return redirect('/login')
        ret=func()
        return ret
    return inner
@app.route("/book")
@is_login  #必须紧贴着函数
def book():
    return "Book"

"""


##########################5.模板############################

"""
Flask使用的是Jinja2模板，所以其语法和Django无差别
1.支持python语法
2.支持模板继承
3.自定义函数
服务端：
def jerd():
    return '<h1>jerd</h1>'
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', ww=jerd)
HTML：需要加()和safe
<body>
    {{ww()|safe}}
</body>
4.全局函数
1.global：
	@app.template_global()
	def test4(arg):
		return arg + 100
	所有视图中都可以调用：
		{{ test4(666) }}
2.filter:
	@app.template_filter()
	def db(a1, a2, a3):
		return a1 + a2 + a3
	所有视图中都可以调用：
		{{ 1|db(2,3)}}


"""

##########################6.session##########################
"""
session的本质是字典
flask的session存放在cookie中
1.导入session
from flask import session
2.设置key值：app.secret_key="xxxxx"
3.操作：
    1.设置：session["zhao"]="zgf"
    2.获取：session.get("zhao")
    3.删除：del session.["zhao"]
在客户端的cookie中能看到session和sessionid

cookie和session的区别？
    cookie，是保存在用户浏览器端的键值对，可以用来做用户认证。
    session，将用户会话信息保存在服务端{adfasdfasdf:"...",99dfsdfsdfsd:'xxx'},依赖cookie将每个用户的随机字符串保存到用户浏览器上；
    
    django，session默认保存在数据库；django_session表
    flask，session默认将加密的数据写用户cookie中。

"""

##########################7.蓝图(blueprint)##########################

"""
app---蓝图----视图
1. 目录结构的划分（解耦）。
2. 单蓝图中应用before_request
3. URL划分
	app.register_blueprint(account,url_prefix='/user')
4. 反向生成URL
	url_for('蓝图.函数名')
	url_for('蓝图.endpoint')
	url_for('蓝图.endpoint',nid=1)
	print(url_for('account.login'))
在app下注册蓝图
app=Flask(__name__)
app.register_blueprint(bpmanager)
在视图中：
from flask import Blueprint
bpmanager=Blueprint('bpmanager',__name__)
@bpmanager.route("/delete/",methods=["GET","POST"])
def delete():pass
"""


