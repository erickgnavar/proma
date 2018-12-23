from django.urls import path, re_path

from . import views

app_name = "projects"


urlpatterns = [
    path("projects/", views.ProjectListView.as_view(), name="project-list"),
    path("projects/create/", views.ProjectCreateView.as_view(), name="project-create"),
    path(
        "projects/<int:id>/", views.ProjectDetailView.as_view(), name="project-detail"
    ),
    path(
        "projects/<int:id>/update/",
        views.ProjectUpdateView.as_view(),
        name="project-update",
    ),
    re_path(
        r"projects/(?P<id>\d+)/create-invoice/(?P<type>(flat|rate|percentage))/",
        views.ProjectCreateInvoiceView.as_view(),
        name="project-create-invoice",
    ),
    path("expenses/", views.ExpenseListView.as_view(), name="expense-list"),
    path("expenses/create/", views.ExpenseCreateView.as_view(), name="expense-create"),
    path(
        "expenses/<int:id>/", views.ExpenseDetailView.as_view(), name="expense-detail"
    ),
    path(
        "expenses/<int:id>/update/",
        views.ExpenseUpdateView.as_view(),
        name="expense-update",
    ),
    path("timesheets/", views.TimesheetListView.as_view(), name="timesheet-list"),
    path(
        "timesheets/create/",
        views.TimesheetCreateView.as_view(),
        name="timesheet-create",
    ),
    path(
        "timesheets/<int:id>/",
        views.TimesheetDetailView.as_view(),
        name="timesheet-detail",
    ),
    path(
        "timesheets/<int:id>/update/",
        views.TimesheetUpdateView.as_view(),
        name="timesheet-update",
    ),
    path(
        "timesheets/clock-in/",
        views.TimesheetClockInView.as_view(),
        name="timesheet-clock-in",
    ),
    path(
        "timesheets/clock-out/",
        views.TimesheetClockOutView.as_view(),
        name="timesheet-clock-out",
    ),
]
