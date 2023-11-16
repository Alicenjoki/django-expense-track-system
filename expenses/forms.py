from django import forms
from .models import *

class AddExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control',
                }
        )
    class Meta:
        model= Expense
        fields = ['amount', 'description', 'category', 'date',]

class EditExpenseForm(forms.ModelForm):
    model = Expense
    fields = ['amount', 'description', 'category', 'date',]