# Django
from django import forms
# app usuarios
from .models import Usuarios, Direcciones

class fLogin(forms.Form):
    username = forms.CharField(label = 'Correo electrónico o teléfono', max_length = 100, label_suffix = '')
    password = forms.CharField(label = 'Contraseña', max_length = 128, label_suffix = '', 
        widget = forms.PasswordInput()
    )

class fRegistroUsuarios(forms.ModelForm):
    repeat_password = forms.CharField(label = 'Confirmar contraseña', 
        widget = forms.PasswordInput()
    )
    privcheck = forms.BooleanField(label = 'Acepto el Aviso de Privacidad',
        widget = forms.CheckboxInput()
    )

    class Meta:
        model = Usuarios
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
        error_messages = {
            'email': {
                'unique': 'Este correo electrónico ya fue registrado'
            },
            'phone_number': {
                'unique': 'Este número de teléfono ya fue registrado'
            }
        }
    
    def __init__(self, *args, **kwargs):
        super(fRegistroUsuarios, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data['repeat_password']
        if not repeat_password == self.cleaned_data['password']:
            raise forms.ValidationError('La contraseña no coincide', code='invalid')
        return repeat_password

class fResetPassword(forms.Form):
    current_password = forms.CharField(label = 'Contraseña actual', max_length = 128, widget = forms.PasswordInput)
    new_password = forms.CharField(label = 'Nueva contraseña', max_length = 128, widget = forms.PasswordInput)
    repeat_password = forms.CharField(label = 'Confirmar nueva contraseña', max_length = 128, widget = forms.PasswordInput)

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data['repeat_password']
        if not repeat_password == self.cleaned_data['new_password']:
            raise forms.ValidationError('La contraseña no coincide', code='invalid')
        return repeat_password

class fResetPasswordEmail(forms.Form):
    email = forms.EmailField(label = 'Ingrese el correo electrónico que registró', label_suffix = '')

class fSetPasswordEmail(fResetPassword):
    current_password = None

class fRegistroDirecciones(forms.ModelForm):
    class Meta:
        model = Direcciones
        fields = '__all__'
        widgets = {
            'instrucciones': forms.Textarea(attrs = {'class': 'materialize-textarea'})
        }