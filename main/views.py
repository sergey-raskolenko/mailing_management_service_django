from django.views.generic import TemplateView

from app_blog.models import Blog
from app_client.models import Client
from app_newsletter.models import Newsletter
from main.services import cache_object_list


class IndexTemplateView(TemplateView):
	template_name = 'main/index.html'

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['object_list'] = cache_object_list(Blog).order_by('-published_date')[:3]
		context_data['newsletter_list'] = cache_object_list(Newsletter).count()
		context_data['active_newsletter_list'] = cache_object_list(Newsletter).filter(is_active=True).count()
		context_data['unique_clients'] = cache_object_list(Client).values('email').distinct().count()
		return context_data
