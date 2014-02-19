#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response as r2r, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import Permission, PermissionManager, PermissionsMixin


from ..utils import  SuperRequiredMixin
from ..patient.models import Patient
from ..medical.models import Doctor, Hospital
from ..volunteer.models import Volunteer

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
                messages.success(request, '注册成功, 请登录！')
                return HttpResponseRedirect(reverse('login'))

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
                messages.success(request, '登录成功，欢迎您：{0}'.format(request.user.username))
                redirect_to = request.REQUEST.get('next', False)
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                else:
                    if user.is_superuser or user.is_staff:
                        return HttpResponseRedirect(reverse('admin-index'))
                    else:
                        return HttpResponseRedirect(reverse_lazy('profile'))
            else:
                messages.error(request, '用户暂停使用，请联系管理员！')
        else:
            messages.error(request, '用户名与密码不匹配！')

    form = AuthenticationForm
    return r2r('login.html', locals(), context_instance = RequestContext(request))

def pah_logout(request):
    """ 网站登出
    """
    logout(request)
    messages.info(request, '成功注销本次登录！')
    return HttpResponseRedirect(reverse('login'))

class Profile(generic.DetailView):
    """ 用户个人主页
    """

    def get_object(self, queryset=None):
        request_user = self.request.user
        if request_user.is_patient:
            self.object = request_user.patient
            self.template_name = 'profile-patient.html'
            self.context_object_name = 'patient'
        elif request_user.is_hospital:
            self.object = request_user.hospital
            self.template_name = 'profile-hospital.html'
            self.context_object_name = 'hospital'
        elif request_user.is_doctor:
            self.object = request_user.doctor
            self.template_name = 'profile-doctor.html'
            self.context_object_name = 'doctor'
        elif request_user.is_superuser:
            self.template_name = 'index.html'
            return HttpResponseRedirect(reverse_lazy('index'))
        return self.object

class Show(generic.DetailView):
    """ 用户个人展示页面
    """

    model = User

    def get_object(self, queryset=None):
        super_object = super(Show, self).get_object()
        if super_object.is_patient:
            self.context_object_name = 'patient'
            self.template_name = 'show-patient.html'
            return super_object.patient
        elif super_object.is_hospital:
            self.context_object_name = 'hospital'
            self.template_name = 'show-hospital.html'
            return super_object.hospital
        elif super_object.is_doctor:
            self.context_object_name = 'doctor'
            self.template_name = 'show-doctor.html'
            return super_object.doctor
        else:
            self.template_name = 'index.html'
            return HttpResponseRedirect(reverse_lazy('index'))



@user_passes_test(lambda u: u.is_staff)
def admin_index(request):
    """ 网站后台首页
    """
    return r2r('admin-index.html', locals(),
               context_instance=RequestContext(request))

class ListUser(SuperRequiredMixin, generic.ListView):
    """ 管理员列出所有用户
    """
    model = User
    context_object_name = 'user_list'
    template_name = 'list-user.html'


class DetailUser(SuperRequiredMixin, generic.DetailView):
    """ 管理员查看用户详情
    """
    model = User
    context_object_name = 'object_user'
    template_name = 'detail-user.html'

class CreateUser(SuperRequiredMixin, generic.CreateView):
    """ 管理员创建用户
    """
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('admin-list-user')
    template_name = 'update-user.html'

class UpdateUser(SuperRequiredMixin, generic.UpdateView):
    """ 管理员更新用户详情
    """
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('admin-list-user')
    template_name = 'update-user.html'

    #def get_success_url(self):
    #    if self.get_object().is_doctor:
    #        return reverse('admin-detail-doctor')


class DeleteUser(SuperRequiredMixin, generic.DeleteView):
    """ 管理员删除用户
    """
    model = User
    success_url = reverse_lazy('admin-list-user')
    template_name = 'user_confirm_delete.html'


class UpdateProfile(generic.UpdateView):
    """ 用户修改个人信息
    """
    form_class = UpdateProfileForm
    template_name = 'update-user-profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.user.get_profile_url()

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


class ListUserGroup(generic.ListView, SuperRequiredMixin):
    """ 管理员查看所有用户组
    """

    model = Group
    template_name = 'list-group.html'
    context_object_name = 'group_list'

class CreateUserGroup(generic.CreateView, SuperRequiredMixin):
    """ 管理员创建用户组
    """
    model = Group
    template_name = 'update.html'
    success_url = '/'

    #def get_object(self, queryset=None):
    #    if self.kwargs['']

class UpdateUserGroup(generic.UpdateView, SuperRequiredMixin):
    """ 管理员修改用户组
    """
    model = Group
    template_name = 'update.html'
    success_url = ''

class DeleteUserGroup(generic.DeleteView, SuperRequiredMixin):

    """ 管理员删除用户组
    """
    model = Group
    template_name = 'confirm_delete.html'
    success_url = '/'


#class PermManage(SuperRequiredMixin, generic.DetailView):

