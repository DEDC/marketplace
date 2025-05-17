# Django
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
# app users
from ..user_tokens import account_activation_token

class SendEmail:
    html_user_confirmation = ''
    text_user_confirmation = ''
    html_payment_success = ''
    text_payment_success = ''
    html_reset_password = ''
    text_reset_password = ''
    subject = ''
    from_ = ''
    to = ''

    def send_user_confirmation(self, user, request, *args, **kwargs):
        self.subject = 'Activa tu cuenta de usuario en CompraTabasco'
        self.to = user.email
        current_site = get_current_site(request)
        text_content = render_to_string(self.text_user_confirmation, {'user': user, 'domain': current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})
        html_content = render_to_string(self.html_user_confirmation, {'user': user, 'domain': current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})
        return self.send_user_email(html_content, text_content)
        
    def send_payment_success(self, user, invoice):
        self.subject = 'Compra exitosa en CompraTabasco'
        self.to = user.email
        text_content = render_to_string(self.text_payment_success, {'user': user, 'invoice': invoice})
        html_content = render_to_string(self.html_payment_success, {'user': user, 'invoice': invoice})
        return self.send_user_email(html_content, text_content)
    
    def reset_password_email(self, user, request):
        self.subject = 'Recuperación de contraseña en CompraTabasco'
        self.to = user.email
        current_site = get_current_site(request)
        text_content = render_to_string(self.text_reset_password, {'domain': current_site, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'user': user, 'token': account_activation_token.make_token(user)})
        html_content = render_to_string(self.html_reset_password, {'domain': current_site, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'user': user, 'token': account_activation_token.make_token(user)})
        return self.send_user_email(html_content, text_content)
    
    def send_user_email(self, html_content, text_content):
        message = EmailMultiAlternatives(self.subject, text_content, self.from_, [self.to])
        message.attach_alternative(text_content, "text/plain")
        message.attach_alternative(html_content, "text/html")
        try:
            message.send()
            return True
        except Exception as e:
            return False