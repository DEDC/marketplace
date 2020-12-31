from django.views.defaults import page_not_found

def error404(request):
    nombre_template = '404.html' 
    return page_not_found(request, template_name = 'error_handler/404.html')