from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


def ticket_directory_path(instance, filename):
    return 'tickets/{0}/{1}'.format(instance.id, filename)


class Ticket(models.Model):
    STATUS = {
        ('Open', 'Open'),
        ('Closed', 'Closed')
    }

    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = RichTextField()
    status = models.CharField(max_length=10, choices=STATUS, default='Open')
    author = User.username
    assignee = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " - " + self.body
