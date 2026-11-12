from django.contrib import admin
from .models import (
    Grievance,
    GrievanceHistory,
    DepartmentAssignment,
    Attachment,
    ActionTakenReport,
    CitizenFeedback
)

admin.site.register(Grievance)
admin.site.register(GrievanceHistory)
admin.site.register(DepartmentAssignment)
admin.site.register(Attachment)
admin.site.register(ActionTakenReport)
admin.site.register(CitizenFeedback)