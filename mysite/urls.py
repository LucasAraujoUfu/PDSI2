from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dados/', views.dados, name='dados'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('consulta/', views.consulta, name='consulta'),
]
