from django.db import models


class DropdownOption(models.Model):
    field_name = models.CharField(
        max_length=100, 
        help_text="Field name (e.g., material, delivery_term)"
    )
    option_values = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Display value (e.g., {\"akzhal\": \"Akzhal\", \"dap\": \"DAP (Delivered at Place)\"})"
    )
    display_order = models.IntegerField( # maybe replace by step_number
        default=0,
        blank=True,
        null=True,
        help_text="Order for display"
    )
    tooltip_text = models.TextField(
        blank=True, 
        null=True,
        help_text="Tooltip content for info icon"
    )

    is_active = models.BooleanField(
        default=True,
        blank=True,
        null=True,
        help_text="Whether this option is active"
    )

    class Meta:
        unique_together = ["field_name", "option_values"]
        ordering = ["field_name", "display_order", "option_values"]
        verbose_name = "Dropdown Option"
        verbose_name_plural = "Dropdown Options"

    def __str__(self):
        return f"{self.field_name}: {self.option_values}"
