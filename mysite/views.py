# TODO: verificar cadastro
# TODO: verificar dashboard
# TODO:

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login as Dlogin, logout as Dlogout, authenticate
from django.contrib import messages

import pandas as pd


def home(request):
    return render(request, 'mysite/home.html')


def cadastro(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
        nome = request.POST['nome']
        try:
            usuario_aux = User.objects.get(email=user_name)
            if usuario_aux:
                messages.error("email já cadastrado")
        except User.DoesNotExist:
            newUser = User.objects.create_user(user_name, password, nome)
            newUser.save()
            return render(request, 'mysite/login.html')
    return render(request, 'mysite/cadastro.html')


def dados(request):
    df = pd.read_csv('datasets/nome_do_dataset.csv')
    dados = df.to_dict('records')
    return render(request, 'mysite/dados.html', {'dados': dados})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            Dlogin(request, user)
            return redirect('../')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'mysite/login.html')


def logout(request):
    Dlogout(request)
    return redirect('login')


def consulta(request):
    if request.method == 'POST':
        # obtem os dados da consulta do formulário
        parametro1 = request.POST.get('parametro1', '')
        parametro2 = request.POST.get('parametro2', '')

        # processa a consulta com os dados obtidos
        # você pode utilizar a biblioteca Pandas para isso
        # por exemplo: 
        # import pandas as pd
        # df = pd.read_csv('caminho/para/o/arquivo.csv')
        # resultado = df.loc[df['parametro1'] == parametro1 & df['parametro2'] == parametro2]

        resultado = "O resultado da consulta é: parametro1 = {}, parametro2 = {}".format(parametro1, parametro2)

        # adiciona o resultado da consulta ao contexto da página
        context = {
            'resultado': resultado
        }
        return render(request, 'mysite/consulta.html', context)
    else:
        return render(request, 'mysite/consulta.html')
