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
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from ..utils import SuperUser

from .models import User
from .froms import (RegisterForm,
    UpdateUserForm, UpdateProfileForm, UpdateUserIdentityForm)



def pah_register(request):
    """ 网站注册
    注册后同步创建其他身份
    """
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
                elif user.is_hospital:
                    return HttpResponseRedirect(reverse('profile-hospital'))
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
    """ 管理员列出所有用户
    """
    model = User
    context_object_name = 'user_list'
    template_name = 'list-user.html'


class DetailUser(generic.DetailView, SuperUser):
    """ 管理员查看用户详情
    """
    model = User
    context_object_name = 'object_user'
    template_name = 'detail-user.html'

class CreateUser(generic.CreateView, SuperUser):
    """ 管理员创建用户
    """
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('admin-list-user')
    template_name = 'update-user.html'

class UpdateUser(generic.UpdateView, SuperUser):
    """ 管理员更新用户详情
    """
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('admin-list-user')
    template_name = 'update-user.html'


class DeleteUser(generic.DeleteView, SuperUser):
    """ 管理员删除用户
    """
    model = User
    success_url = reverse_lazy('admin-list-user')
    template_name = 'user_confirm_delete.html'


class UpdateProfile(generic.UpdateView):
    """ 用户修改个人信息
    """
    form_class = UpdateProfileForm
    success_url = reverse_lazy('profile-patient')
    template_name = 'update-user-profile.html'

    def get_object(self, queryset=None):
        return self.request.user

class UpdatePassword(generic.FormView):
    """ 用户或管理员更新个人密码
    """

    form_class = PasswordChangeForm
    template_name = 'update-user-profile.html'

    def get_success_url(self):
        return self.request.user.get_profile_url()

    def get_form_kwargs(self):
        kwargs = super(UpdatePassword, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UpdatePassword, self).form_valid(form)


class UpdateIdentity(generic.FormView):

    form_class = UpdateUserIdentityForm
    template_name = 'update-user-profile.html'

    def get_success_url(self):
        return reverse('admin-detail-user', kwargs=self.kwargs)
    
    def form_valid(self, form):
        form.save()
        return super(UpdateIdentity, self).form_valid(form)    