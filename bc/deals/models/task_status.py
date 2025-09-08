import uuid
from django.db import models
from django.contrib.auth import get_user_model


class TaskStatus(models.Model):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
    ]

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    task_id = models.CharField(
        max_length=255,
        unique=True,
        help_text="Celery task ID"
    )
    deal = models.ForeignKey(
        "BusinessConfirmationDeal",
        on_delete=models.CASCADE,
        related_name="task_statuses"
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    message = models.TextField(
        blank=True,
        null=True,
        help_text="Status message or error details"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the task was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the task was last updated"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when the task was completed"
    )

    class Meta:
        verbose_name = "Task Status"
        verbose_name_plural = "Task Statuses"
        ordering = ['-created_at']

    def __str__(self):
        return f"Task {self.task_id} - {self.status}"
