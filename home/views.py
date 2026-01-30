from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps
from django.contrib.auth.decorators import login_required
from .models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido, Pagamento
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm, PedidoForm, ItemPedidoForm, PagamentoForm

@login_required
def index(request):
    return render(request, 'index.html')

# --- VIEWS CATEGORIA ---
@login_required
def categoria(request):
    contexto = {'lista': Categoria.objects.all().order_by('-id')}
    return render(request, 'categoria/lista.html', contexto)

@login_required
def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('categoria')
    else:
        form = CategoriaForm()
    return render(request, 'categoria/formulario.html', {'form': form})

@login_required
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

@login_required
def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Registro excluído com sucesso')
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
    return redirect('categoria')

@login_required
def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        return render(request, 'categoria/detalhes.html', {'item': categoria})
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('categoria')

# --- VIEWS CLIENTE ---
@login_required
def cliente(request):
    contexto = {'lista': Cliente.objects.all().order_by('-id')}
    return render(request, 'cliente/lista.html', contexto)

@login_required
def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('cliente')
    else:
        form = ClienteForm()
    return render(request, 'cliente/formulario.html', {'form': form})

@login_required
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

@login_required
def remover_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
        cliente.delete()
        messages.success(request, 'Registro excluído com sucesso')
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
    return redirect('cliente')

@login_required
def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
        return render(request, 'cliente/detalhes.html', {'item': cliente})
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')

# --- VIEWS PRODUTO ---
@login_required
def produto(request):
    contexto = {'lista': Produto.objects.all().order_by('-id')}
    return render(request, 'produto/lista.html', contexto)

@login_required
def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('produto')
    else:
        form = ProdutoForm()
    return render(request, 'produto/form.html', {'form': form})

@login_required
def editar_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('produto')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto/form.html', {'form': form})

@login_required
def remover_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        produto.delete()
        messages.success(request, 'Registro excluído com sucesso')
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
    return redirect('produto')

@login_required
def detalhes_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
        return render(request, 'produto/detalhes.html', {'item': produto})
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('produto')

@login_required
def ajustar_estoque(request, id):
    produto = Produto.objects.get(pk=id)
    estoque = produto.estoque # acessa a property criada no model
    
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            estoque = form.save()
            messages.success(request, 'Estoque atualizado com sucesso')
            return redirect('produto') 
    else:
         form = EstoqueForm(instance=estoque)
         
    return render(request, 'produto/estoque.html', {'form': form})

# --- VIEWS TESTES / AUTOCOMPLETE ---
@login_required
def teste1(request):
    return render(request, 'testes/teste1.html')

@login_required
def teste2(request):
    return render(request, 'testes/teste2.html')

@login_required
def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo (ex: home.Categoria)
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

# --- VIEWS PEDIDO ---
@login_required
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})

@login_required
def novo_pedido(request, id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Registro não encontrado')
            return redirect('cliente')
        
        # Cria uma instância de pedido com o cliente selecionado (sem salvar no banco ainda)
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedido/form.html', {'form': form})
    else:
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            messages.success(request, 'Pedido criado com sucesso!')
            return redirect('pedido')

@login_required
def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')
    
    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else: # method Post
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False) 
            item_pedido.preco = item_pedido.produto.preco # Salva o preço atual do produto
            
            # Tratamento de Estoque
            estoque_atual = item_pedido.produto.estoque
            
            # Verifica se tem estoque suficiente
            if estoque_atual.qtde >= item_pedido.qtde:
                estoque_atual.qtde -= item_pedido.qtde
                estoque_atual.save() # Atualiza o estoque
                item_pedido.save()   # Salva o item do pedido
                messages.success(request, 'Produto adicionado com sucesso!')
            else:
                messages.error(request, f'Estoque insuficiente. Disponível: {estoque_atual.qtde}')
        else:
             messages.error(request, 'Erro ao adicionar produto')
        
        # Redireciona para limpar o POST e atualizar a página
        return redirect('detalhes_pedido', id=id)
                  
    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def editar_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')
         
    pedido = item_pedido.pedido
    quantidade_anterior = item_pedido.qtde
    
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido = form.save(commit=False)
            
            # Lógica de ajuste de estoque na edição
            estoque = item_pedido.produto.estoque
            nova_quantidade = item_pedido.qtde
            diferenca = nova_quantidade - quantidade_anterior
            
            # Se diferença > 0, estamos tirando mais do estoque.
            # Se diferença < 0, estamos devolvendo ao estoque.
            
            if estoque.qtde >= diferenca:
                estoque.qtde -= diferenca
                estoque.save()
                item_pedido.save()
                messages.success(request, 'Item atualizado com sucesso')
                return redirect('detalhes_pedido', id=pedido.id)
            else:
                messages.error(request, f'Estoque insuficiente para essa quantidade. Disponível extra: {estoque.qtde}')
                
    else:
        form = ItemPedidoForm(instance=item_pedido)
        
    contexto = {
        'pedido': pedido,
        'form': form,
        'item_pedido': item_pedido, # Passamos o item para saber que estamos editando
        'editando': True # Flag para ajudar no template se quiser mudar o texto do botão
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def remover_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')
    
    pedido_id = item_pedido.pedido.id
    
    # Devolve a quantidade ao estoque
    estoque = item_pedido.produto.estoque
    estoque.qtde += item_pedido.qtde
    estoque.save()
    
    # Remove o item
    item_pedido.delete()
    messages.success(request, 'Item removido e estoque estornado.')

    return redirect('detalhes_pedido', id=pedido_id)

@login_required
def remover_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
        
        # --- Lógica de Estorno de Estoque ---
        # Antes de deletar o pedido, percorremos seus itens
        for item in pedido.itempedido_set.all():
            estoque = item.produto.estoque
            estoque.qtde += item.qtde # Devolve a quantidade
            estoque.save()

        pedido.delete() # Agora exclui o pedido (e os itens em cascata)
        messages.success(request, 'Pedido excluído e estoque estornado com sucesso')
        
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        
    return redirect('pedido')

# --- VIEWS PAGAMENTO E NOTA FISCAL ---

@login_required
def form_pagamento(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')
    
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('form_pagamento', id=id)
        else:
            messages.error(request, 'Erro ao registrar pagamento. Verifique os valores informados.')
    
    if request.method == 'GET':
        pagamento = Pagamento(pedido=pedido)
        form = PagamentoForm(instance=pagamento)
    
    pagamento_instance = Pagamento(pedido=pedido)
    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com Sucesso')
            return redirect('form_pagamento', id=id)
        else:
            messages.error(request, 'Erro: O valor do pagamento excede o débito ou é inválido.')
    else:
        form = PagamentoForm(instance=pagamento_instance)

    contexto = {
        'pedido': pedido,
        'form': form,
    }    
    return render(request, 'pedido/pagamento.html', contexto)

@login_required
def remover_pagamento(request, id):
    try:
        pagamento = Pagamento.objects.get(pk=id)
        pedido_id = pagamento.pedido.id
        pagamento.delete()
        messages.success(request, 'Pagamento removido com sucesso')
        return redirect('form_pagamento', id=pedido_id)
    except Pagamento.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')

@login_required
def nota_fiscal(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')
    return render(request, 'pedido/nota_fiscal.html', {'pedido': pedido})