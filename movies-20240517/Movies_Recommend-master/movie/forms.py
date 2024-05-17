from django import forms
# from django.forms  import ModelForm
from movie.models import User, Movie_rating, UserType
import numpy as np

class UserInfoForm(forms.ModelForm):
    '''用户信息用的表单'''
    name = forms.CharField(max_length=128, required=False)
    age = forms.IntegerField(required=False)
    sex = forms.IntegerField()
    married = forms.IntegerField()
    work = forms.IntegerField()
    type = forms.IntegerField()
    address = forms.IntegerField()
    def clean(self):
        cleaned_data = super(UserInfoForm, self).clean()
        name = cleaned_data.get('name')
        age = cleaned_data.get('age')
        if name is None:
            raise forms.ValidationError(message='Login expired please login again！')
        if age is None:
            raise forms.ValidationError(message='Age cannot be null！')
        return cleaned_data
    # 向量化做预测
    def get_value_list(self):
        cleaned_data = super(UserInfoForm, self).clean()
        age = cleaned_data.get('age')
        sex = cleaned_data.get('sex')
        married = cleaned_data.get('married')
        work = cleaned_data.get('work')
        type = cleaned_data.get('type')
        address = cleaned_data.get('address')
        return np.array([age, sex, address, work,married, type]).reshape(1,6)
    def get_errors(self):
        errors = self.errors.get_json_data()
        errors_lst = []
        for messages in errors.values():
            for message_dict in messages:
                for key, message in message_dict.items():
                    if key == 'message':
                        errors_lst.append(message)
        return errors_lst
    class Meta:
        model = UserType
        fields = ['name','type']


class RegisterForm(forms.ModelForm):
    '''注册用的表单'''
    password_repeat = forms.CharField(max_length=256)

    def get_errors(self):
        errors = self.errors.get_json_data()
        errors_lst = []
        for messages in errors.values():
            for message_dict in messages:
                for key, message in message_dict.items():
                    if key == 'message':
                        errors_lst.append(message)
        return errors_lst

    # 普通验证之后的最后一层验证
    # 验证密码
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        pwd = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        if pwd != password_repeat:
            raise forms.ValidationError(message='The two passwords you typed do not match！')
        return cleaned_data

    class Meta:
        model = User
        fields = ['name', 'password', 'email']


class LoginForm(forms.ModelForm):
    '''
    用于登录的表单
    '''
    name = forms.CharField(max_length=128)
    remember = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['password']

    def get_errors(self):
        errors = self.errors.get_json_data()
        errors_lst = []
        for messages in errors.values():
            for message_dict in messages:
                for key, message in message_dict.items():
                    if key == 'message':
                        errors_lst.append(message)
        return errors_lst


class CommentForm(forms.ModelForm):
    # 表单验证通过后再验证分数是否为0
    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        score = cleaned_data.get('score')
        if score == 0:
            raise forms.ValidationError(message='Ratings cannot be empty!')
        else:
            return cleaned_data

    class Meta:
        # 电影评分，只记录评分和评论
        model = Movie_rating
        fields = ['score', 'comment']

