from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from app_message.forms import MessageForm
from app_message.models import Message


class MessageCreateView(LoginRequiredMixin, CreateView):
	model = Message
	form_class = MessageForm
	success_url = reverse_lazy('message:list_message')

	def form_valid(self, form):
		message = form.save(commit=False)
		message.created_by = self.request.user
		message.save()

		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['action'] = 'Создание'
		return context_data


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Message
	form_class = MessageForm
	success_url = reverse_lazy('message:list_message')

	def test_func(self):
		if self.request.user.is_staff and not self.request.user.is_superuser:
			return False
		return True

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['action'] = 'Редактировать'
		return context_data


class MessageListView(LoginRequiredMixin, ListView):
	model = Message

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Все сообщения'
		if self.request.user.is_staff:
			context_data['object_list'] = Message.objects.all()
		else:
			context_data['object_list'] = Message.objects.filter(created_by=self.request.user)
		return context_data


class MessageDetailView(LoginRequiredMixin, DetailView):
	model = Message

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Просмотр сообщения'
		return context_data


class MessageDeleteView(LoginRequiredMixin, DeleteView):
	model = Message
	success_url = reverse_lazy('message:list_message')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Удаление сообщения'
		return context_data

