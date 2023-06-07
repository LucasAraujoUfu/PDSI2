from django.shortcuts import render, redirect
from .models import dataset
from django.contrib.auth import login as Dlogin, logout as Dlogout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


class IA:

    def __init__(self):
        self.knn = KNeighborsClassifier(n_neighbors=5)
        self.cols = None

    def fit(self, X, y):
        self.knn.fit(X, y)

    def is_trained(self):
        if hasattr(self.knn, 'classes_'):
            return True
        else:
            return False


ia = IA()


def home(request):
    return render(request, 'mysite/home.html')


@login_required
def dados(request):
    if request.method == 'POST':
        if 'arq' in request.FILES:
            file = request.FILES['arq']
            df = pd.read_csv(file)
            ia.cols = df.columns
            X = np.array(df)
            y = X[:, -1]
            X = X[:, :-1]
            ia.fit(X, y)
            for _, row in df.iterrows():
                ln = dataset(**row)
                ln.save()
            return render(request, 'mysite/dados.html', {'cols': df.columns, 'dados': df.to_numpy()})
        else:
            messages.error(request, 'Arquivo não localizado')
    return render(request, 'mysite/dados.html')


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


@login_required
def logout(request):
    Dlogout(request)
    return redirect('login')


@login_required
def consulta(request):
    if ia.is_trained():
        if request.method == 'POST':
            res = []
            if 'arq' in request.FILES:
                file = request.FILES['arq']
                df = pd.read_csv(file, header=None)
                X = np.array(df)
                for i in X:
                    if ia.knn.predict([i]):
                        res.append('Possivel Formando')
                    else:
                        res.append('Possivel desistente')
                return render(request, 'mysite/consulta.html', {'resultados': res})
            else:
                data = []

                for i in ia.cols[:-1]:
                    data.append(request.POST.get(i, ''))

                if ia.knn.predict([data]):
                    context = {'resultado': 'Possivel Formando'}
                else:
                    context = {'resultado': 'Possivel desistente'}

                return render(request, 'mysite/consulta.html', context)
        else:
            return render(request, 'mysite/consulta.html', {'cols': ia.cols[:-1]})
    else:
        return status(request)


@login_required
def train(request):
    if dataset.objects.count():
       return render(request, 'mysite/train.html', {'data': 'ok'})
    return render(request, 'mysite/train.html')


@login_required
def status(request):
    dt = {}
    if ia.is_trained():
        dt['status'] = "TREINADO"
    else:
        dt['status'] = "NAO TREINADO"
    return render(request, 'mysite/status.html', dt)


@login_required
def visual(request):
    objects = dataset.objects.all()
    dados = []
    for i in objects.values():
        dados.append(i.values())
    dado = dataset()  # Cria uma instância vazia do modelo para acessar o atributo _meta
    columns = [field.name for field in dado._meta.fields]
    return render(request, 'mysite/visual.html', {"cols": columns,"linhas": dados})


@login_required
def train_db(request):
    df = pd.DataFrame(dataset.objects.all().values())
    ia.cols = list(df.columns)[1:]
    X1 = np.array(df)
    y = X1[:, -1].astype(int)
    X = X1[:, 1:-1]
    ia.fit(X, y)
    return render(request, 'mysite/dados.html', {'cols': ia.cols, 'dados': X1[:, 1:]})
