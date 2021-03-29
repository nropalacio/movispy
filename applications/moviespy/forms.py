from django import forms

class Fecha(forms.Form):
    fecha = forms.DateField(label='Fecha', required=True)