# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class NameForm(Form):
    name = StringField(u'请输入你的名字？', validators=[Required()])
    submit = SubmitField(u'提交')


class EditProfileForm(Form):
    """普通用户个人资料编辑表单"""
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    """管理员个人资料编辑表单"""
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名只能由字母、数字、点和下划线组成！')])
    confirmed = BooleanField(u'是否邮件验证')
    role = SelectField(u'角色', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮件已被注册！')

    def validate_username(self, field):
        if field.data != self.user.username and \
            User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被使用！')


class PostForm(Form):
    """博客文章表单"""
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField(u'提交')


class CommentForm(Form):
    """评论表单"""
    body = StringField('', validators=[Required()])
    submit = SubmitField('Submit')
