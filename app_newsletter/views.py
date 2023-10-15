from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
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
		if self.request.user.is_staff:
			context_data['object_list'] = Newsletter.objects.all()
		else:
			context_data['object_list'] = Newsletter.objects.filter(created_by=self.request.user)
		return context_data


class NewsletterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Newsletter
	form_class = NewsletterCreateForm
	success_url = reverse_lazy('newsletter:list_newsletter')

	def test_func(self):
		if self.get_object().created_by == self.request.user:
			return True
		elif self.request.user.is_superuser:
			return True
		elif self.request.user.is_staff:
			return False

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Создание рассылки'
		return context_data

	def form_valid(self, form):
		newsletter = form.save(commit=False)
		newsletter.created_by = self.request.user
		newsletter.status = 'создана'
		newsletter.save()
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
	model = Newsletter
	form_class = NewsletterCreateForm
	success_url = reverse_lazy('newsletter:list_newsletter')

	def test_func(self):
		if self.get_object().created_by == self.request.user:
			return True
		elif self.request.user.is_superuser:
			return True
		elif self.request.user.is_staff:
			return False

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Редактирование рассылки'
		return context_data

	def form_valid(self, form):
		newsletter = form.save(commit=False)
		newsletter.status = 'отредактирована'
		newsletter.save()
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
	model = Newsletter
	success_url = reverse_lazy('newsletter:list_newsletter')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Удаление рассылки'
		return context_data

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		success_url = self.get_success_url()

		self.object.status = 'удалена'
		# log creation of deleting
		NewsletterLog.objects.create_log(self.object, self.object.status)

		self.object.is_active = False
		return HttpResponseRedirect(success_url)


class NewsletterDetailView(LoginRequiredMixin, DetailView):
	model = Newsletter

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = f'{self.object}'
		return context_data


def toggle_is_active(*args, **kwargs):
	print(kwargs.get('pk'))
	newsletter = get_object_or_404(Newsletter, pk=kwargs.get('pk'))
	if newsletter.is_active:
		newsletter.is_active = False
	else:
		newsletter.is_active = True
	newsletter.save()

	return redirect(reverse_lazy('newsletter:list_newsletter'))


class NewsletterLogListView(LoginRequiredMixin, ListView):
	model = NewsletterLog
	# Просмотр логов по конкретной рассылке?

	def get_queryset(self):
		queryset = super().get_queryset().filter(newsletter_id=self.kwargs.get('pk'))
		queryset = queryset.order_by('-pk')
		return queryset

	def get_context_data(self, *args, **kwargs):
		context_data = super().get_context_data(*args, **kwargs)
		context_data['title'] = 'Отчеты проведенных рассылок'

		return context_data
