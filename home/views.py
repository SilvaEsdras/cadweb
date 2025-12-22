from django.shortcuts import render, redirect # type: ignore # Adicione o redirect
from .models import Categoria
from .forms import CategoriaForm # Importe o formulário

def index(request):
    return render(request, 'index.html')

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

# Nova view para o formulário
def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST) # pega os dados enviados pelo form
        if form.is_valid():
            form.save() # salva no banco
            return redirect('categoria') # volta para a lista
    else:
        form = CategoriaForm() # cria form vazio

    contexto = {
        'form': form,
    }
    return render(request, 'categoria/formulario.html', contexto)