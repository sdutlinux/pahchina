#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.views import generic
from django.views.generic.edit import ModelFormMixin
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
from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelform_factory

from ..utils import SuperRequiredMixin, create_operate_log
from ..patient.models import Patient
from ..medical.models import Doctor, Hospital
from ..volunteer.models import Volunteer
from ..accounts.models import User
from ..accounts import forms as account_form


class GenericOperateMixin(ModelFormMixin):
    """ 通用CRUD Mixin
    方便进行常规操作，推荐使用默认配置
    需定制内容请重写方法， 比如，更新内容时候使用特定的form，
    需要制定` form_class`或者重写`get_form_class`方法
    """
    kwargs = {}
    operate = ''
    object = None
    # 禁止使用本方法的model
    forbid_models = ('group', 'site', 'redirect', 'session')

    #def operate_name(self, operate):
    #    name_dict = {'create':'添加', 'update':'修改',
    #                 'delete':'删除', 'detail':'查看'}
    #    return name_dict[operate]


    def get_model(self):
        _model = self.kwargs['model']
        if _model not in self.forbid_models:
            return get_object_or_404(ContentType, model=_model).model_class()
        else:
            raise Http404

    def get_object(self, queryset=None):
        self.model = self.get_model()
        return get_object_or_404(self.model, id=self.kwargs['pk'])

    def get_queryset(self):
        self.model = self.get_model()
        return super(GenericOperateMixin, self).get_queryset()

    def get_context_data(self, **kwargs):
        """
        传入template的变量， verbose_name为model名
        operate为操作名称
        """
        context = super(GenericOperateMixin, self).get_context_data(**kwargs)
        context.update({
            'verbose_name': self.get_model()._meta.verbose_name,
            'operate': self.operate
        })
        return context


class Update(SuperRequiredMixin, GenericOperateMixin, generic.UpdateView):
    """ 修改对象，默认使用ModelForm
    """
    template_name = 'admin-update.html'
    operate = '修改'

    _form_dict = {
        'user': account_form.UpdateUserForm,
    }

    def get_success_url(self):
        self.kwargs.pop('pk')
        return reverse('admin-list', kwargs=self.kwargs)

    def get_form_class(self):

        try:
            return self._form_dict[self.kwargs['model']]
        except KeyError:
            return super(Update, self).get_form_class()


class Create(SuperRequiredMixin, GenericOperateMixin, generic.CreateView):
    """ 创建对象
    默认使用ModelForm
    """
    template_name = 'admin-update.html'
    operate = '添加'

    def get_success_url(self):
        return reverse('admin-list', kwargs=self.kwargs)

    def get_form_class(self):
        if self.kwargs['model'] == 'user':
            return account_form.RegisterForm
        else:
            return super(Create, self).get_form_class()

class List(SuperRequiredMixin, GenericOperateMixin, generic.ListView):
    """
    template使用默认路径，即： `app_name/<model_name>_list.html`, 可通过
    自定义方法：`get_template_names`重新设置。
    内容列表变量名默认为： object_list, 可通过重写方法`get_context_object_name`重新设置
    """
    operate = '全部'


class Detail(SuperRequiredMixin, GenericOperateMixin, generic.DetailView):

    operate = '查看'



class Delete(SuperRequiredMixin, GenericOperateMixin, generic.DeleteView):
    """
    默认删除操作方法
    """
    template_name = 'confirm_delete.html'
    operate = '删除'

    # id为1的下面model不允许被删除
    admin_protect = ('user', 'website')

    def get_success_url(self):
        """ 获取删除成功后跳转的地址
        """
        if self.kwargs['model'] == 'record':
            return reverse('admin-list', kwargs={'model':'patient'})
        self.kwargs.pop('pk')
        return reverse('admin-list', kwargs=self.kwargs)

    def check_permit(self):
        """ 检查对象是否允许被删除
        """
        _model, pk = self.kwargs['model'], self.kwargs['pk']
        if pk == '1' and _model in self.admin_protect:
            messages.error(self.request,
                           message='该对象不能被删除！')
            return True
        else:
            return False

    # 检查，重定向
    def get(self, request, *args, **kwargs):
        if self.check_permit():
            return HttpResponseRedirect(reverse('admin-list',
                                                kwargs={'model': self.kwargs['model']}))
        return super(Delete, self).get(self, request, *args, **kwargs)

    def post(self, *args, **kwargs):
        if self.check_permit():
            return HttpResponseRedirect(reverse('admin-list', kwargs={'model': self.kwargs['model']}))
        return super(Delete, self).post(*args, **kwargs)
