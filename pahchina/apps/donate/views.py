# Create your views here.
# Create your views here.
from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from ...apps.donate.models import Donate, Itemized
from ..utils.views import SuperRequiredMixin
from .form import DonateFormUser, ItemizedForm
from ...apps.accounts.models import User



class ListDonate(SuperRequiredMixin, generic.ListView):

    model = Donate
    context_object_name = 'donate_list'
    template_name = 'list-donate-admin.html'




class DetailDonate(SuperRequiredMixin, generic.DetailView):

    model = Donate
    context_object_name = 'object_donate'
    template_name = 'detail-donate-admin.html'

    def get_context_data(self, **kwargs):
        context = super(DetailDonate, self).get_context_data( **kwargs)
        donate = Donate.objects.get(id=self.kwargs['pk'])
        context['itemized_list'] = Itemized.objects.filter(number=donate)
        return context



class CreateDonate(SuperRequiredMixin, generic.CreateView):
    model = Donate
    success_url = reverse_lazy('admin-list-donate')
    template_name = 'update-donate-admin.html'


class UpdateDonate(SuperRequiredMixin, generic.UpdateView):

    model = Donate
    template_name = 'update-donate-admin.html'
    def get_success_url(self):
        return reverse('admin-detail-donate',kwargs=self.kwargs)


class DeleteDonate(SuperRequiredMixin, generic.DeleteView):
    model = Donate
    success_url = reverse_lazy('admin-list-donate')
    template_name = 'user_confirm_delete.html'


class CreateDonateUser(generic.FormView):

    form_class = DonateFormUser
    template_name = 'create-donate.html'
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(CreateDonateUser, self).get_form_kwargs()
        if self.request.user.is_authenticated():
            kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CreateDonateUser, self).form_valid(form)

class ListDonateUser(generic.DetailView):
    model = User
    template_name = 'list-donate.html'

    def get_context_data(self, **kwargs):
        context = super(ListDonateUser, self).get_context_data( **kwargs)
        context['donate_list'] = Donate.objects.filter(user=self.request.user).order_by('-create_time')
        return  context

    def get_object(self, queryset=None):
        return self.request.user

class DetailDonateUser(generic.DetailView):
    model = Donate
    context_object_name = 'object_donate'
    template_name = 'detail-donate.html'



class ListItemizedId(SuperRequiredMixin, generic.DetailView):

    model = Donate
    template_name = 'list-itemized-admin.html'

    def get_context_data(self, **kwargs):
        context = super(ListItemizedId, self).get_context_data( **kwargs)
        donate = Donate.objects.get(id=self.kwargs['pk'])
        context['itemized_list'] = Itemized.objects.filter(number=donate)
        return context



class ListItemized(SuperRequiredMixin, generic.ListView):
    model = Itemized
    context_object_name = 'itemized_list'
    template_name = 'list-itemized-admin.html'



class DetailItemized(SuperRequiredMixin, generic.DetailView):

    model = Itemized
    context_object_name = 'object_itemized'
    template_name = 'detail-itemized-admin.html'


# class CreateItemizedId(SuperRequiredMixin, generic.CreateView):
class CreateItemizedId(generic.CreateView):
    model = Itemized
    form_class = ItemizedForm
    # success_url = reverse_lazy('admin-list-itemized')
    template_name = 'update-itemized-admin.html'

    def get_success_url(self):
        return reverse_lazy('admin-list-itemized')

    def get_form_kwargs(self):
        kwargs = super(CreateItemizedId, self).get_form_kwargs()
        kwargs['donate'] = Donate.objects.get(id = self.kwargs["pk"])
        return kwargs

class UpdateItemized(SuperRequiredMixin, generic.UpdateView):
    model = Itemized
    #form_class = ItemizedForm
    #success_url = reverse_lazy('admin-list-itemized')
    template_name = 'update-itemized-admin.html'
    def get_success_url(self):
        return reverse('admin-detail-itemized',kwargs=self.kwargs)


class DeleteItemized(SuperRequiredMixin, generic.DeleteView):
    model = Itemized
    success_url = reverse_lazy('admin-list-itemized')
    template_name = 'user_confirm_delete.html'