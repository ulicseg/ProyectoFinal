from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    texto = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': ''}), 
        label='' 
    )

    class Meta:
        model = Comentario
        fields = ['texto']