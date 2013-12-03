# Create your views here.
from django.views import generic
from ...apps.activity.models import Activity
from django.core.urlresolvers import reverse_lazy, reverse
from ..utils.views import SuperRequiredMixin
from .forms import ActivityForm



class ListActivity(SuperRequiredMixin, generic.ListView):

    model = Activity
    context_object_name = 'activity_list'
    template_name = 'list-activity-admin.html'


class DetailActivity(SuperRequiredMixin, generic.DetailView):

    model = Activity
    context_object_name = 'object_activity'
    template_name = 'detail-activity-admin.html'

    #def get_object(self):
    def get_object(self, queryset=None):
        object = super(DetailActivity, self).get_object()
        object.pageview += 1
        object.save()
        return object

class ShowActivity(generic.DetailView):

    model = Activity
    context_object_name = 'object_activity'
    template_name = 'show-activity.html'

class CreateActivity(SuperRequiredMixin, generic.CreateView):
    model = Activity
    success_url = reverse_lazy('admin-list-activity')
    template_name = 'update-activity-admin.html'

class UpdateActivity(SuperRequiredMixin, generic.UpdateView):
    model = Activity
    #form_class = ActivityForm
    #success_url = reverse_lazy('admin-list-activity')
    template_name = 'update-activity-admin.html'
    def get_success_url(self):
        return reverse('admin-detail-activity',kwargs=self.kwargs)


class DeleteActivity(SuperRequiredMixin, generic.DeleteView):
    model = Activity
    success_url = reverse_lazy('admin-list-activity')
    template_name = 'user_confirm_delete.html'
