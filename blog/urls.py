from django.urls import path
from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.home, name='homepage'),
    path('search/', views.post_search, name='post-search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('<slug:post>/', views.post_single, name='post-single'),
    path('category/<category>/', views.CatListView.as_view(), name='category'),
    path('generate_pdf/<int:pk>/', views.post_render_pdf_view, name='generate-pdf'),
]
