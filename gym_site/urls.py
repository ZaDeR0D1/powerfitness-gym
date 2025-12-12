from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs_page, name='programs'),
    path('trainers/', views.trainers, name='trainers'),
    path('schedule/', views.schedule, name='schedule'),
    path('pricing/', views.pricing, name='pricing'), 
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('membership/', views.membership, name='membership'), 
    path('search/', views.search_view, name='search'),
    path('search/autocomplete/', views.search_autocomplete, name='search_autocomplete'),
    path('coaches/<int:coach_id>/', views.coach_detail, name='coach_detail'),
    path('programs/<int:program_id>/', views.program_detail, name='program_detail'),
    path('search-home/', views.SearchHomeView.as_view(), name='search_home'),

]