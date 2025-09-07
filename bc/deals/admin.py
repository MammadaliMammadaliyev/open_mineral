from django.contrib import admin
from django.utils.html import format_html

from .models import (DropdownOption, NewBusinessConfirmation, CommercialTerms, 
                     AdditionalClause, PaymentTerms, BusinessConfirmationDeal)


@admin.register(AdditionalClause)
class AdditionalClauseAdmin(admin.ModelAdmin):
    list_display = (
        "short_clause",
        "display_order",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("clause",)
    ordering = ("display_order",)

    fieldsets = (
        ("Clause Details", {
            "fields": ("clause", "display_order"),
            "description": "Manage additional clauses that can be attached to contracts or dropdowns."
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "description": "These fields are automatically maintained by the system.",
        }),
    )
    readonly_fields = ("created_at", "updated_at")

    def short_clause(self, obj):
        """Display shortened version of the clause in list view."""
        if not obj.clause:
            return "-"
        return obj.clause[:70] + ("..." if len(obj.clause) > 70 else "")
    short_clause.short_description = "Clause Preview"


@admin.register(DropdownOption)
class DropdownOptionAdmin(admin.ModelAdmin):
    list_display = (
        "field_name", 
        "formatted_option_values", 
        "display_order",
        "is_active",
        "short_tooltip",
    )
    list_filter = ("field_name", "is_active")
    search_fields = ("field_name", "option_values")
    ordering = ("field_name", "display_order")

    fieldsets = (
        ("General Information", {
            "fields": ("field_name", "option_values", "display_order", "is_active"),
            "description": "Define dropdown options grouped by field (e.g., material, delivery_term)."
        }),
        ("Additional Info", {
            "fields": ("tooltip_text",),
            "description": "Optional tooltip text that will be displayed as an info icon in the UI."
        }),
    )

    def formatted_option_values(self, obj):
        """Nicely display JSON field as key → value pairs."""
        if not obj.option_values:
            return "-"
        if isinstance(obj.option_values, dict):
            items = [f"<li><b>{k}</b>: {v}</li>" for k, v in obj.option_values.items()]
            return format_html("<ul>{}</ul>", format_html("".join(items)))
        return str(obj.option_values)
    formatted_option_values.short_description = "Options"

    def short_tooltip(self, obj):
        """Show a shortened tooltip preview in list view."""
        if not obj.tooltip_text:
            return "-"
        return obj.tooltip_text[:40] + ("..." if len(obj.tooltip_text) > 40 else "")
    short_tooltip.short_description = "Tooltip"


@admin.register(NewBusinessConfirmation)
class NewBusinessConfirmationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "buyer",
        "seller",
        "material",
        "quantity",
        "created_at",
        "updated_at",
    )
    list_filter = ("seller", "buyer", "material", "created_at")
    search_fields = ("buyer", "seller", "material")
    ordering = ("-created_at",)

    fieldsets = (
        ("Parties", {
            "fields": ("buyer", "seller"),
            "description": "Information about buyer and seller companies."
        }),
        ("Deal Details", {
            "fields": ("material", "quantity"),
            "description": "Specify material and quantity of the deal."
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "description": "System-generated timestamps for auditing."
        }),
    )
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        """Optimize queryset with select_related if needed (for future FKs)."""
        return super().get_queryset(request)

    def quantity_display(self, obj):
        """Format quantity with two decimals and commas."""
        return f"{obj.quantity:,.2f}"
    quantity_display.short_description = "Quantity"


