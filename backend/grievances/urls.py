
from django.urls import path

from .views import (
    GrievanceListCreateView,
    GrievanceDetailView,
    TrackGrievanceView,
    CMOGrievanceListView,
    CMODashboardStatsView,
    AssignGrievanceView,
    CMOStatusUpdateView,
    OfficerGrievanceListView,
    OfficerStatusUpdateView,
    SubmitActionReportView,
    CMOActionReportsView,
    CMOReviewActionReportView,
    CitizenFeedbackView,
)

urlpatterns = [
    # Citizen APIs
    path('', GrievanceListCreateView.as_view(), name='grievance-list-create'),
    path('track/<str:reference_number>/', TrackGrievanceView.as_view(), name='track-grievance'),
    path('<str:reference_number>/', GrievanceDetailView.as_view(), name='grievance-detail'),

    # CMO APIs
    path('cmo/list/', CMOGrievanceListView.as_view(), name='cmo-grievance-list'),
    path('cmo/stats/', CMODashboardStatsView.as_view(), name='cmo-dashboard-stats'),
    path('cmo/<str:reference_number>/assign/', AssignGrievanceView.as_view(), name='assign-grievance'),
    path('cmo/<str:reference_number>/status/', CMOStatusUpdateView.as_view(), name='cmo-status-update'),
    path('cmo/action-reports/', CMOActionReportsView.as_view(), name='cmo-action-reports'),
    path(
        'cmo/action-reports/<int:report_id>/review/',
        CMOReviewActionReportView.as_view(),
        name='cmo-review-action-report',
    ),

    # Department Officer APIs
    path('officer/list/', OfficerGrievanceListView.as_view(), name='officer-grievance-list'),
    path('officer/<str:reference_number>/status/', OfficerStatusUpdateView.as_view(), name='officer-status-update'),
    path('officer/<str:reference_number>/action-report/', SubmitActionReportView.as_view(), name='submit-action-report'),
    path(
    '<str:reference_number>/feedback/',
    CitizenFeedbackView.as_view(),
    name='citizen-feedback',
    ),
]
