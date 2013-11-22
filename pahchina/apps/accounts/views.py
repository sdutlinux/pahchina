#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.core.urlresolvers import reverse_lazy

from .models import User


class ListUser(generic.ListView):

    model = User
    context_object_name = 'user_list'
    template_name = 'list-user.html'


class DetailUser(generic.DetailView):

    model = User
    context_object_name = 'object_user'
    template_name = 'detail-user.html'

class CreateUser(generic.CreateView):
    model = User
    success_url = reverse_lazy('list-user')
    template_name = 'update-user.html'

class UpdateUser(generic.UpdateView):
    model = User
    success_url = reverse_lazy('list-user')
    template_name = 'update-user.html'


class DeleteUser(generic.DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'