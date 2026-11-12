
from rest_framework import serializers

from .models import (
    Grievance,
    DepartmentAssignment,
    ActionTakenReport,
)


class DepartmentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentAssignment
        fields = [
            'id',
            'grievance',
            'department',
            'assigned_by',
            'assigned_officer',
            'remarks',
            'assigned_at',
            'is_active',
        ]
        read_only_fields = [
            'id',
            'assigned_by',
            'assigned_at',
            'is_active',
        ]


class ActionTakenReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionTakenReport
        fields = [
            'id',
            'grievance',
            'officer',
            'investigation_details',
            'action_taken',
            'resolution_details',
            'submitted_to_cmo',
            'submitted_at',
        ]
        read_only_fields = [
            'id',
            'grievance',
            'officer',
            'submitted_to_cmo',
            'submitted_at',
        ]


class AdminGrievanceSerializer(serializers.ModelSerializer):
    citizen_name = serializers.CharField(
        source='citizen.get_full_name',
        read_only=True
    )
    department_name = serializers.CharField(
        source='assigned_department.name',
        read_only=True
    )
    officer_name = serializers.CharField(
        source='assigned_officer.username',
        read_only=True
    )

    class Meta:
        model = Grievance
        fields = '__all__'
        read_only_fields = [
            'reference_number',
            'citizen',
            'created_at',
            'updated_at',
        ]
