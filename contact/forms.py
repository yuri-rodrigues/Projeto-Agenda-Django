from typing import Any, Mapping
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . import models

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update(
            {
            'class': 'classe-a classe-b',
            'placeholder': 'Veio do init',            
            })
        
        

    class Meta:
        model = models.Contact
        fields = (
            'first_name', 'last_name', 'phone',
        )
        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'class': 'classe-a classe-b',
        #             'placeholder': 'Escreva aqui'
        #         }
        #     )
        # }

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if first_name == last_name:
            self.add_error('last_name', ValidationError('Primeiro nome nao pode ser igual ao segundo', code='invalid'))
            self.add_error('first_name', ValidationError('Primeiro nome nao pode ser igual ao segundo', code='invalid'))
        
        # self.add_error('first_name', ValidationError('Mensagem de erro', code='invalid'))

        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if first_name == 'ABC':
            self.add_error('first_name', ValidationError('Digite algo diferente de ABC', code='invalid'))

        return first_name

