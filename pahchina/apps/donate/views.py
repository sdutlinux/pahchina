# Create your views here.
# Create your views here.
from django.views import generic
from ...apps.donate.models import Donate
from django.core.urlresolvers import reverse_lazy, reverse
from ..utils import SuperUser
from .form import DonateFormUser



class ListDonate(generic.ListView, SuperUser):

    model = Donate
    context_object_name = 'donate_list'
    template_name = 'list-donate-admin.html'


class DetailDonate(generic.DetailView, SuperUser):

    model = Donate
    context_object_name = 'object_donate'
    template_name = 'detail-donate-admin.html'


class CreateDonate(generic.CreateView, SuperUser):
    model = Donate
    success_url = reverse_lazy('admin-list-donate')
    template_name = 'update-donate-admin.html'


class UpdateDonate(generic.UpdateView, SuperUser):

    model = Donate
    template_name = 'update-donate-admin.html'
    def get_success_url(self):
        return reverse('admin-detail-donate',kwargs=self.kwargs)


class DeleteDonate(generic.DeleteView, SuperUser):
    model = Donate
    success_url = reverse_lazy('admin-list-donate')
    template_name = 'user_confirm_delete.html'

class CreateDonateUser(generic.FormView):
    form_class = DonateFormUser
    template_name = 'update-donate-admin.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(CreateDonateUser, self).form_valid(form)