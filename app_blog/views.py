from django.views.generic import ListView, DetailView
from app_blog.models import Blog
from main.services import cache_object_list


class BlogListView(ListView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список статей'
        context_data['object_list'] = cache_object_list(Blog)
        return context_data


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.object.title
        return context_data
