from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    """Single to-do item belonging to a user."""

    title = models.CharField(_('Tytuł'), max_length=200)
    description = models.TextField(_('Opis'), blank=True)
    is_done = models.BooleanField(_('Wykonane'), default=False)
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