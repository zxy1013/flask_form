import os
from io import BytesIO
from flask import Flask, render_template, make_response, session
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from form import UserForm
from flask_wtf.csrf import CSRFProtect
from util import generate_image

# 路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 项目路径
STATIC_DIR = os.path.join(BASE_DIR, 'static') # 静态文件路径
UPLOAD_DIR = os.path.join(STATIC_DIR, 'upload') # 上传文件路径


app = Flask(__name__)
# 必须配置密钥 flaskform的csrf需要
app.config['SECRET_KEY'] = 'jfkdk73434kjfk3'
app.config['ENV'] = 'development'
# 验证码的公钥
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
# 验证码的私钥
app.config['RECAPTCHA_PRIVATE_KEY	'] = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
app.config['RECAPTCHA_PARAMETERS'] = {'hl': 'zh', 'render': 'explicit'}
# 验证码主题为黑色
app.config['RECAPTCHA_DATA_ATTRS'] = {'theme': 'dark'}
# 初始化bootstrap
bootstrap = Bootstrap(app=app)
csrf = CSRFProtect(app)


@app.route('/', methods=["GET","POST"])
def hello_world():
    # 创建表单类对象
    uform = UserForm()
    if uform.validate_on_submit( ): # 主要通过其进行校验 校验提交方式以及form的验证
        name = uform.name.data
        password = uform.password.data
        phone = uform.phone.data
        print('name:',name,' password:',password,' phone:',phone)
        icon = uform.icon.data # FileStorage类型
        print(type(icon))
        # 构建安全文件名 存入
        filename = secure_filename(icon.filename)
        icon.save(os.path.join(UPLOAD_DIR, filename))
        return '提交成功！'
    return render_template('user.html', uform = uform)


@app.route('/image')
def get_image():
    im, code = generate_image(4)
    # 将image对象转成二进制
    buffer = BytesIO()
    # 将图片保存到buffer format=JPEG
    im.save(buffer, "JPEG")
    # getvalue:Retrieve the entire contents of the BytesIO object
    buf_bytes = buffer.getvalue()
    # 保存到session中
    session['valid'] = code
    # 构建response对象 存二进制
    response = make_response(buf_bytes)
    response.headers['Content-Type'] = 'image/jpg'
    return response

# form与bootstrap结合使用
@app.route('/user1',methods=['GET', 'POST'])
def boot_form_user():
    uform = UserForm()
    if uform.validate_on_submit( ):  # 主要通过其进行校验 校验提交方式以及form的验证
        name = uform.name.data
        password = uform.password.data
        phone = uform.phone.data
        print('name:', name, ' password:', password, ' phone:', phone)
        icon = uform.icon.data  # FileStorage类型
        print(type(icon))
        # 构建安全文件名 存入
        filename = secure_filename(icon.filename)
        icon.save(os.path.join(UPLOAD_DIR, filename))
        return '提交成功！'
    return render_template('user1.html',uform=uform)


if __name__ == '__main__':
    app.run(debug=True)
