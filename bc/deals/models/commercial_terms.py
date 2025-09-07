from django.db import models
from django.core.validators import MinValueValidator


class AdditionalClause(models.Model):
    clause = models.TextField(
        null=True,
        blank=True,
        help_text="Additional clause"
    )
    display_order = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Order for display"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="Date and time when the additional clause was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        help_text="Date and time when the additional clause was last updated",
    )

    class Meta:
        ordering = ["display_order"]
        verbose_name = "Additional Clause"
        verbose_name_plural = "Additional Clauses"

    def __str__(self):
        return self.clause


class CommercialTerms(models.Model):
    # Delivery & Shipment
    delivery_term = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Delivery term (e.g., DAP, FOB, CIF)"
    )
    delivery_point = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
        help_text="Delivery point location"
    )
    packaging = models.CharField(
        max_length=100, 
        null=True,
        blank=True,
        help_text="Packaging type (e.g., Big Bags, Bulk)"
    )
    transport_mode = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Transport mode (e.g., Rail, Ship, Truck)"
    )
    inland_freight_buyer = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        help_text="Inland freight borne by buyer"
    )
    shipment_start_date = models.DateField(
        null=True,
        blank=True,
        help_text="Shipment period start date"
    )
    shipment_end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Shipment period end date"
    )
    shipment_evenly_distributed = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        help_text="Shipments distributed evenly across period"
    )

    # Pricing & Charges
    treatment_charge = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Treatment charge amount"
    )
    treatment_charge_unit = models.CharField(
        max_length=10, 
        default="dmt",
        null=True,
        blank=True,
        help_text="Treatment charge unit"
    )
    refining_charge = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Refining charge amount"
    )
    refining_charge_unit = models.CharField(
        max_length=10, 
        default="toz",
        null=True,
        blank=True,
        help_text="Refining charge unit"
    )

    # Assay / Quality
    assay_file = models.FileField(
        upload_to="assay_files/%Y/%m/%d/", 
        blank=True, 
        null=True,
        help_text="Uploaded assay file"
    )
    china_import_compliant = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        help_text="Material complies with China import standards"
    )
    # there is another boolean field for the buyer in Figma, but it's not visible in the design

    # Additional Terms
    clauses = models.JSONField(
        default=list, 
        null=True,
        blank=True,
        help_text="List of additional clause strings"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="Date and time when the commercial terms were created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        help_text="Date and time when the commercial terms were last updated",
    )

    class Meta:
        verbose_name = "Commercial Terms"
        verbose_name_plural = "Commercial Terms"

    def __str__(self):
        return f"Commercial Terms for Business Confirmation {self.id}"
    