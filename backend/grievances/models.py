
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone


class Grievance(models.Model):

    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('REOPENED', 'Reopened'),
    ]

    CATEGORY_CHOICES = [
        ('INFRASTRUCTURE', 'Infrastructure'),
        ('HEALTHCARE', 'Healthcare'),
        ('EDUCATION', 'Education'),
        ('PUBLIC_SERVICES', 'Public Services'),
        ('WATER', 'Water Supply'),
        ('ELECTRICITY', 'Electricity'),
        ('TRANSPORT', 'Transport'),
        ('SANITATION', 'Sanitation'),
        ('OTHER', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    DISTRICT_CHOICES = [
    ('THIRUVANANTHAPURAM', 'Thiruvananthapuram'),
    ('KOLLAM', 'Kollam'),
    ('PATHANAMTHITTA', 'Pathanamthitta'),
    ('ALAPPUZHA', 'Alappuzha'),
    ('KOTTAYAM', 'Kottayam'),
    ('IDUKKI', 'Idukki'),
    ('ERNAKULAM', 'Ernakulam'),
    ('THRISSUR', 'Thrissur'),
    ('PALAKKAD', 'Palakkad'),
    ('MALAPPURAM', 'Malappuram'),
    ('KOZHIKODE', 'Kozhikode'),
    ('WAYANAD', 'Wayanad'),
    ('KANNUR', 'Kannur'),
    ('KASARAGOD', 'Kasaragod'),
]

    reference_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False
    )

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='grievances'
    )

    district = models.CharField(
        max_length=30,
        choices=DISTRICT_CHOICES
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    subject = models.CharField(max_length=200)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SUBMITTED'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    assigned_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grievances'
    )

    assigned_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_grievances'
    )

    # AI-generated recommendations
    ai_suggested_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_suggested_grievances'
    )

    ai_suggested_category = models.CharField(
        max_length=50,
        blank=True
    )

    ai_suggested_priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        blank=True
    )

    ai_summary = models.TextField(blank=True)

    ai_analysis = models.JSONField(default=dict, blank=True)

    ai_reviewed = models.BooleanField(default=False)

    internal_remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    due_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):

        if not self.reference_number:
            self.reference_number = (
                f"CMK-{timezone.now():%Y%m%d}-"
                f"{uuid.uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference_number

    class Meta:
        ordering = ['-created_at']


class GrievanceHistory(models.Model):

    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name='history'
    )

    old_status = models.CharField(
        max_length=20,
        choices=Grievance.STATUS_CHOICES,
        blank=True
    )

    new_status = models.CharField(
        max_length=20,
        choices=Grievance.STATUS_CHOICES
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    remarks = models.TextField(blank=True)

    is_internal = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class DepartmentAssignment(models.Model):

    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='department_assignments_made'
    )

    assigned_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_assignments_received'
    )

    remarks = models.TextField(blank=True)

    assigned_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)


class Attachment(models.Model):

    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name='attachments'
    )

    file = models.FileField(upload_to='grievances/')

    original_name = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True)


class ActionTakenReport(models.Model):

    grievance = models.ForeignKey(
        Grievance,
        on_delete=models.CASCADE,
        related_name='action_reports'
    )

    officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    investigation_details = models.TextField()

    action_taken = models.TextField()

    resolution_details = models.TextField(blank=True)

    submitted_to_cmo = models.BooleanField(default=False)

    submitted_at = models.DateTimeField(auto_now_add=True)


class CitizenFeedback(models.Model):

    grievance = models.OneToOneField(
        Grievance,
        on_delete=models.CASCADE,
        related_name='feedback'
    )

    rating = models.PositiveSmallIntegerField()

    comments = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.grievance.reference_number} - {self.rating}/5"
