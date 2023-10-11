from django.views.generic import TemplateView

from app_blog.models import Blog


class IndexTemplateView(TemplateView):
	template_name = 'main/index.html'

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['object_list'] = Blog.objects.all().order_by('-published_date')[:3]
		return context_data
