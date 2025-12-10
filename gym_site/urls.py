from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs_page, name='programs'),
    path('trainers/', views.trainers, name='trainers'),
    path('schedule/', views.schedule, name='schedule'),
    path('pricing/', views.pricing, name='pricing'),  # ← это должно быть вместо membership
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('membership/', views.membership, name='membership'),  # алиас для pricing
]