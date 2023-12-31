from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView

from app_client.forms import ClientCreateForm
from app_client.models import Client


class ClientCreateView(LoginRequiredMixin, CreateView):
	"""
	Представление для создания нового клиента авторизованным пользователем
	"""
	model = Client
	form_class = ClientCreateForm
	success_url = reverse_lazy('client:list_client')

	def form_valid(self, form):
		client = form.save(commit=False)
		client.created_by = self.request.user
		client.save()

		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['action'] = 'Создание'
		return context_data


class ClientUpdateView(LoginRequiredMixin, UpdateView):
	"""
	Представление для обновления клиента авторизованным пользователем
	"""
	model = Client
	form_class = ClientCreateForm
	success_url = reverse_lazy('client:list_client')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['action'] = 'Редактировать'
		return context_data


class ClientListView(LoginRequiredMixin, ListView):
	"""
	Представление для отображения списка клиентов авторизованному пользователю
	"""
	model = Client

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Все мои клиенты'
		object_list = Client.objects.all()
		if self.request.user.is_staff:
			context_data['object_list'] = object_list
		else:
			context_data['object_list'] = object_list.filter(created_by=self.request.user)
		return context_data


class ClientDetailView(LoginRequiredMixin, DetailView):
	"""
	Представление для детального отображения клиента авторизованному пользователю
	"""
	model = Client

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Просмотр моего клиента'
		return context_data


class ClientDeleteView(LoginRequiredMixin, DeleteView):
	"""
	Представление для удаления клиента авторизованному пользователю
	"""
	model = Client
	success_url = reverse_lazy('client:list_client')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Удаление клиента'
		return context_data
