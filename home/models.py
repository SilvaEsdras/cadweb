from django.db import models
import random # Necessário para a chave de acesso

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name="C.P.F")
    datanasc = models.DateField(verbose_name="Data de Nascimento")

    def __str__(self):
        return self.nome
    
    @property
    def datanascimento(self):
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return None

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)

    def __str__(self):
        return self.nome
    
    @property
    def estoque(self):
        # Tenta buscar o estoque, se não existir, cria um novo com qtde 0
        estoque_item, flag_created = Estoque.objects.get_or_create(produto=self, defaults={'qtde': 0})
        return estoque_item

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - Quantidade: {self.qtde}'
    
class Pedido(models.Model):
    NOVO = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3
    CANCELADO = 4

    STATUS_CHOICES = [
        (NOVO, 'Novo'),
        (EM_ANDAMENTO, 'Em Andamento'),
        (CONCLUIDO, 'Concluído'),
        (CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOVO)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Status: {self.get_status_display()}"

    @property
    def data_pedidof(self):
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None

    @property
    def total(self):
        """Soma o total de todos os itens do pedido"""
        return sum(item.qtde * item.preco for item in self.itempedido_set.all())

    @property
    def qtdeItens(self):
        return self.itempedido_set.count()

    # --- NOVAS PROPRIEDADES DE PAGAMENTO (Slide 19) ---
    @property
    def pagamentos(self):
        return self.pagamento_set.all()

    @property
    def total_pago(self):
        return sum(p.valor for p in self.pagamentos)

    @property
    def debito(self):
        return self.total - self.total_pago

    # --- PROPRIEDADES PARA NOTA FISCAL (Desafio Slide 19) ---
    @property
    def icms(self): # Alíquota 18%
        return self.total * 0.18

    @property
    def ipi(self): # Alíquota 4%
        return self.total * 0.04

    @property
    def pis(self): # Alíquota 1.65%
        return self.total * 0.0165
    
    @property
    def cofins(self): # Alíquota 7.6%
        return self.total * 0.076

    @property
    def total_impostos(self):
        return self.icms + self.ipi + self.pis + self.cofins

    @property
    def total_com_impostos(self):
        return self.total + self.total_impostos

    @property
    def chave_acesso(self):
        # Gera uma chave aleatória baseada no ID e Data
        ts = int(self.data_pedido.timestamp()) if self.data_pedido else 0
        rand = random.randint(1000, 9999)
        return f"3523{self.id:04d}591{ts}{rand}55001000000001" # Formato fictício de DANFE

class ItemPedido(models.Model):
    # ... (Mantenha o código existente) ...
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde}) - Preço Unitário: {self.preco}"

    @property
    def total(self):
        return self.qtde * self.preco

# --- NOVO MODELO PAGAMENTO (Slide 19) ---
class Pagamento(models.Model):
    DINHEIRO = 1
    CARTAO = 2
    PIX = 3
    OUTRA = 4

    FORMA_CHOICES = [
        (DINHEIRO, 'Dinheiro'),
        (CARTAO, 'Cartão'),
        (PIX, 'Pix'),
        (OUTRA, 'Outra'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    forma = models.IntegerField(choices=FORMA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    data_pgto = models.DateTimeField(auto_now_add=True)
    
    @property
    def data_pgtof(self):
        if self.data_pgto:
            return self.data_pgto.strftime('%d/%m/%Y %H:%M')
        return None