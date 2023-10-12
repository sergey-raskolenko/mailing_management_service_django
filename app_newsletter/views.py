from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from app_newsletter.forms import NewsletterCreateForm
from app_newsletter.models import Newsletter, NewsletterLog


class NewsletterListView(ListView):
	model = Newsletter

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['object_list'] = Newsletter.objects.filter(created_by=self.request.user)
		context_data['title'] = 'Список рассылок'
		return context_data


class NewsletterCreateView(CreateView):
	model = Newsletter
	form_class = NewsletterCreateForm
	success_url = reverse_lazy('newsletter:list_newsletter')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Создание рассылки'
		return context_data

	def form_valid(self, form):
		newsletter = form.save(commit=False)
		newsletter.created_by = self.request.user
		newsletter.status = 'создана'
		# log creation of creating

		if form.is_valid():
			if newsletter.mail_time_from <= now() <= newsletter.mail_time_to:
				newsletter.mail_status = 'запущена'
			# Send newsletter function with log creation

			elif newsletter.mail_time_to <= now():
				newsletter.mail_status = 'завершена'
		# log creation of ending

		newsletter.save()
		return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
	model = Newsletter
	form_class = NewsletterCreateForm
	success_url = reverse_lazy('newsletter:list_newsletter')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Редактирование рассылки'
		return context_data

	def form_valid(self, form):
		newsletter = form.save(commit=False)
		newsletter.status = 'отредактирована'
		# log creation of creating

		if form.is_valid():
			if newsletter.mail_time_from <= now() <= newsletter.mail_time_to:
				newsletter.mail_status = 'запущена'
			# Send newsletter function with log creation

			elif newsletter.mail_time_to <= now():
				newsletter.mail_status = 'завершена'
		# log creation of ending

		newsletter.save()
		return super().form_valid(form)


class NewsletterDeleteView(DeleteView):
	model = Newsletter
	success_url = reverse_lazy('newsletter:list_newsletter')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Удаление рассылки'
		return context_data

	def delete(self, request, *args, **kwargs):
		"""
		Call the delete() method on the fetched object and then redirect to the
		success URL.
		"""
		self.object = self.get_object()
		success_url = self.get_success_url()

		self.object.mail_status = 'удалена'
		# log creation of deleting

		self.object.delete()
		return HttpResponseRedirect(success_url)


class NewsletterDetailView(DetailView):
	model = Newsletter

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = f'{self.object}'
		return context_data


class NewsletterLogListView(ListView):
	model = NewsletterLog
	# Просмотр логов по конкретной рассылке?
	# def get_queryset(self):
	# 	return super().get_queryset().filter(newsletter_id=self.kwargs.get('pk'))

	def get_context_data(self, *args, **kwargs):
		context_data = super().get_context_data(*args, **kwargs)
		context_data['title'] = 'Отчеты проведенных рассылок'

		return context_data
