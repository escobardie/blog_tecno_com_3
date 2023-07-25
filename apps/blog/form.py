from django import forms
from .models import Articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = [
            'titulo', 'bajada', 'contenido', 'imagen', 'categoria', 'etiquetas'
        ]

        widgets = {
            'titulo':forms.TextInput(attrs={'class':'form-control'}),
            'bajada':forms.TextInput(attrs={'class':'form-control'}),
            'contenido':forms.Textarea(attrs={'class':'form-control'}),
            'imagen':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'categoria':forms.Select(attrs={'class':'form-control'}),
            'etiquetas':forms.SelectMultiple(attrs={'class':'form-control'}),
        }