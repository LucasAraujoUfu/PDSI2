from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dados/', views.dados, name='dados'),
    path('login/', views.login_view, name='login'),
    path('consulta/', views.consulta, name='consulta'),
]

