#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create your views here.


# Create your views here.
from django.views import generic
from ...apps.volunteer.models import Volunteer
from django.core.urlresolvers import reverse_lazy
from ..utils import SuperUser



class ListVolunteer(generic.ListView, SuperUser):

    model = Volunteer
    context_object_name = 'volunteer_list'
    template_name = 'list-volunteer-admin.html'


class DetailVolunteer(generic.DetailView, SuperUser):

    model = Volunteer
    context_object_name = 'object_volunteer'
    template_name = 'detail-volunteer-admin.html'


class CreateVolunteer(generic.CreateView, SuperUser):
    model = Volunteer
    success_url = reverse_lazy('list-volunteer')
    template_name = 'update-volunteer-admin.html'

class UpdateVolunteer(generic.UpdateView, SuperUser):
    model = Volunteer
    success_url = reverse_lazy('list-volunteer')
    template_name = 'update-volunteer-admin.html'


class DeleteVolunteer(generic.DeleteView, SuperUser):
    model = Volunteer
    success_url = reverse_lazy('list-volunteer')
    template_name = 'user_confirm_delete.html'
