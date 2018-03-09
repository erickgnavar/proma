from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import loader


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
