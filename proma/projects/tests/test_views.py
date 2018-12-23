from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from mixer.backend.django import mixer

from .. import forms, views
from ..models import Project, Timesheet


class ProjectCreateViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ProjectCreateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")

    def test_match_expected_view(self):
        url = resolve("/projects/create/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)

    def test_create_project(self):
        client = mixer.blend("clients.Client")
        data = {
            "name": "test",
            "client": client.id,
            "start_date": "2018-01-01",
            "payment_type": Project.FLAT_RATE,
            "currency": Project.USD,
            "rate": 20,
        }
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse("projects:project-list"), response["location"])

    def test_create_project_missing_fields(self):
        data = {"name": "test"}
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data["form"].errors) > 0)


class ProjectUpdateViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ProjectUpdateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")
        self.project = mixer.blend("projects.Project")

    def test_match_expected_view(self):
        url = resolve("/projects/1/update/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request, id=self.project.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)

    def test_update_project(self):
        data = {
            "name": "test",
            "client": self.project.client.id,
            "start_date": "2018-01-01",
            "payment_type": Project.DAILY_RATE,
            "currency": Project.USD,
            "rate": 20,
        }
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request, id=self.project.id)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse(
            "projects:project-detail", kwargs={"id": self.project.id}
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.payment_type, Project.DAILY_RATE)
        self.assertEqual(redirect_url, response["location"])

    def test_update_project_missing_fields(self):
        data = {"name": "test"}
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request, id=self.project.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data["form"].errors) > 0)


class ProjectListViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ProjectListView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")

    def test_match_expected_view(self):
        url = resolve("/projects/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        mixer.cycle(5).blend("projects.Project")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("projects", response.context_data)
        self.assertIn("filter", response.context_data)
        self.assertEqual(response.context_data["projects"].count(), 5)


class ProjectDetailViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ProjectDetailView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")
        self.project = mixer.blend("projects.Project")

    def test_match_expected_view(self):
        url = resolve("/projects/1/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request, id=self.project.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("project", response.context_data)


class ExpenseCreateViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ExpenseCreateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")

    def test_match_expected_view(self):
        url = resolve("/expenses/create/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)

    def test_create_expense(self):
        project = mixer.blend("projects.Project")
        data = {
            "name": "test",
            "project": project.id,
            "date": "2018-01-01",
            "amount": 10.00,
        }
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse("projects:expense-list"), response["location"])

    def test_create_expense_missing_fields(self):
        data = {"name": "test"}
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data["form"].errors) > 0)


class ExpenseUpdateViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ExpenseUpdateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")
        self.expense = mixer.blend("projects.Expense")

    def test_match_expected_view(self):
        url = resolve("/expenses/1/update/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request, id=self.expense.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)

    def test_update_expense(self):
        data = {
            "name": "another name",
            "project": self.expense.project.id,
            "date": "2018-01-01",
            "amount": 20,
        }
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request, id=self.expense.id)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse(
            "projects:expense-detail", kwargs={"id": self.expense.id}
        )
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.name, "another name")
        self.assertEqual(redirect_url, response["location"])

    def test_update_expense_missing_fields(self):
        data = {"name": "test"}
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request, id=self.expense.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data["form"].errors) > 0)


class ExpenseListViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ExpenseListView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")

    def test_match_expected_view(self):
        url = resolve("/expenses/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        mixer.cycle(5).blend("projects.Expense")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("expenses", response.context_data)
        self.assertIn("filter", response.context_data)
        self.assertEqual(response.context_data["expenses"].count(), 5)


class ExpenseDetailViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ExpenseDetailView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")
        self.expense = mixer.blend("projects.Expense")

    def test_match_expected_view(self):
        url = resolve("/expenses/1/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request, id=self.expense.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("expense", response.context_data)


class ProjectCreateInvoiceViewTestCase(TestCase):
    def setUp(self):
        self.view = views.ProjectCreateInvoiceView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")
        self.project = mixer.blend("projects.Project")

    def test_match_expected_view(self):
        url = resolve("/projects/1/create-invoice/flat/")
        self.assertEqual(url.func.__name__, self.view.__name__)
        url = resolve("/projects/1/create-invoice/rate/")
        self.assertEqual(url.func.__name__, self.view.__name__)
        url = resolve("/projects/1/create-invoice/percentage/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_flat_form(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request, id=self.project.id, type="flat")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)
        self.assertIsInstance(
            response.context_data["form"], forms.CreateInvoiceFlatForm
        )

    def test_load_rate_form(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request, id=self.project.id, type="rate")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)
        self.assertIsInstance(
            response.context_data["form"], forms.CreateInvoiceRateForm
        )

    def test_load_percentage_form(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request, id=self.project.id, type="percentage")
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)
        self.assertIsInstance(
            response.context_data["form"], forms.CreateInvoicePercentageForm
        )

    def test_create_invoice_flat(self):
        request = self.factory.post("/", {"description": "test", "amount": 10})
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        invoice = self.project.invoices.last()
        self.assertIsNone(invoice)
        response = self.view(request, id=self.project.id, type="flat")
        self.assertEqual(response.status_code, 302)
        invoice = self.project.invoices.last()
        self.assertIsNotNone(invoice)
        self.assertEqual(
            response["location"],
            reverse("invoices:invoice-detail", kwargs={"id": invoice.id}),
        )

    def test_create_invoice_rate(self):
        request = self.factory.post(
            "/", {"description": "test", "rate": 10, "units": 10}
        )
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        invoice = self.project.invoices.last()
        self.assertIsNone(invoice)
        response = self.view(request, id=self.project.id, type="rate")
        self.assertEqual(response.status_code, 302)
        invoice = self.project.invoices.last()
        self.assertIsNotNone(invoice)
        self.assertEqual(
            response["location"],
            reverse("invoices:invoice-detail", kwargs={"id": invoice.id}),
        )

    def test_create_invoice_percentage(self):
        request = self.factory.post("/", {"description": "test", "percentage": 10})
        request.user = self.user
        request.session = {}
        request._messages = FallbackStorage(request)
        invoice = self.project.invoices.last()
        self.assertIsNone(invoice)
        response = self.view(request, id=self.project.id, type="percentage")
        self.assertEqual(response.status_code, 302)
        invoice = self.project.invoices.last()
        self.assertIsNotNone(invoice)
        self.assertEqual(
            response["location"],
            reverse("invoices:invoice-detail", kwargs={"id": invoice.id}),
        )


class TimesheetCreateViewTestCase(TestCase):
    def setUp(self):
        self.view = views.TimesheetCreateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")

    def test_match_expected_view(self):
        url = resolve("/timesheets/create/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)

    def test_create_timesheet(self):
        project = mixer.blend("projects.Project")
        data = {
            "label": "test",
            "project": project.id,
            "date_start": "2018-01-01",
            "date_end": "2018-01-01",
        }
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse("projects:timesheet-list"), response["location"])

    def test_create_timesheet_missing_fields(self):
        data = {"label": "test"}
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data["form"].errors) > 0)


class TimesheetUpdateViewTestCase(TestCase):
    def setUp(self):
        self.view = views.TimesheetUpdateView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")
        self.timesheet = mixer.blend(
            "projects.Timesheet", project=mixer.blend("projects.Project")
        )

    def test_match_expected_view(self):
        url = resolve("/timesheets/1/update/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request, id=self.timesheet.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context_data)

    def test_update_timesheet(self):
        data = {
            "label": "another label",
            "date_start": "2018-01-01",
            "date_end": "2018-01-01",
            "project": self.timesheet.project.id,
        }
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request, id=self.timesheet.id)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse(
            "projects:timesheet-detail", kwargs={"id": self.timesheet.id}
        )
        self.timesheet.refresh_from_db()
        self.assertEqual(self.timesheet.label, "another label")
        self.assertEqual(redirect_url, response["location"])

    def test_update_timesheet_missing_fields(self):
        data = {"label": "test"}
        request = self.factory.post("/", data=data)
        request.user = self.user
        response = self.view(request, id=self.timesheet.id)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context_data["form"].errors) > 0)


