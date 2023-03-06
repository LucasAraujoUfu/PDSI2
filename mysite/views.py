from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

import pandas as pd

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(email=email, password=raw_password)
			login(request, user)
			return redirect('nome_da_pagina_inicial')
		else:
			form = UserCreationForm()
			return render(request, 'cadastro.html', {'form': form})


def dados(request):
    df = pd.read_csv('datasets/nome_do_dataset.csv')
    dados = df.to_dict('records')
    return render(request, 'dados.html', {'dados': dados})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dados')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'login.html')
    

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
        return render(request, 'consulta.html', context)
    else:
        return render(request, 'consulta.html')


