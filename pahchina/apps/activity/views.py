# Create your views here.
from django.views import generic
from ...apps.activity.models import Activity
from django.core.urlresolvers import reverse_lazy
from ..utils import SuperUser



class ListActivity(generic.ListView, SuperUser):

    model = Activity
    context_object_name = 'activity_list'
    template_name = 'list-activity-admin.html'


class DetailActivity(generic.DetailView, SuperUser):

    model = Activity
    context_object_name = 'object_activity'
    template_name = 'detail-activity-admin.html'

    #def get_object(self):
    def get_object(self, queryset=None):
        object = super(DetailActivity, self).get_object()
        object.pageview += 1
        object.save()
        return object

class ShowActivity(generic.DetailView, SuperUser):

    model = Activity
    context_object_name = 'object_activity'
    template_name = 'show-activity.html'

class CreateActivity(generic.CreateView, SuperUser):
    model = Activity
    success_url = reverse_lazy('list-activity')
    template_name = 'update-activity-admin.html'

class UpdateActivity(generic.UpdateView, SuperUser):
    model = Activity
    success_url = reverse_lazy('list-activity')
    template_name = 'update-activity-admin.html'


class DeleteActivity(generic.DeleteView, SuperUser):
    model = Activity
    success_url = reverse_lazy('list-activity')
    template_name = 'user_confirm_delete.html'