@admin.register(CommercialTerms)
class CommercialTermsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "delivery_term",
        "delivery_point",
        "packaging",
        "transport_mode",
        "shipment_period",
        "treatment_charge_display",
        "refining_charge_display",
        "china_import_compliant",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "delivery_term",
        "transport_mode",
        "packaging",
        "china_import_compliant",
        "created_at",
    )
    search_fields = ("delivery_point", "delivery_term", "packaging", "transport_mode")
    ordering = ("-created_at",)

    fieldsets = (
        ("Delivery & Shipment", {
            "fields": (
                "delivery_term", 
                "delivery_point", 
                "packaging", 
                "transport_mode",
                "inland_freight_buyer",
                "shipment_start_date",
                "shipment_end_date",
                "shipment_evenly_distributed",
            ),
            "description": "Define logistics terms, shipment schedule, and responsibility for inland freight."
        }),
        ("Pricing & Charges", {
            "fields": (
                "treatment_charge", "treatment_charge_unit",
                "refining_charge", "refining_charge_unit",
            ),
            "description": "Specify treatment and refining charges with their respective units."
        }),
        ("Assay / Quality", {
            "fields": ("assay_file", "china_import_compliant"),
            "description": "Attach assay documentation and compliance details."
        }),
        ("Additional Terms", {
            "fields": ("clauses",),
            "description": "List of extra clauses (JSON list of strings)."
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "description": "System-generated audit timestamps."
        }),
    )

    readonly_fields = ("created_at", "updated_at")

    # === Custom display helpers ===

    def shipment_period(self, obj):
        """Show shipment start and end as a range."""
        if obj.shipment_start_date and obj.shipment_end_date:
            return f"{obj.shipment_start_date} → {obj.shipment_end_date}"
        elif obj.shipment_start_date:
            return f"From {obj.shipment_start_date}"
        elif obj.shipment_end_date:
            return f"Until {obj.shipment_end_date}"
        return "-"
    shipment_period.short_description = "Shipment Period"

    def treatment_charge_display(self, obj):
        """Show treatment charge with unit."""
        if obj.treatment_charge is not None:
            return f"{obj.treatment_charge} {obj.treatment_charge_unit}"
        return "-"
    treatment_charge_display.short_description = "Treatment Charge"

    def refining_charge_display(self, obj):
        """Show refining charge with unit."""
        if obj.refining_charge is not None:
            return f"{obj.refining_charge} {obj.refining_charge_unit}"
        return "-"
    refining_charge_display.short_description = "Refining Charge"


@admin.register(PaymentTerms)
class PaymentTermsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "prepayment_percentage",
        "payment_method",
        "currency",
        "buyer_cost_share_percentage",
        "seller_cost_share_percentage",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "payment_method",
        "currency",
        "created_at",
    )
    search_fields = (
        "payment_method",
        "currency",
        "prepayment_trigger",
        "final_determination_location",
        "nominated_by",
        "agreed_by",
    )
    ordering = ("-created_at",)

    fieldsets = (
        ("Payment Stages", {
            "fields": (
                "prepayment_percentage",
                "prepayment_trigger",
                "provisional_payment_terms",
                "final_payment_terms",
            ),
            "description": "Define prepayment percentage, its trigger, and detailed provisional/final payment terms."
        }),
        ("Payment Method & Terms", {
            "fields": (
                "payment_method",
                "currency",
                "triggering_event",
                "reference_document",
            ),
            "description": "General payment method, currency, and conditions that trigger payments."
        }),
        ("WSMD & Surveyor", {
            "fields": (
                "final_determination_location",
                "buyer_cost_share_percentage",
                "seller_cost_share_percentage",
                "nominated_by",
                "agreed_by",
                "surveyor_notes",
            ),
            "description": "Surveyor-related details and cost-sharing agreements."
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "description": "System-managed timestamps."
        }),
    )

    readonly_fields = ("created_at", "updated_at")


@admin.register(BusinessConfirmationDeal)
class BusinessConfirmationDealAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "new_business_confirmation",
        "commercial_terms",
        "payment_terms",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = (
        "id",
        "user__username",
        "new_business_confirmation__buyer",
        "new_business_confirmation__seller",
        "commercial_terms__incoterm",
        "payment_terms__payment_method",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    autocomplete_fields = (
        "user",
        "new_business_confirmation",
        "commercial_terms",
        "payment_terms",
    )