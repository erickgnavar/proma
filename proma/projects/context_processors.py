from .models import Timesheet


def current_timesheet_data(request):
    active_timesheet = (
        Timesheet.objects.filter(is_active=True).order_by("-created").first()
    )
    return {"active_timesheet": active_timesheet}
