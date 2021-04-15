flaskwtf文档
https://flask-wtf.readthedocs.io/en/stable/#
wtform文档
https://wtforms.readthedocs.io/en/2.3.x/

Flask-WTF集成了WTForm功能，是带有csrf令牌的安全表单且具有全局csrf保护的功能、有文件上传(Flask-Uploads)及图形验证码功能。

安装，会自动安装WTForms：
pip install Flask-WTF

定义form.py,添加
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired, Length

# 定义表单项匹配到前端的表单中，继承FlaskForm
class UserForm(FlaskForm):
    # StringField表示前端的文本框 type=text name=name DataRequired表示必填
    name = StringField('name', validators=[DataRequired(), Length(min=6, max=12, message='用户名长度必须在6～12位之间')])
    # 密码框
    password = PasswordField('password',validators=[DataRequired(), Length(min=6, max=12, message='密码长度必须在6～12位之间')])

Field类型:
StringField PasswordField IntegerField DecimalField FloatField BooleanField RadioField SelectField DatetimeField
所有验证：
DataRequired EqualTo IPAddress Length NumberRange URL Email Regexp

# 在app.py中连接表单对象和html
from flask import Flask, render_template
from form import UserForm

app = Flask(__name__)
# 全局使用csrf保护
# 必须配置密钥 flaskform的csrf需要
app.config['SECRET_KEY'] = 'jfkdk73434kjfk3'
app.config['ENV'] = 'development'

@app.route('/')
def hello_world():
    # 创建表单类对象
    uform = UserForm()
    return render_template('user.html', uform = uform)

if __name__ == '__main__':
    app.run(debug=True)


# 在templates中建立网页user.html，form标签和提交按钮需要自己写
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>用户页面</title>
</head>
<body>
<form action="{{ url_for('hello_world') }}" method="post" enctype="multipart/form-data">
    {{ uform.csrf_token }}
    <p>{{ uform.name.label }}:{{ uform.name }}
        <span>{% if uform.name.errors %}{{ uform.name.errors.0 }} {% endif %}</span>
    </p>
    <p><input type="submit" value="提交"></p>
</form>
</body>
</html>


CSRF中文名称：跨站请求伪造，缩写为：CSRF/XSRF。
可以这么理解CSRF攻击：
攻击者盗用了受害者的身份，以受害者的名义发送恶意请求。
要完成一次CSRF攻击，受害者必须依次完成两个步骤：
登录受信任网站A，并在本地生成Cookie。在不登出A的情况下，访问危险网站B。此时B就可以携带在A处产生的cookie访问A
CSRF的防御可以从服务端和客户端两方面着手，防御效果是从服务端着手效果比较好，现在一般的CSRF防御也都在服务端进行。
{{ uform.csrf_token }}表示表单随机产生一个值，每次请求都不同。浏览器验证cookie和随机值，都正确才通过。

若想让所有的post提交均有这个功能，
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

python app.py runserver


文件上传：
定义form
class UserForm(FlaskForm):
    # 上传使用的是FileField，如果需要指定上传文件的类型需要使用：FileAllowed
    icon = FileField(label='用户头像', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], message='必须是图片文件格式')])
必须在form上面添加：enctype="multipart/form-data"
视图函数中如果验证成功，通过：
icon = uform.icon.data   -----》icon是FileStorage类型
filename = secure_filename(icon.filename)
icon.save(os.path.join(UPLOAD_DIR, filename))


# 图形验证码
pip install pillow

# bootstrap
{% extends 'bootstrap/base.html' %}
{# 为了和form匹配使用，需要导入 #}
{% import 'bootstrap/wtf.html'  as wtf %}