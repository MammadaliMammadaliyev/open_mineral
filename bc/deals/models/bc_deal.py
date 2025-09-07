import uuid

from django.db import models
from django.contrib.auth import get_user_model


class BusinessConfirmationDeal(models.Model):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (SUBMITTED, "Submitted"),
        (PROCESSING, "Processing"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business_confirmation_deals",
    )

    new_business_confirmation = models.OneToOneField(
        "NewBusinessConfirmation", 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="business_confirmation_deal",
    )
    commercial_terms = models.OneToOneField(
        "CommercialTerms", 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="business_confirmation_deal",
    )

    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default=DRAFT
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the business confirmation deal was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the business confirmation deal was last updated",
    )

    class Meta:
        verbose_name = "Business Confirmation Deal"
        verbose_name_plural = "Business Confirmation Deals"

    def __str__(self):
        return f"Business Confirmation Deal {self.id}"