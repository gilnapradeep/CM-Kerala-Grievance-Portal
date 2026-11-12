
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsCMOAdmin
from grievances.models import Grievance, GrievanceHistory
from departments.models import Department

from .services import analyze_grievance
from .serializers import AIReviewSerializer


class AIGrievanceAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reference_number):

        grievance = get_object_or_404(
            Grievance,
            reference_number=reference_number
        )

        if (
            request.user.role != "CMO_ADMIN"
            and grievance.citizen_id != request.user.id
        ):
            return Response(
                {"error": "You cannot analyze this grievance."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            result = analyze_grievance(grievance)

            department = None

            if result["suggested_department"]:
                department = Department.objects.filter(
                    name=result["suggested_department"],
                    is_active=True
                ).first()

            grievance.ai_suggested_department = department
            grievance.ai_suggested_category = (
                result["suggested_category"]
            )
            grievance.ai_suggested_priority = (
                result["suggested_priority"]
            )
            grievance.ai_summary = result["summary"]
            grievance.ai_analysis = result
            grievance.ai_reviewed = False

            grievance.save()

            return Response({
                "message": "AI analysis completed. Suggestions require human review.",
                "reference_number": grievance.reference_number,
                "analysis": result,
                "reviewed": False,
            })

        except Exception as error:
            return Response(
                {
                    "error": "AI analysis failed.",
                    "details": str(error),
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class AIGrievanceReviewView(APIView):
    permission_classes = [IsAuthenticated, IsCMOAdmin]

    def post(self, request, reference_number):

        grievance = get_object_or_404(
            Grievance,
            reference_number=reference_number
        )

        serializer = AIReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        approved = serializer.validated_data["approved"]

        if approved:
            if grievance.ai_suggested_category:
                grievance.category = (
                    grievance.ai_suggested_category
                )

            if grievance.ai_suggested_priority:
                grievance.priority = (
                    grievance.ai_suggested_priority
                )

            if grievance.ai_suggested_department:
                grievance.assigned_department = (
                    grievance.ai_suggested_department
                )

        grievance.ai_reviewed = True
        grievance.save()

        GrievanceHistory.objects.create(
            grievance=grievance,
            old_status=grievance.status,
            new_status=grievance.status,
            changed_by=request.user,
            remarks=(
                "CMO approved AI recommendations."
                if approved
                else "CMO reviewed and rejected AI recommendations."
            ),
            is_internal=True
        )

        return Response({
            "message": (
                "AI recommendations approved."
                if approved
                else "AI recommendations rejected."
            ),
            "approved": approved,
            "ai_reviewed": grievance.ai_reviewed,
        })
