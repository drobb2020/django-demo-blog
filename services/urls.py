from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'services'

urlpatterns = [
    path('comments/', views.comments, name='comments'),
    path('cookie/', views.cookie, name='cookie'),
    path('copyright/', views.copyright, name='copyright'),
    path('dcmapolicy/', views.dcmapolicy, name='dcmapolicy'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
    path('helpdesk/', views.helpdesk, name='helpdesk'),
    path('postagreement/', views.postagreement, name='postagreement'),
    path('privacy/', views.privacy, name='privacy'),
    path('termsandconditions/', views.termsandconditions, name='termsandconditions'),
    path('termsofuse/', views.termsofuse, name='termsofuse'),
    path('create_ticket/', views.create_ticket, name='create-ticket'),
    path('ticket_list/', views.ticket_list, name='ticket-list'),
    path('edit_ticket/<int:id>', views.edit_ticket, name='edit-ticket'),
    path('delete_ticket/<int:id>', views.delete_ticket, name='delete-ticket'),
    path('detail/<int:id>', views.detail, name='detail'),
]
