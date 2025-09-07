import uuid

from django.db import models
from django.core.validators import MinValueValidator


class Deal(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    seller = models.CharField(
        max_length=255, 
        default='Open Mineral',
        help_text='Seller company name'
    )
    buyer = models.CharField(
        max_length=255,
        help_text='Buyer company name'
    )
    material = models.CharField(
        max_length=255,
        help_text='Material type (e.g., Akzhal, Lead concentrate)'
    )
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text='Quantity in specified unit'
    )