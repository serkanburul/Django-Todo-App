from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        context['count'] = Task.objects.filter(completed=False).count()

        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        task = get_object_or_404(Task, id=data['id'])
        task.completed = data.get('is_checked')
        task.save()

        return JsonResponse({'message': 'Veri başarıyla alındı.', 'data': data})


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ('title', 'description', 'completed')
    success_url = reverse_lazy('taskList')
    template_name = 'base/task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ('title', 'description', 'completed')
    success_url = reverse_lazy('taskList')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('taskList')
    template_name = 'base/task_delete.html'

