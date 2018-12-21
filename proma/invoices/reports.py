from proma.common.utils import PDFReport
from proma.config.models import Configuration


class InvoicePDF(PDFReport):

    template_name = "pdf/invoice.html"
    bootstrap_styles = True

    def __init__(self, invoice, *args, **kwargs):
        self.invoice = invoice
        super().__init__(*args, **kwargs)

    def get_filename(self):
        return f"{self.invoice.number}.pdf"

    def get_context(self):
        config = Configuration.get_instance()
        return {
            "invoice": self.invoice,
            "currency": self.invoice.project.currency,
            "company": config.get_info("company"),
            "logo_path": config.get_company_logo_path(),
        }
