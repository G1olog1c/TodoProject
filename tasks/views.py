from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Case, IntegerField, Value, When
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    """Display tasks belonging to the current user, with optional filter."""

    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Order priorities explicitly: High -> Medium -> Low
        priority_order = Case(
            When(priority='H', then=Value(0)),
            When(priority='M', then=Value(1)),
            When(priority='L', then=Value(2)),
            output_field=IntegerField(),
        )
        qs = Task.objects.filter(user=self.request.user).annotate(
            priority_rank=priority_order
        ).order_by('is_done', 'priority_rank', 'due_date', '-created_at')

        # Filter from query string: ?filter=active or ?filter=done
        filter_value = self.request.GET.get('filter')
        if filter_value == 'active':
            qs = qs.filter(is_done=False)
        elif filter_value == 'done':
            qs = qs.filter(is_done=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'priority', 'due_date']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        # Assign current user before saving
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'priority', 'due_date', 'is_done']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


def toggle_task(request, pk):
    """Flip the is_done flag for a task."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    return redirect('task_list')

class SignUpView(CreateView):
    """User registration view using Django's built-in form."""

    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')