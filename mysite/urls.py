from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('dados/', views.dados, name='dados'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('consulta/', views.consulta, name='consulta'),
    path('train/', views.train, name='fit'),
    path('status/', views.status, name='status'),
    path('visual/', views.visual, name='dados'),
    path('train_db/', views.train_db),
]
