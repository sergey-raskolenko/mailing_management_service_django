from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from app_newsletter.forms import NewsletterCreateForm
from app_newsletter.models import Newsletter, NewsletterLog
from app_newsletter.services import send_newsletter


class NewsletterListView(LoginRequiredMixin, ListView):
	model = Newsletter

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Список рассылок'
		object_list = Newsletter.objects.all()
		if self.request.user.is_staff:
			context_data['object_list'] = object_list
		else:
			context_data['object_list'] = object_list.filter(created_by=self.request.user)
		return context_data


class NewsletterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	"""
	Представление для создания новой рассылки авторизованным пользователем, кроме стаффа.
	При создании рассылки автоматически отправляется сообщение для клиентов, указанных в ней
	"""
	model = Newsletter
	form_class = NewsletterCreateForm
	success_url = reverse_lazy('newsletter:list_newsletter')

	def test_func(self):
		if self.request.user.is_staff and not self.request.user.is_superuser:
			return False
		return True

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Создание рассылки'
		return context_data

	def form_valid(self, form):
		newsletter = form.save()
		newsletter.created_by = self.request.user
		newsletter.status = 'создана'
		# log creation of creating
		NewsletterLog.objects.create_log(newsletter, newsletter.status)

		if newsletter.mail_time_from <= now() <= newsletter.mail_time_to:
			newsletter.status = 'запущена'
			# Send newsletter function with log creation
			send_newsletter(newsletter)

		elif newsletter.mail_time_to <= now():
			newsletter.status = 'завершена'
			# log creation of ending
			NewsletterLog.objects.create_log(newsletter, newsletter.status)

		newsletter.save()
		return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	"""
	Представление для обновления рассылки авторизованным пользователем, кроме стаффа.
	После редактирования рассылки автоматически отправляется сообщение для клиентов, указанных в ней
	"""
	model = Newsletter
	form_class = NewsletterCreateForm
	success_url = reverse_lazy('newsletter:list_newsletter')

	def test_func(self):
		if self.request.user.is_staff and not self.request.user.is_superuser:
			return False
		return True

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Редактирование рассылки'
		return context_data

	def form_valid(self, form):
		newsletter = form.save()
		newsletter.status = 'отредактирована'
		# log creation of creating
		NewsletterLog.objects.create_log(newsletter, newsletter.status)

		if newsletter.is_active:
			if newsletter.mail_time_from <= now() <= newsletter.mail_time_to:
				newsletter.status = 'запущена'
				# Send newsletter function with log creation
				send_newsletter(newsletter)

			elif newsletter.mail_time_to <= now():
				newsletter.status = 'завершена'
				# log creation of ending
				NewsletterLog.objects.create_log(newsletter, newsletter.status)

		newsletter.save()
		return super().form_valid(form)


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
	"""
	Представление для удаления рассылки авторизованному пользователю
	"""
	model = Newsletter
	success_url = reverse_lazy('newsletter:list_newsletter')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Удаление рассылки'
		return context_data


class NewsletterDetailView(LoginRequiredMixin, DetailView):
	"""
	Представление для детального отображения рассылки авторизованному пользователю
	"""
	model = Newsletter

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = f'{self.object}'
		return context_data


def toggle_is_active(*args, **kwargs):
	"""
	Контроллер для изменения поля активности рассылки
	"""
	print(kwargs.get('pk'))
	newsletter = get_object_or_404(Newsletter, pk=kwargs.get('pk'))
	if newsletter.is_active:
		newsletter.is_active = False
	else:
		newsletter.is_active = True
	newsletter.save()

	return redirect(reverse_lazy('newsletter:list_newsletter'))


class NewsletterLogListView(LoginRequiredMixin, ListView):
	"""
	Представление для отображения списка логов конкретной рассылки авторизованному пользователю
	"""
	model = NewsletterLog

	def get_queryset(self):
		queryset = super().get_queryset().filter(newsletter_id=self.kwargs.get('pk'))
		queryset = queryset.order_by('-pk')
		return queryset

	def get_context_data(self, *args, **kwargs):
		context_data = super().get_context_data(*args, **kwargs)
		context_data['title'] = 'Отчеты проведенных рассылок'

		return context_data
