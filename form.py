import re
from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


# 定义表单项匹配到前端的表单中，继承FlaskForm
class UserForm(FlaskForm):
    # field类型 'BooleanField', 'DecimalField', 'DateField', 'DateTimeField', 'FieldList', 'FloatField', 'FormField', 'IntegerField', 'RadioField', 'SelectField', 'SelectMultipleField', 'StringField', 'TimeField',
    # StringField表示前端的文本框 type=text name=name DataRequired表示必填 errors为元组
    # 限制格式 DataRequired EqualTo IPAddress Length NumberRange URL Email Regexp
    name = StringField(label='用户名', validators=[DataRequired(), Length(min=6, max=12, message='用户名长度必须在6～12位之间')])

    # 密码框
    password = PasswordField(label='密  码',validators=[DataRequired(), Length(min=6, max=12, message='密码长度必须在6～12位之间')])

    # 确认密码 EqualTo(name)
    confirm_pwd = PasswordField(label='确认密码', validators=[ DataRequired( ), Length(min=6, max=12, message='密码长度必须在6～12位之间'), EqualTo('password', '两次密码不一致') ])

    # 手机号 ctrl点击进去，点击下箭头显示其所有子类
    phone = StringField(label='手机号码', validators=[ DataRequired( ), Length(min=11, max=11, message='手机号码必须11位长度') ])

    # 头像上传 from flask_wtf.file import FileField, FileRequired, FileAllowed  FileAllowed允许上传的扩展名
    icon = FileField(label='用户头像', validators=[ FileRequired( ), FileAllowed([ 'jpg', 'png', 'gif' ], message='必须是图片文件格式') ])

    # 图形验证码 RecaptchaField 使用需要google 所以直接使用StringField
    recaptcha = StringField(label='验证码')

    # If the form defines a ``validate_<fieldname>`` method, it is appended as an extra validator for the field's ``validate``.
    # 自定义name的格式 data 就是提交过来的表单项 data.data以及 self.name.data 都为取值 2zxcgyh
    def validate_name(self, data):
        # self.name <input id="name" name="name" required type="text" value="2zxcgyh">
        if self.name.data[ 0 ].isdigit( ):
            # 抛出错误 加入元组
            raise ValidationError('用户名不能以数字开头')

    # 自定义phone的格式
    def validate_phone(self, data):
        phone = data.data
        # 正则匹配 ^1[35678]\d{9}$  开头1 第二位为3/5/6/7/8 后面9位数字
        if not re.search(r'^1[35678]\d{9}$', phone):
            raise ValidationError('手机号码格式错误')

    def validate_recaptcha(self, data):
        input_code = data.data
        code = session.get('valid')
        # 全改为小写
        if input_code.lower() != code.lower( ):
            raise ValidationError('验证码错误')
