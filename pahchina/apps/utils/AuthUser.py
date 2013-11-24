#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required

class SuperUser(View):
    """ 基类
    用于管理员页面权限控制, 只能管理员进行访问
    Usage: class SimpleView(SuperUser): ...
    """
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(SuperUser, self).dispatch(*args, **kwargs)


