#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import get_list_or_404, get_object_or_404

class GetOr404View(object):
    """ 在Generic View 中使用 get_object_or_404
    """
    model = None
    kwargs = None

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.kwargs['pk'])

    def get_queryset(self):

        return get_list_or_404(self.model)

class SuperRequiredMixin(object):
    """ 基类
    用于管理员页面权限控制, 只能管理员进行访问
    Usage: class SimpleView(SuperUser): ...
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect_to_login(request.get_full_path(),
                                     reverse_lazy('login'),
                                     REDIRECT_FIELD_NAME,)
        return super(SuperRequiredMixin, self).dispatch(request, *args, **kwargs)


class StaffRequiredMixin(object):
    """ 基类
    用于管理员页面权限控制, 只能管理员进行访问
    Usage: class SimpleView(SuperUser): ...
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect_to_login(request.get_full_path(),
                                     reverse_lazy('login'),
                                     REDIRECT_FIELD_NAME,)
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

class LoginRequiredMixin(View):
    """ 基类
    用于管理员页面权限控制, 只能管理员进行访问
    Usage: class SimpleView(SuperUser): ...
    """
    pass
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_active:
    #         return redirect_to_login(request.get_full_path(),
    #                                  reverse_lazy('login'),
    #                                  REDIRECT_FIELD_NAME,)
    #     return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class SuperUser(View):
    """ 基类
    用于管理员页面权限控制, 只能管理员进行访问
    Usage: class SimpleView(SuperUser): ...
    """
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(SuperUser, self).dispatch(*args, **kwargs)


#class CurrentUser(View):
#
#    def dispatch(self, *args, **kwargs):
#        return super(CurrentUser, self).dispatch(*args, **kwargs)