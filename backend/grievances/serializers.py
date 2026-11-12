
from rest_framework import serializers
from .models import Grievance, Attachment, GrievanceHistory


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'original_name', 'uploaded_at']
        read_only_fields = ['id', 'original_name', 'uploaded_at']


class GrievanceHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.StringRelatedField()

    class Meta:
        model = GrievanceHistory
        fields = [
            'old_status',
            'new_status',
            'changed_by',
            'remarks',
            'created_at'
        ]


class GrievanceSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    history = serializers.SerializerMethodField()

    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Grievance
        fields = [
            'id',
            'reference_number',
            'district',
            'category',
            'subject',
            'description',
            'status',
            'priority',
            'created_at',
            'updated_at',
            'attachments',
            'uploaded_files',
            'history'
        ]
        read_only_fields = [
            'id',
            'reference_number',
            'status',
            'priority',
            'created_at',
            'updated_at'
        ]

    def validate_uploaded_files(self, files):
        allowed_extensions = {
            '.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'
        }

        for file in files:
            extension = '.' + file.name.rsplit('.', 1)[-1].lower()

            if extension not in allowed_extensions:
                raise serializers.ValidationError(
                    f"Unsupported file type: {file.name}"
                )

            if file.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    f"{file.name} exceeds the 5 MB limit."
                )

        return files

    def get_history(self, obj):
        history = obj.history.filter(
            is_internal=False
        ).order_by('created_at')

        return GrievanceHistorySerializer(
            history,
            many=True
        ).data

    def create(self, validated_data):
        files = validated_data.pop('uploaded_files', [])

        request = self.context['request']

        grievance = Grievance.objects.create(
            citizen=request.user,
            **validated_data
        )

        # Record the initial submission in the history.
        GrievanceHistory.objects.create(
            grievance=grievance,
            old_status='',
            new_status=grievance.status,
            changed_by=request.user,
            remarks='Grievance submitted by citizen.',
            is_internal=False
        )

        # Save supporting documents.
        for file in files:
            Attachment.objects.create(
                grievance=grievance,
                file=file,
                original_name=file.name
            )

        return grievance
