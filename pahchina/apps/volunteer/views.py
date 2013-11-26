#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create your views here.


# Create your views here.
from django.views import generic
from ...apps.volunteer.models import Volunteer
from django.core.urlresolvers import reverse_lazy, reverse
from ..utils import SuperUser
from .forms import VolunteerForm



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
    success_url = reverse_lazy('admin-list-volunteer')
    template_name = 'update-volunteer-admin.html'

class UpdateVolunteer(generic.UpdateView, SuperUser):
    model = Volunteer
    template_name = 'update-volunteer-admin.html'

    def get_success_url(self):
        return reverse('admin-detail-volunteer', kwargs=self.kwargs)


class DeleteVolunteer(generic.DeleteView, SuperUser):
    model = Volunteer
    success_url = reverse_lazy('admin-list-volunteer')
    template_name = 'user_confirm_delete.html'

class ShowVolunteer(generic.DetailView):
    model = Volunteer
    context_object_name = 'object_volunteer'
    template_name = 'show-volunteer.html'

class VolunteerPro(generic.UpdateView):

    model = Volunteer
    context_object_name = 'object_volunteer'
    form_class = VolunteerForm
    template_name = 'update-volunteer.html'

    def get_success_url(self):
        return reverse('show-volunteer',kwargs=self.kwargs)