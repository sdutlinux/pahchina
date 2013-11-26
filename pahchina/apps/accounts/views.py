#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response as r2r
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

from ..utils import SuperUser

from .models import User
from .froms import (RegisterForm,
    UpdateUserForm, UpdateProfileForm, )#PasswordResetForm)



def pah_register(request):

    form = RegisterForm
    if request.method == "POST":
            form = RegisterForm(request.POST.copy())
            if form.is_valid():
                form.save()
                return HttpResponse('<script>alert("注册成功！");top.location="/"</script>')

    return r2r('register.html', locals(), context_instance=RequestContext(request))

def pah_login(request):
    """ 网站登录
    根据不同身份用户跳转到不同的页面
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect(reverse('admin-index'))
                elif user.is_patient:
                    return HttpResponseRedirect(reverse('profile-patient'))
                else:
                    return HttpResponse('请定义页面')
            else:
                return HttpResponse('用户没有激活')
        else:
            return HttpResponse('用户名与密码不匹配')

    form = AuthenticationForm
    return r2r('login.html', locals(), context_instance = RequestContext(request))

def pah_logout(request):
    """ 网站登出
    """
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@user_passes_test(lambda u: u.is_superuser)
def admin_index(request):
    """ 网站后台首页
    """
    return r2r('admin-index.html', locals(),
               context_instance=RequestContext(request))

class ListUser(generic.ListView, SuperUser):
    """ 列出所有用户
    """
    model = User
    context_object_name = 'user_list'
    template_name = 'list-user.html'


class DetailUser(generic.DetailView, SuperUser):
    """ 查看用户详情
    """
    model = User
    context_object_name = 'object_user'
    template_name = 'detail-user.html'

class CreateUser(generic.CreateView, SuperUser):
    """ 创建用户
    """
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('admin-list-user')
    template_name = 'update-user.html'

class UpdateUser(generic.UpdateView, SuperUser):
    """ 更新用户详情
    """
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('admin-list-user')
    template_name = 'update-user.html'


class DeleteUser(generic.DeleteView, SuperUser):
    """ 删除用户
    """
    model = User
    success_url = reverse_lazy('admin-list-user')
    template_name = 'user_confirm_delete.html'

class PasswordReset(generic.FormView):
    """ 用户通过Email重置密码
    """
    form_class = PasswordResetForm
    success_url = reverse_lazy('login')
    template_name = 'registration/password_reset_form.html'


class UpdateProfile(generic.UpdateView):
    """ 用户修改个人信息
    """
    form_class = UpdateProfileForm
    success_url = reverse_lazy('profile-patient')
    template_name = 'update-user-profile.html'

    def get_object(self, queryset=None):
        return self.request.user

