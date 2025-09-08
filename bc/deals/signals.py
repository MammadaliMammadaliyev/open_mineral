import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from deals.models import DropdownOption
from deals.views.dropdown_views import DropdownOptionView

logger = logging.getLogger("deals")


@receiver(post_save, sender=DropdownOption)
def invalidate_dropdown_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate dropdown options cache when a DropdownOption is saved (created or updated).
    
    Args:
        sender: The model class that sent the signal
        instance: The actual instance being saved
        **kwargs: Additional keyword arguments
    """
    cache_key = DropdownOptionView.CACHE_KEY
    from django.core.cache import cache
    cache.delete(cache_key)
    logger.info(f"Dropdown options cache invalidated due to save of {instance}")


@receiver(post_delete, sender=DropdownOption)
def invalidate_dropdown_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate dropdown options cache when a DropdownOption is deleted.
    
    Args:
        sender: The model class that sent the signal
        instance: The actual instance being deleted
        **kwargs: Additional keyword arguments
    """
    cache_key = DropdownOptionView.CACHE_KEY
    from django.core.cache import cache
    cache.delete(cache_key)
    logger.info(f"Dropdown options cache invalidated due to deletion of {instance}")