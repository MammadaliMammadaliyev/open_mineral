from django.db import models


class DropdownOption(models.Model):
    field_name = models.CharField(
        max_length=100, 
        help_text='Field name (e.g., material, delivery_term)'
    )
    option_key = models.CharField(
        max_length=100, 
        help_text='Option key (e.g., akzhal, dap)'
    )
    option_value = models.CharField(
        max_length=255, 
        help_text='Display value (e.g., Akzhal, DAP (Delivered at Place))'
    )
    display_order = models.IntegerField(
        default=0, 
        help_text='Order for display'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this option is active'
    )
    tooltip_text = models.TextField(
        blank=True, 
        help_text='Tooltip content for info icon'
    )
    
    class Meta:
        unique_together = ['field_name', 'option_key']
        ordering = ['field_name', 'display_order', 'option_key']
        verbose_name = 'Dropdown Option'
        verbose_name_plural = 'Dropdown Options'
    
    def __str__(self):
        return f'{self.field_name}: {self.option_value}'
