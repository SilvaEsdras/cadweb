from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Categoria, Cliente
from .forms import CategoriaForm, ClienteForm

def index(request):
    return render(request, 'index.html')

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria')
    else:
        form = CategoriaForm()

    contexto = {
        'form': form,
    }
    return render(request, 'categoria/formulario.html', contexto)

def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria')
    else:
        form = CategoriaForm(instance=categoria)
        
    return render(request, 'categoria/formulario.html', {'form': form})

def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Registro excluído com sucesso')
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        
    return redirect('categoria')

def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        return render(request, 'categoria/detalhes.html', {'item': categoria})
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')
    
def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id'),
    }
    return render(request, 'cliente/lista.html', contexto)

def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente')
    else:
        form = ClienteForm()
    
    contexto = {'form': form}
    return render(request, 'cliente/formulario.html', contexto)

def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'cliente/formulario.html', {'form': form})

def remover_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
        cliente.delete()
        messages.success(request, 'Registro excluído com sucesso')
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
    return redirect('cliente')

def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
        return render(request, 'cliente/detalhes.html', {'item': cliente})
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')