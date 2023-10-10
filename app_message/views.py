from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from app_message.forms import MessageForm
from app_message.models import Message


class MessageCreateView(CreateView):
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


class MessageUpdateView(UpdateView):
	model = Message
	form_class = MessageForm
	success_url = reverse_lazy('message:list_message')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['action'] = 'Редактирование'
		return context_data


class MessageListView(ListView):
	model = Message

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Все сообщения'
		return context_data


class MessageDetailView(DetailView):
	model = Message

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Просмотр сообщения'
		return context_data


class MessageDeleteView(DeleteView):
	model = Message
	success_url = reverse_lazy('message:list_message')

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data['title'] = 'Удаление сообщения'
		return context_data

