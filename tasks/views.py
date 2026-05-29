from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models.functions import Lower
from django.db.models import Case, IntegerField, Q, Value, When
from django.db.models import Case, IntegerField, Value, When
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    """Display tasks belonging to the current user with search, filter and sort."""

    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    # Allowed sort fields mapped to ORM expressions
    SORT_FIELDS = {
        'title': Lower('title').asc(),
        '-title': Lower('title').desc(),
        'priority': 'priority_rank',
        '-priority': '-priority_rank',
        'due_date': 'due_date',
        '-due_date': '-due_date',
        'created_at': 'created_at',
        '-created_at': '-created_at',
    }

    def get_queryset(self):
        # Explicit priority ordering: High -> Medium -> Low
        priority_order = Case(
            When(priority='H', then=Value(0)),
            When(priority='M', then=Value(1)),
            When(priority='L', then=Value(2)),
            output_field=IntegerField(),
        )
        qs = Task.objects.filter(user=self.request.user).annotate(
            priority_rank=priority_order
        )

        # Search by title or description
        search = self.request.GET.get('q', '').strip()
        if search:
            qs = qs.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Status filter
        filter_value = self.request.GET.get('filter', 'all')
        if filter_value == 'active':
            qs = qs.filter(is_done=False)
        elif filter_value == 'done':
            qs = qs.filter(is_done=True)

        # Sort: validated against whitelist
        sort = self.request.GET.get('sort')
        if sort in self.SORT_FIELDS:
            qs = qs.order_by('is_done', self.SORT_FIELDS[sort], '-created_at')
        else:
            qs = qs.order_by('is_done', 'priority_rank', 'due_date', '-created_at')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Counters for filter badges (independent of current filter)
        all_tasks = Task.objects.filter(user=self.request.user)
        context['count_all'] = all_tasks.count()
        context['count_active'] = all_tasks.filter(is_done=False).count()
        context['count_done'] = all_tasks.filter(is_done=True).count()
        context['current_filter'] = self.request.GET.get('filter', 'all')
        context['current_sort'] = self.request.GET.get('sort', '')
        context['search_query'] = self.request.GET.get('q', '')
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


@require_POST
def toggle_task(request, pk):
    """Flip the is_done flag. Returns JSON for AJAX, redirects for plain POST."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_done': task.is_done})
    return redirect('task_list')

class SignUpView(CreateView):
    """User registration view using Django's built-in form."""

    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')