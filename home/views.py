from django.shortcuts import render, redirect
from .models import Categoria
from .forms import CategoriaForm

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
            return redirect('categoria')
    else:
        form = CategoriaForm()

    contexto = {
        'form': form,
    }
    return render(request, 'categoria/formulario.html', contexto)

# --- Novas Views (Implementação do Slide) ---

def editar_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    
    if request.method == 'POST':
        # Combina os dados do formulário submetido com a instância do objeto existente
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save() # Salva as alterações
            return redirect('categoria') # Redireciona para a listagem
    else:
        # Método GET: Preenche o formulário com os dados da instância (para editar)
        form = CategoriaForm(instance=categoria)
        
    return render(request, 'categoria/formulario.html', {'form': form})

def remover_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    categoria.delete()
    return redirect('categoria')

def detalhes_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    return render(request, 'categoria/detalhes.html', {'item': categoria})