class TimesheetListViewTestCase(TestCase):
    def setUp(self):
        self.view = views.TimesheetListView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")

    def test_match_expected_view(self):
        url = resolve("/timesheets/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        mixer.cycle(5).blend("projects.Timesheet")
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("timesheets", response.context_data)
        self.assertIn("filter", response.context_data)
        self.assertEqual(response.context_data["timesheets"].count(), 5)

    def test_valid_assign_project_form(self):
        mixer.cycle(5).blend("projects.Timesheet", project=None)
        ids = Timesheet.objects.values_list("id", flat=True)
        project = mixer.blend("projects.Project")
        request = self.factory.post(
            "/", {"project": project.id, "timesheets": ",".join(map(str, ids))}
        )
        request.session = {}
        request._messages = FallbackStorage(request)
        request.user = self.user
        self.assertEqual(Timesheet.objects.filter(project=None).count(), 5)
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        expected_url = reverse("projects:timesheet-list")
        self.assertEqual(response["location"], expected_url)
        self.assertEqual(Timesheet.objects.filter(project=None).count(), 0)

    def test_invalid_assign_project_form(self):
        mixer.cycle(5).blend("projects.Timesheet", project=None)
        ids = Timesheet.objects.values_list("id", flat=True)
        request = self.factory.post(
            "/", {"project": None, "timesheets": ",".join(map(str, ids))}
        )
        request.session = {}
        request._messages = FallbackStorage(request)
        request.user = self.user
        self.assertEqual(Timesheet.objects.filter(project=None).count(), 5)
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        expected_url = reverse("projects:timesheet-list")
        self.assertEqual(response["location"], expected_url)
        self.assertEqual(Timesheet.objects.filter(project=None).count(), 5)


class TimesheetDetailViewTestCase(TestCase):
    def setUp(self):
        self.view = views.TimesheetDetailView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")
        self.timesheet = mixer.blend("projects.Timesheet")

    def test_match_expected_view(self):
        url = resolve("/timesheets/1/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_load_sucessful(self):
        request = self.factory.get("/")
        request.user = self.user
        response = self.view(request, id=self.timesheet.id)
        self.assertEqual(response.status_code, 200)
        self.assertIn("timesheet", response.context_data)


class TimesheetClockInViewTestCase(TestCase):
    def setUp(self):
        self.view = views.TimesheetClockInView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")

    def test_match_expected_view(self):
        url = resolve("/timesheets/clock-in/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_redirect_to_referer(self):
        request = self.factory.get("/")
        request.user = self.user
        expected_url = "redirect"
        request.META["HTTP_REFERER"] = expected_url
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], expected_url)

    def test_redirect_to_home_when_there_is_not_a_referer(self):
        request = self.factory.get("/")
        request.user = self.user
        expected_url = reverse("home")
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], expected_url)


class TimesheetClockOutViewTestCase(TestCase):
    def setUp(self):
        self.view = views.TimesheetClockOutView.as_view()
        self.factory = RequestFactory()
        self.user = mixer.blend("users.User")
        mixer.blend("projects.Timesheet", is_active=True)

    def test_match_expected_view(self):
        url = resolve("/timesheets/clock-out/")
        self.assertEqual(url.func.__name__, self.view.__name__)

    def test_redirect_to_referer(self):
        request = self.factory.get("/")
        request.user = self.user
        expected_url = "redirect"
        request.META["HTTP_REFERER"] = expected_url
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], expected_url)

    def test_redirect_to_home_when_there_is_not_a_referer(self):
        request = self.factory.get("/")
        request.user = self.user
        expected_url = reverse("home")
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], expected_url)
