# Create your views here.
from django.http import HttpResponse
from django.views import generic
from ...apps.activity.models import Activity
from django.core.urlresolvers import reverse_lazy



class ListActivity(generic.ListView):

    model = Activity
    context_object_name = 'activity_list'
    template_name = 'list-activity.html'


class DetailActivity(generic.DetailView):

    model = Activity
    context_object_name = 'object_activity'
    template_name = 'detail-activity.html'

class CreateActivity(generic.CreateView):
    model = Activity
    success_url = reverse_lazy('list-activity')
    template_name = 'update-activity.html'

class UpdateActivity(generic.UpdateView):
    model = Activity
    success_url = reverse_lazy('list-activity')
    template_name = 'update-activity.html'


class DeleteActivity(generic.DeleteView):
    model = Activity
    template_name = 'user_confirm_delete.html'