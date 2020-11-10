from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login 
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import logout
from  .forms import RegisterForm

from django.http import HttpResponseRedirect

from products.models import Product

#from django.contrib.auth.models import User
from users.models import User

def index(request):

    products = Product.objects.all().order_by('-id')

    return render(request,'index.html',{
        'message':'Listado de productos',
        'title': 'Productos',
        'products': products,
       # [
        #    {'title': 'playera', 'price':5, 'stock':True},#producto
         #   {'title': 'camisa', 'price':7, 'stock':True},
          #  {'title': 'mochila', 'price':20, 'stock':False},
          #  {'title': 'Laptop', 'price':660, 'stock':True},
        #]

    })

def login_view(request):

    if request.user.is_authenticated:
        return redirect('index')

    #Se obtine la informacion que se envia a travez del metodo post
    if request.method== 'POST':
        username = request.POST.get('username')# es un diccionario
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)#si no existe retorna none

        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])

            return redirect('index')
        else:
            messages.error(request, 'usuario o contraseña no validos')

       
    return render(request, 'users/login.html',{ 

    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('login')


def register(request):

    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)

    if request.method =='POST' and form.is_valid():
        user = form.save()#revisar form.py
      
        if user:
            login(request,user)
            messages.success(request, 'usuario creado exitosamente')
            return redirect('index') 


    return render(request,'users/register.html', {
        'form': form

    })
    
