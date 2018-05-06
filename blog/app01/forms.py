from django.forms import fields
from django.forms import widgets
from django.forms import Form
from django.forms import ValidationError


class RegisterForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    avatar = fields.FileField(widget=widgets.FileInput(attrs={'id': "imgSelect", 'class': "f1"}))
    code = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, request,*args, **kwargs): # 通过构造方法将request传入
        super(RegisterForm, self).__init__(*args, **kwargs) # 调用父类中的构造方法
        self.request = request

    def clean_code(self):   # 通过内置的钩子对字段进行扩展，对验证码进行匹配
        input_code = self.cleaned_data['code']  # 从表单字典中获得该字段的值
        session_code = self.request.session.get('code') # 获得session中的验证码，采用code不会报错，
        print(input_code, session_code)
        if input_code == session_code:
            return input_code   # 重新将字段的值返回给cleaned_data
        raise ValidationError('验证码错误')  # 匹配失败，将错误信息传入验证码字段对应的错误列表中

    def clean(self):    # 通过内置的钩子对表单中的多个字段进行扩展，对两次输入的密码进行验证
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 == p2:
            return None     # 返回值，不进行任何操作
        # self.add_error(None,ValidationError('密码不一致'))     # key可以为空,会将错误信息传入公共错误列表中，而非字段对应的错误列表中
        self.add_error('password2', ValidationError('密码不一致'))   # 将错误信息传入给password2字段对应的错误列表中
