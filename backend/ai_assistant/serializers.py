
from rest_framework import serializers


class AIAnalysisSerializer(serializers.Serializer):
    reference_number = serializers.CharField()
    suggested_department = serializers.CharField(
        allow_null=True
    )
    suggested_category = serializers.CharField()
    suggested_priority = serializers.CharField()
    summary = serializers.CharField()
    reasoning = serializers.CharField()
    similar_grievances = serializers.ListField()
    duplicate_candidates_found = serializers.BooleanField()


class AIReviewSerializer(serializers.Serializer):
    approved = serializers.BooleanField()
