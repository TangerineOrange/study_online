from captcha.fields import CaptchaField
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=1)
    password = forms.CharField(required=True, min_length=2)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    # username = forms.CharField(required=True, min_length=1)
    password = forms.CharField(required=True, min_length=2)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})
