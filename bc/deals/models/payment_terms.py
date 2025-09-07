from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PaymentTerms(models.Model):
    # Payment Stages
    prepayment_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text="Prepayment percentage"
    )
    prepayment_trigger = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Prepayment trigger event"
    )
    provisional_payment_terms = models.TextField(
        null=True,
        blank=True,
        help_text="Provisional payment terms description"
    )
    final_payment_terms = models.TextField(
        null=True,
        blank=True,
        help_text="Final payment terms description"
    )

    # Payment Method & Terms
    payment_method = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Payment method (e.g., T/T, L/C)"
    )
    currency = models.CharField(
        max_length=10,
        default="USD",
        null=True,
        blank=True,
        help_text="Payment currency"
    )
    triggering_event = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="General triggering event"
    )
    reference_document = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Reference document type"
    )

    # WSMD & Surveyor
    final_determination_location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Final determination location"
    )
    buyer_cost_share_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text="Buyer cost share percentage"
    )
    seller_cost_share_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text="Seller cost share percentage"
    )
    nominated_by = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Surveyor nominated by"
    )
    agreed_by = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Surveyor agreed by"
    )
    surveyor_notes = models.TextField(
        blank=True,
        help_text="Additional surveyor notes"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the payment terms were created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the payment terms were last updated",
    )
    
    class Meta:
        verbose_name = "Payment Terms"
        verbose_name_plural = "Payment Terms"
    
    def __str__(self):
        return f"Payment Terms {self.id} for Deal"
    