import logging
import time
from celery import shared_task
from django.utils import timezone
from django.db import transaction
from deals.models import BusinessConfirmationDeal, TaskStatus

logger = logging.getLogger("deals")


@shared_task(bind=True)
def process_business_confirmation_deal(self, deal_id, task_status_id):
    """
    Alternative implementation using atomic decorator for the entire function.
    This approach keeps everything in one transaction but may cause issues
    with long-running operations (like the 15-second sleep).
    """
    try:
        with transaction.atomic():
            # Get the task status object
            task_status = TaskStatus.objects.select_for_update().get(id=task_status_id)
            
            # Validate task state
            if task_status.status not in [TaskStatus.PENDING]:
                logger.warning(f"Task {task_status_id} is not in pending state (current: {task_status.status})")
                return
            
            # Update to processing
            task_status.status = TaskStatus.PROCESSING
            task_status.message = "Processing business confirmation deal..."
            task_status.save()
            
            logger.info(f"Starting processing for deal {deal_id}, task {self.request.id}")
            
            # Get the deal
            deal = BusinessConfirmationDeal.objects.select_for_update().get(id=deal_id)
            
            # Simulate processing (this keeps the transaction open for 15 seconds)
            # WARNING: This may cause database lock issues in production
            time.sleep(15)
            
            # Update deal status to processing
            deal.status = BusinessConfirmationDeal.PROCESSING
            deal.save()
            
            # Update task status to completed
            task_status.status = TaskStatus.COMPLETED
            task_status.message = "Business confirmation deal processed successfully"
            task_status.completed_at = timezone.now()
            task_status.save()
            
            # Update deal status to completed
            deal.status = BusinessConfirmationDeal.COMPLETED
            deal.save()
            
            logger.info(f"Successfully processed deal {deal_id}, task {self.request.id}")
            
    except Exception as e:
        logger.error(f"Error processing deal {deal_id}: {str(e)}")
        # Handle errors with atomic updates
        try:
            with transaction.atomic():
                task_status = TaskStatus.objects.select_for_update().get(id=task_status_id)
                task_status.status = TaskStatus.FAILED
                task_status.message = f"Processing failed: {str(e)}"
                task_status.completed_at = timezone.now()
                task_status.save()
        except Exception as update_error:
            logger.error(f"Failed to update task status: {update_error}")
