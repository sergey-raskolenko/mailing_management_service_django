
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView

from app_client.forms import ClientCreateForm
from app_client.models import Client


class ClientCreateView(CreateView):
	model = Client
	form_class = ClientCreateForm
	success_url = reverse_lazy('client:list_client')

	def form_valid(self, form):
		message = form.save(commit=False)
		message.created_by = self.request.user
		message.save()

		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['action'] = 'Создание'
		return context_data


class ClientUpdateView(UpdateView):
	model = Client
	form_class = ClientCreateForm
	success_url = reverse_lazy('client:list_client')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['action'] = 'Редактировать'
		return context_data


class ClientListView(ListView):
	model = Client

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Все клиенты'
		return context_data


class ClientDetailView(DetailView):
	model = Client

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Просмотр клиента'
		return context_data


class ClientDeleteView(DeleteView):
	model = Client
	success_url = reverse_lazy('client:list_client')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Удаление клиента'
		return context_data
