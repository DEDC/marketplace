from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from ..user_tokens import account_activation_token

class EmailConfirmation:
    html_confirmation_content = ''
    text_confirmation_content = ''
    subject = 'Activa tu cuenta de usuario en CompraTabasco.com'
    from_ = ''
    to = ''

    def send_email_confirmation(self, user, request, *args, **kwargs):
        text, html = self.render_templates(user, request)
        self.to = user.email
        message = EmailMultiAlternatives(self.subject, text, self.from_, [self.to])
        message.attach_alternative(text, "text/plain")
        message.attach_alternative(html, "text/html")
        try:
            message.send()
            return True
        except Exception as e:
            return False

    def render_templates(self, user, request):
        current_site = get_current_site(request)
        text = render_to_string(self.text_confirmation_content, {'user': user, 'domain': current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})
        html = render_to_string(self.html_confirmation_content, {'user': user, 'domain': current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})
        return [text, html]