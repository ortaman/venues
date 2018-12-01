
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Favorite(models.Model):
    id = models.CharField(primary_key=True, max_length=24, editable=True)
    name = models.CharField(max_length=50)
    address = models.TextField(max_length=200)

    photo = models.ImageField(upload_to='photos/', verbose_name=_('Phonto'), blank=True, null=True)

    lat = models.FloatField(verbose_name=_('Latitude'))
    lng = models.FloatField(verbose_name=_('Longitude'))

    tip_count = models.IntegerField(verbose_name=_('Tip count'))
    users_count = models.IntegerField(verbose_name=_('Users count'))
    checkins_count = models.IntegerField(verbose_name=_('Check-ins count'))
    visits_count = models.IntegerField(verbose_name=_('Visits count'))

    added_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Date of creation'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Date of the last update'))

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='added_by', verbose_name=_('Added by'), on_delete='DO_NOTHING')
