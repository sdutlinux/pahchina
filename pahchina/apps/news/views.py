# Create your views here.
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from .models import News, Sorts
from .forms import NewsForm
from ..utils.views import SuperRequiredMixin

class ListNews(SuperRequiredMixin, generic.ListView):

    model = News
    context_object_name = 'news_list'
    template_name = 'list-news-admin.html'


class DetailNews(SuperRequiredMixin, generic.DetailView):

    model = News
    context_object_name = 'object_news'
    template_name = 'detail-news-admin.html'



class CreateNews(SuperRequiredMixin, generic.FormView):
    form_class = NewsForm
    template_name = 'update-news-admin.html'
    success_url = reverse_lazy('admin-list-news')


    def get_form_kwargs(self):
        kwargs = super(CreateNews, self).get_form_kwargs()
        kwargs['author'] = self.request.user
        print self.request.SITE
        kwargs['site'] = self.request.SITE
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CreateNews, self).form_valid(form)

class UpdateNews(SuperRequiredMixin, generic.UpdateView):
    model = News
    template_name = 'update-news-admin.html'

    def get_success_url(self):
        return reverse('admin-detail-news', kwargs=self.kwargs)

class DeleteNews(SuperRequiredMixin, generic.DeleteView):
    model = News
    success_url = reverse_lazy('admin-list-news')
    template_name = 'user_confirm_delete.html'

# class ShowNews(generic.DetailView):
#     model = News
#     context_object_name = 'object_news'
#     template_name = 'show-news.html'


class ListSorts(SuperRequiredMixin, generic.ListView):

    model = Sorts
    context_object_name = 'sorts_list'
    template_name = 'list-sorts-admin.html'


class DetailSorts(SuperRequiredMixin, generic.DetailView):

    model = Sorts
    context_object_name = 'object_sorts'
    template_name = 'detail-sorts-admin.html'


class CreateSorts(SuperRequiredMixin, generic.CreateView):
    model = Sorts
    success_url = reverse_lazy('admin-list-sorts')
    template_name = 'update-sorts-admin.html'

class UpdateSorts(SuperRequiredMixin, generic.UpdateView):
    model = Sorts
    #form_class = SortsForm
    #success_url = reverse_lazy('admin-list-sorts')
    template_name = 'update-sorts-admin.html'
    def get_success_url(self):
        return reverse('admin-detail-sorts',kwargs=self.kwargs)


class DeleteSorts(SuperRequiredMixin, generic.DeleteView):
    model = Sorts
    success_url = reverse_lazy('admin-list-sorts')
    template_name = 'user_confirm_delete.html'

