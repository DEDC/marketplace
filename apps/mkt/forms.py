from django import forms
from apps.mkt.models import Productos, Imagenes


class fRegistroProducto(forms.ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'

class fExtra_Imagenes(forms.ModelForm):
    class Meta:
        model = Imagenes
        fields = '__all__'