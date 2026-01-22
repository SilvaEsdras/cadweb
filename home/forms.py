from django import forms
from .models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido
from datetime import date

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem <= 0:
            raise forms.ValidationError("O campo ordem deve ser maior que zero.")
        return ordem

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%d/%m/%Y'),
        }

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc > date.today():
             raise forms.ValidationError("A data de nascimento não pode ser maior que a data atual.")
        return datanasc

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64']
        widgets = {
            'categoria': forms.HiddenInput(),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            
            # --- CORREÇÃO AQUI ---
            # Adicionamos attrs para incluir o ID, a classe img_init e o data-canvas
            'img_base64': forms.HiddenInput(attrs={
                'id': 'img_base64', 
                'class': 'img_init', 
                'data-canvas': 'imageCanvas'
            }),
            # ---------------------

            'preco': forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
        }
        labels = {
            'nome': 'Nome do Produto',
            'preco': 'Preço do Produto',
        }

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'qtde']
        
        widgets = {
            'produto': forms.HiddenInput(),  # Campo oculto para armazenar o ID do produto
            'qtde': forms.TextInput(attrs={'class': 'inteiro form-control'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.HiddenInput(),  # Campo oculto para armazenar o ID do cliente
        }

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido', 'produto', 'qtde']

        widgets = {
            'pedido': forms.HiddenInput(),
            'produto': forms.HiddenInput(),
            'qtde': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
        }