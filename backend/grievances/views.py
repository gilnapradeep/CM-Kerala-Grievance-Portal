
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from accounts.models import User
from accounts.permissions import IsCMOAdmin, IsDepartmentOfficer
from departments.models import Department

from .models import (
    Grievance,
    GrievanceHistory,
    DepartmentAssignment,
    ActionTakenReport,
    CitizenFeedback,
    Grievance
)

from .serializers import GrievanceSerializer
from .admin_serializers import (
    AdminGrievanceSerializer,
    ActionTakenReportSerializer,
)


# ============================================================
# COMMON HELPER
# ============================================================

def add_internal_remarks(grievance, user, remarks):
    if not remarks:
        return

    entry = (
        f"[{timezone.now().isoformat()}] "
        f"{user.username}: {remarks}"
    )

    grievance.internal_remarks = (
        f"{grievance.internal_remarks}\n{entry}"
    ).strip()


def record_history(grievance, old_status, new_status, user, remarks):
    GrievanceHistory.objects.create(
        grievance=grievance,
        old_status=old_status,
        new_status=new_status,
        changed_by=user,
        remarks=remarks or "",
        is_internal=True,
    )


# ============================================================
# 1. CITIZEN APIs
# ============================================================

class GrievanceListCreateView(generics.ListCreateAPIView):
    serializer_class = GrievanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Grievance.objects.filter(
            citizen=self.request.user
        ).order_by("-created_at")


class GrievanceDetailView(generics.RetrieveAPIView):
    serializer_class = GrievanceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference_number"

    def get_queryset(self):
        return Grievance.objects.filter(
            citizen=self.request.user
        )


class TrackGrievanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reference_number):
        grievance = get_object_or_404(
            Grievance,
            reference_number=reference_number,
            citizen=request.user,
        )

        serializer = GrievanceSerializer(
            grievance,
            context={"request": request},
        )

        return Response(serializer.data)


# ============================================================
# 2. CMO ADMINISTRATOR APIs
# ============================================================

class CMOGrievanceListView(ListAPIView):
    serializer_class = AdminGrievanceSerializer
    permission_classes = [IsAuthenticated, IsCMOAdmin]

    def get_queryset(self):
        queryset = Grievance.objects.select_related(
            "citizen",
            "assigned_department",
            "assigned_officer",
        ).all()

        for field in ["district", "category", "priority", "status"]:
            value = self.request.query_params.get(field)

            if value:
                queryset = queryset.filter(**{field: value})

        return queryset.order_by("-created_at")


