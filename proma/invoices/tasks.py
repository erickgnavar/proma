from celery.utils.log import get_task_logger
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext as _

from config.celery import app
from proma.common.utils import Email
from proma.invoices.reports import InvoicePDF

from .models import Invoice


logger = get_task_logger(__name__)


@app.task(name='invoices.notify_open_invoice', retry_limit=3, default_retry_delay=10, bind=True)
def notify_open_invoice(self, invoice_id):
    logger.info('Notification for invoice:%d', invoice_id)
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        assert invoice.status == Invoice.OPEN, f'The invoice:{invoice.id} is not opened yet'
        path = reverse('invoices:invoice-public-detail', kwargs={'token': invoice.token})
        report = InvoicePDF(invoice=invoice)
        Email.send_mail(
            template_name='email/invoice_opened.html',
            context={
                'invoice': invoice,
                'url': f'{settings.DOMAIN}{path}',
            },
            subject=_('New invoice #%s' % invoice.number),
            to=[invoice.client.email],
            attachments=(
                (report.get_filename(), report.render(), 'application/pdf'),
            )
        )
    except Exception as ex:
        self.retry(exc=ex)
    logger.info('Open invoice:%d email notification sent', invoice.id)
