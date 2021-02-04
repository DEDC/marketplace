# app users
from .forms import fLogin, fRegistroUsuarios

def login_form_processor(request):
    form_login = fLogin(label_suffix = '')
    form_user = fRegistroUsuarios(label_suffix = '')
    return {'form_login': form_login, 'form_user': form_user}