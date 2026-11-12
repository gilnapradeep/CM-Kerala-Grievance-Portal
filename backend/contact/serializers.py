
from rest_framework import serializers
from .models import ContactEnquiry


class ContactEnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactEnquiry
        fields = [
            "id",
            "name",
            "email",
            "subject",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value.strip()

    def validate_subject(self, value):
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be empty.")
        return value.strip()

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        return value.strip()
