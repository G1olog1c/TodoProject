from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    """Single to-do item belonging to a user."""

    class Priority(models.TextChoices):
        LOW = 'L', _('Niski')
        MEDIUM = 'M', _('Średni')
        HIGH = 'H', _('Wysoki')

    title = models.CharField(_('Tytuł'), max_length=200)
    description = models.TextField(_('Opis'), blank=True)
    is_done = models.BooleanField(_('Wykonane'), default=False)
    priority = models.CharField(
        _('Priorytet'),
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    due_date = models.DateField(_('Termin'), null=True, blank=True)
    created_at = models.DateTimeField(_('Utworzono'), auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('Użytkownik'),
    )

    class Meta:
        ordering = ['is_done', '-created_at']
        verbose_name = _('Zadanie')
        verbose_name_plural = _('Zadania')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_list')

    @property
    def is_overdue(self):
        """Return True if the task is past its due date and not completed."""
        if self.due_date and not self.is_done:
            return self.due_date < timezone.localdate()
        return False

    @property
    def due_status(self):
        """Return CSS class hint for the due date: overdue/today/soon/none."""
        if not self.due_date or self.is_done:
            return ''
        today = timezone.localdate()
        delta = (self.due_date - today).days
        if delta < 0:
            return 'overdue'
        if delta == 0:
            return 'today'
        if delta <= 2:
            return 'soon'
        return ''