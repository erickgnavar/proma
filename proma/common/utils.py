import os

import pdfkit
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse
from django.template import loader
from django.views.generic import View


class Email(object):

    @staticmethod
    def send_mail(*args, **kwargs):
        """
        Send an html message
        Args:
            template_name: required
            context: required, a dict for render template
            subject: required
            from_email: optional, email address
            to: required, array of destination emails
            plain: optional, default is false
        Raise:
            TemplateDoesNotExist
        """
        subject = kwargs.get('subject')
        from_email = kwargs.get('from_email', settings.DEFAULT_FROM_EMAIL)
        to = kwargs.get('to')
        body = kwargs.get('body', '')

        plain = kwargs.get('plain', False)

        if plain:
            message = EmailMessage(subject, body, from_email, to)
        else:
            context = kwargs.get('context', {})
            template = loader.get_template(kwargs.get('template_name'))
            html_content = template.render(context)
            message = EmailMultiAlternatives(subject, body, from_email, to)
            message.attach_alternative(html_content, 'text/html')
        message.send(fail_silently=not settings.DEBUG)


class PDFView(View):
    """
    Create a PDF response using pdfkit
    """

    template_name = None
    bootstrap_styles = False

    def get(self, request, *args, **kwargs):
        content = self._render(self.get_context_data())
        filename = self.get_filename()
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    def _render(self, context):
        context.update(self._get_default_context())
        template = loader.get_template(self.template_name)
        content = template.render(context)
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'UTF-8',
            'quiet': '',
        }
        return pdfkit.from_string(content, False, options=options)

    def _get_default_context(self):
        context = {}
        if self.bootstrap_styles:
            path = os.path.join(settings.BASE_DIR, 'proma', 'static', 'vendor', 'css', 'bootstrap.min.css')
            with open(path) as f:
                context.update({
                    'bootstrap_styles': f.read(),
                })
        return context

    def get_context_data(self):
        raise NotImplementedError

    def get_filename(self):
        raise NotImplementedError
