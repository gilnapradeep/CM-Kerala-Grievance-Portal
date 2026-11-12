
from django.urls import path

from .views import (
    AIGrievanceAnalysisView,
    AIGrievanceReviewView,
)

urlpatterns = [
    path(
        "analyze/<str:reference_number>/",
        AIGrievanceAnalysisView.as_view(),
        name="ai-grievance-analysis",
    ),
    path(
        "review/<str:reference_number>/",
        AIGrievanceReviewView.as_view(),
        name="ai-grievance-review",
    ),
]
