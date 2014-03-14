#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
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
from django.utils.safestring import mark_safe

from ..utils import  SuperRequiredMixin, LoginRequiredMixin
from ..patient.models import Patient
from ..medical.models import Doctor, Hospital
from ..volunteer.models import Volunteer

from .models import User, Personal, Unit, Bank
import forms



def pah_register(request):
    """ 网站注册
    注册后同步创建其他身份
    """
    form = forms.RegisterForm
    if request.method == "POST":
            form = forms.RegisterForm(request.POST.copy())
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
                user.count_login_time() # 修改登录次数
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


#def first_login(request):
#    """ 用户第一次登录
#    """
#    if request.user.is_patient:
#



class Profile(LoginRequiredMixin, generic.DetailView):
    """ 用户个人主页
    """

    def get_template_names(self):

        return 'profile-{}.html'.format(self.request.user.get_identity_label())

    def get_context_object_name(self, obj):

        return self.request.user.get_identity_label()

    def get_object(self, queryset=None):

        return self.request.user.get_identity_model()

class UserInfoView(LoginRequiredMixin, generic.DetailView):

    #model = Personal
    #template_name = 'user-personal.html'

    _dic = {
        'personal': Personal,
        'unit': Unit,
        'bank': Bank,
    }
    def get_obj(self):
        try:
            return self._dic[self.kwargs['model']]
        except KeyError:
            raise Http404

    def get_template_names(self):

        return 'user-{}.html'.format(self.kwargs['model'])

    def get_object(self, queryset=None):
        try:
            _obj = self.get_obj().objects.get(user=self.request.user)
            return _obj
        except self.get_obj().DoesNotExist:
            messages.info(self.request, '您尚未创建该信息！')

class UpdateUserInfo(LoginRequiredMixin, generic.FormView):
    """ 修改个人信息
    包括个人信息、单位信息、银行信息
    """
    #form_class = forms.VltFirstFillForm
    template_name = 'index-update.html'

    _dic = {
        'personal': (forms.VltFirstFillForm, Personal),
        'unit': (forms.UnitForm, Unit),
        'bank': (forms.BankForm, Bank),
    }

    def get_tu(self):
        try:
            return self._dic[self.kwargs['model']]
        except KeyError:
            raise Http404

    def get_form_class(self):

        return self.get_tu()[0]

    def get_initial(self):
        try:
            obj=self.get_tu()[1].objects.get(user=self.request.user)
            return obj.__dict__.copy()
        except self.get_tu()[1].DoesNotExist:
            return {}

    def form_valid(self, form):
        form.save()
        return super(UpdateUserInfo, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, '修改成功！')
        return reverse('user-info', kwargs=self.kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdateUserInfo, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdateUserInfo, self).get_context_data(**kwargs)
        context['title']='修改信息'
        return context


class Show(generic.DetailView):
    """ 用户个人展示页面
    """

    model = User

    def get_template_names(self):

        return 'show-{}.html'.format(self.request.user.get_identity_label())

    def get_context_object_name(self, obj):

        return self.request.user.get_identity_label()

    def get_object(self, queryset=None):

        return self.request.user.get_identity_model()


class UpdateProfile(LoginRequiredMixin, generic.UpdateView):
    """ 用户修改账户信息
    """
    form_class = forms.UpdateProfileForm
    template_name = 'index-update.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, '修改成功！')
        return self.request.user.get_profile_url()

    def get_context_data(self, **kwargs):
        context = super(UpdateProfile, self).get_context_data(**kwargs)
        context['title']='修改账户信息'
        return context

@user_passes_test(lambda u: u.is_staff)
def admin_index(request):
    """ 网站后台首页
    """
    return r2r('admin-index.html', locals(),
               context_instance=RequestContext(request))




class UpdatePassword(LoginRequiredMixin, generic.FormView):
    """ 用户或管理员更新个人密码
    """

    form_class = PasswordChangeForm
    template_name = 'index-update.html'

    def get_success_url(self):
        messages.success(self.request, '修改密码成功！')
        return self.request.user.get_profile_url()

    def get_form_kwargs(self):
        kwargs = super(UpdatePassword, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdatePassword, self).get_context_data(**kwargs)
        context['title']='修改密码'
        return context

    def form_valid(self, form):
        form.save()
        return super(UpdatePassword, self).form_valid(form)


#class Create