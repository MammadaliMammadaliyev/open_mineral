import uuid

from django.db import models
from django.core.validators import MinValueValidator


class NewBusinessConfirmation(models.Model):
    # Buyer & Seller
    seller = models.CharField(
        max_length=255, 
        default="Open Mineral",
        help_text="Seller company name",
    )
    buyer = models.CharField(
        max_length=255,
        default="Company A, John Materials",
        help_text="Buyer company name"
    )

    # Material
    material = models.CharField(
        max_length=255,
        help_text="Material type (e.g., Akzhal, Lead concentrate)"
    )
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Quantity in specified unit"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="Date and time when the deal was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        help_text="Date and time when the deal was last updated",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "New Business Confirmation"
        verbose_name_plural = "New Business Confirmations"

    def __str__(self):
        return f"New Business Confirmation {self.id}: {self.buyer} - {self.material}"