class CMODashboardStatsView(APIView):
    permission_classes = [IsAuthenticated, IsCMOAdmin]

    def get(self, request):
        grievances = Grievance.objects.all()

        total = grievances.count()
        resolved = grievances.filter(status="RESOLVED").count()
        pending = grievances.exclude(status="RESOLVED").count()

        overdue = grievances.filter(
            due_at__lt=timezone.now()
        ).exclude(status="RESOLVED").count()

        district_stats = list(
            grievances.values("district")
            .annotate(total=Count("id"))
            .order_by("district")
        )

        department_stats = list(
            grievances.filter(
                assigned_department__isnull=False
            )
            .values("assigned_department__name")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        # Include both names for compatibility with the React frontend.
        return Response({
            "total": total,
            "pending": pending,
            "resolved": resolved,
            "overdue": overdue,

            "total_grievances": total,
            "pending_grievances": pending,
            "resolved_grievances": resolved,
            "overdue_grievances": overdue,

            "district_statistics": district_stats,
            "department_statistics": department_stats,
        })


class AssignGrievanceView(APIView):
    permission_classes = [IsAuthenticated, IsCMOAdmin]

    @transaction.atomic
    def post(self, request, reference_number):
        grievance = Grievance.objects.select_for_update().filter(
            reference_number=reference_number
        ).first()

        if not grievance:
            return Response(
                {"error": "Grievance not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        department_id = request.data.get("department_id")
        officer_id = request.data.get("officer_id")
        remarks = request.data.get("remarks", "")

        if not department_id:
            return Response(
                {"error": "department_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        department = Department.objects.filter(
            id=department_id,
            is_active=True,
        ).first()

        if not department:
            return Response(
                {"error": "Active department not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        officer = None

        if officer_id:
            officer = User.objects.filter(
                id=officer_id,
                role="OFFICER",
                is_active=True,
            ).first()

            if not officer:
                return Response(
                    {"error": "Valid department officer not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Deactivate previous assignments.
        DepartmentAssignment.objects.filter(
            grievance=grievance,
            is_active=True,
        ).update(is_active=False)

        assignment = DepartmentAssignment.objects.create(
            grievance=grievance,
            department=department,
            assigned_by=request.user,
            assigned_officer=officer,
            remarks=remarks,
        )

        old_status = grievance.status

        grievance.assigned_department = department
        grievance.assigned_officer = officer

        if grievance.status == "SUBMITTED":
            grievance.status = "UNDER_REVIEW"

        add_internal_remarks(grievance, request.user, remarks)
        grievance.save()

        if old_status != grievance.status:
            record_history(
                grievance,
                old_status,
                grievance.status,
                request.user,
                "Grievance assigned to department. " + remarks,
            )

        return Response({
            "message": "Grievance assigned successfully.",
            "assignment_id": assignment.id,
            "reference_number": grievance.reference_number,
            "department": department.name,
            "officer": officer.username if officer else None,
            "status": grievance.status,
        }, status=status.HTTP_201_CREATED)


class CMOStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsCMOAdmin]

    @transaction.atomic
    def patch(self, request, reference_number):
        grievance = Grievance.objects.select_for_update().filter(
            reference_number=reference_number
        ).first()

        if not grievance:
            return Response(
                {"error": "Grievance not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_status = request.data.get("status")
        remarks = request.data.get("remarks", "")
        priority = request.data.get("priority")

        valid_statuses = dict(Grievance.STATUS_CHOICES)
        valid_priorities = dict(Grievance.PRIORITY_CHOICES)

        if new_status and new_status not in valid_statuses:
            return Response(
                {"error": "Invalid grievance status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if priority and priority not in valid_priorities:
            return Response(
                {"error": "Invalid priority."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_status = grievance.status

        if new_status:
            grievance.status = new_status

        if priority:
            grievance.priority = priority

        add_internal_remarks(grievance, request.user, remarks)
        grievance.save()

        if old_status != grievance.status:
            record_history(
                grievance,
                old_status,
                grievance.status,
                request.user,
                remarks,
            )

        return Response({
            "message": "Grievance updated successfully.",
            "reference_number": grievance.reference_number,
            "status": grievance.status,
            "priority": grievance.priority,
        })


class CMOActionReportsView(ListAPIView):
    serializer_class = ActionTakenReportSerializer
    permission_classes = [IsAuthenticated, IsCMOAdmin]

    def get_queryset(self):
        return ActionTakenReport.objects.filter(
            submitted_to_cmo=True
        ).select_related(
            "grievance",
            "officer",
        ).order_by("-submitted_at")


class CMOReviewActionReportView(APIView):
    """
    CMO approves or rejects an officer's submitted action report.

    Approval resolves the grievance.
    Rejection returns it to IN_PROGRESS.
    """

    permission_classes = [IsAuthenticated, IsCMOAdmin]

    @transaction.atomic
    def post(self, request, report_id):
        report = get_object_or_404(
            ActionTakenReport.objects.select_related("grievance"),
            id=report_id,
            submitted_to_cmo=True,
        )

        grievance = Grievance.objects.select_for_update().get(
            id=report.grievance_id
        )

        approved = request.data.get("approved")
        remarks = request.data.get("remarks", "")

        if not isinstance(approved, bool):
            return Response(
                {"error": "approved must be true or false."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_status = grievance.status

        if approved:
            grievance.status = "RESOLVED"
            decision = "CMO approved the officer action report."
        else:
            grievance.status = "IN_PROGRESS"
            decision = "CMO rejected the officer action report. Further action required."

        if remarks:
            decision += " Remarks: " + remarks

        add_internal_remarks(grievance, request.user, decision)
        grievance.save()

        record_history(
            grievance,
            old_status,
            grievance.status,
            request.user,
            decision,
        )

        return Response({
            "message": (
                "Action report approved."
                if approved
                else "Action report rejected and returned for further action."
            ),
            "report_id": report.id,
            "reference_number": grievance.reference_number,
            "approved": approved,
            "status": grievance.status,
        })


# ============================================================
# 3. DEPARTMENT OFFICER APIs
# ============================================================

class OfficerGrievanceListView(ListAPIView):
    serializer_class = AdminGrievanceSerializer
    permission_classes = [IsAuthenticated, IsDepartmentOfficer]

    def get_queryset(self):
        return Grievance.objects.filter(
            assigned_officer=self.request.user
        ).select_related(
            "citizen",
            "assigned_department",
            "assigned_officer",
        ).order_by("-created_at")


class OfficerStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsDepartmentOfficer]

    @transaction.atomic
    def patch(self, request, reference_number):
        grievance = Grievance.objects.select_for_update().filter(
            reference_number=reference_number,
            assigned_officer=request.user,
        ).first()

        if not grievance:
            return Response(
                {"error": "Assigned grievance not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_status = request.data.get("status")
        remarks = request.data.get("remarks", "")

        allowed_statuses = ["UNDER_REVIEW", "IN_PROGRESS"]

        if new_status not in allowed_statuses:
            return Response(
                {"error": "Invalid officer status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_status = grievance.status
        grievance.status = new_status

        add_internal_remarks(grievance, request.user, remarks)
        grievance.save()

        if old_status != new_status:
            record_history(
                grievance,
                old_status,
                new_status,
                request.user,
                remarks,
            )

        return Response({
            "message": "Grievance status updated successfully.",
            "reference_number": grievance.reference_number,
            "status": grievance.status,
        })


class SubmitActionReportView(APIView):
    permission_classes = [IsAuthenticated, IsDepartmentOfficer]

    @transaction.atomic
    def post(self, request, reference_number):
        grievance = Grievance.objects.select_for_update().filter(
            reference_number=reference_number,
            assigned_officer=request.user,
        ).first()

        if not grievance:
            return Response(
                {"error": "Assigned grievance not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if grievance.status == "RESOLVED":
            return Response(
                {"error": "Grievance is already resolved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ActionTakenReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report = serializer.save(
            grievance=grievance,
            officer=request.user,
            submitted_to_cmo=True,
        )

        add_internal_remarks(
            grievance,
            request.user,
            "Officer submitted an action-taken report for CMO review.",
        )
        grievance.save()

        return Response({
            "message": "Action-taken report submitted to CMO.",
            "report": ActionTakenReportSerializer(report).data,
        }, status=status.HTTP_201_CREATED)


class CitizenFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reference_number):
        # Only the owner of the grievance can submit feedback.
        grievance = get_object_or_404(
            Grievance,
            reference_number=reference_number,
            citizen=request.user,
        )

        # Feedback is allowed only after resolution.
        if grievance.status != "RESOLVED":
            return Response(
                {"error": "Feedback can only be submitted after the grievance is resolved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Enforce one feedback submission per grievance.
        if CitizenFeedback.objects.filter(grievance=grievance).exists():
            return Response(
                {"error": "Feedback has already been submitted for this grievance."},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            rating = int(request.data.get("rating"))
        except (TypeError, ValueError):
            return Response(
                {"error": "Rating must be an integer between 1 and 5."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if rating < 1 or rating > 5:
            return Response(
                {"error": "Rating must be between 1 and 5."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comments = request.data.get("comments", "")

        feedback = CitizenFeedback.objects.create(
            grievance=grievance,
            rating=rating,
            comments=comments,
        )

        return Response(
            {
                "message": "Feedback submitted successfully.",
                "feedback": {
                    "id": feedback.id,
                    "reference_number": grievance.reference_number,
                    "rating": feedback.rating,
                    "comments": feedback.comments,
                    "created_at": feedback.created_at,
                },
            },
            status=status.HTTP_201_CREATED,
        )