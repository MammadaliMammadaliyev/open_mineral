import logging
import time
from datetime import datetime
from celery import shared_task
from django.utils import timezone
from deals.models import BusinessConfirmationDeal, TaskStatus

logger = logging.getLogger("deals")


@shared_task(bind=True)
def process_business_confirmation_deal(self, deal_id, task_status_id):
    """
    Background task to process a business confirmation deal.
    Simulates processing by sleeping for 15 seconds.
    """
    try:
        # Get the task status object
        task_status = TaskStatus.objects.get(id=task_status_id)
        
        # Update status to processing
        task_status.status = TaskStatus.PROCESSING
        task_status.message = "Processing business confirmation deal..."
        task_status.save()
        
        logger.info(f"Starting processing for deal {deal_id}, task {self.request.id}")
        
        # Simulate processing by sleeping for 15 seconds
        time.sleep(15)
        
        # Get the deal and update its status
        try:
            deal = BusinessConfirmationDeal.objects.get(id=deal_id)
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
            
        except BusinessConfirmationDeal.DoesNotExist:
            logger.error(f"Deal {deal_id} not found during processing")
            task_status.status = TaskStatus.FAILED
            task_status.message = f"Deal {deal_id} not found"
            task_status.completed_at = timezone.now()
            task_status.save()
            
    except TaskStatus.DoesNotExist:
        logger.error(f"Task status {task_status_id} not found")
    except Exception as e:
        logger.error(f"Error processing deal {deal_id}: {str(e)}")
        try:
            task_status = TaskStatus.objects.get(id=task_status_id)
            task_status.status = TaskStatus.FAILED
            task_status.message = f"Processing failed: {str(e)}"
            task_status.completed_at = timezone.now()
            task_status.save()
        except TaskStatus.DoesNotExist:
            pass
