import django_filters
from django import forms
from django.contrib.auth.models import User

from .models import Ticket


class TicketForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ['title', 'body', 'status', 'user']


class TicketFilter(django_filters.FilterSet):
    
    class Meta:
        model = Ticket
        fields = ['title', 'status']
