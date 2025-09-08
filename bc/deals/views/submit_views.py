import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from deals.models import BusinessConfirmationDeal, TaskStatus
from deals.tasks.processing_tasks import process_business_confirmation_deal
from rest_framework.throttling import UserRateThrottle

logger = logging.getLogger("deals")


class SubmitDealView(APIView):
    """
    API endpoint to submit a business confirmation deal for processing.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @swagger_auto_schema(
        operation_description="Submit a business confirmation deal for processing",
        manual_parameters=[
            openapi.Parameter(
                'deal_id',
                openapi.IN_PATH,
                description="UUID of the business confirmation deal",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID
            )
        ],
        responses={
            200: openapi.Response(
                description="Deal submitted successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'task_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'task_status_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'status': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            404: openapi.Response(description="Deal not found"),
            400: openapi.Response(description="Deal already submitted or invalid status")
        }
    )
    def post(self, request, deal_id):
        try:
            # Get the deal
            deal = get_object_or_404(BusinessConfirmationDeal, id=deal_id)

            # Check if deal is in a valid state for submission
            if deal.status not in [BusinessConfirmationDeal.DRAFT, BusinessConfirmationDeal.CANCELLED]:
                return Response(
                    {"error": "Deal is already submitted or processed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create task status record
            task_status = TaskStatus.objects.create(
                deal=deal,
                status=TaskStatus.PENDING,
                message="Task queued for processing"
            )
            
            # Update deal status to submitted
            deal.status = BusinessConfirmationDeal.SUBMITTED
            deal.save()
            
            # Start the background task
            task = process_business_confirmation_deal.delay(
                str(deal_id), 
                str(task_status.id)
            )
            
            # Update task status with the actual Celery task ID
            task_status.task_id = task.id
            task_status.save()
            
            logger.info(f"Deal {deal_id} submitted for processing by user {request.user}, task {task.id}")
            
            return Response({
                "message": "Deal submitted successfully for processing",
                "task_id": task.id,
                "task_status_id": str(task_status.id),
                "status": "submitted"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error submitting deal {deal_id}: {str(e)}")
            return Response(
                {"error": "Failed to submit deal for processing"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskStatusView(APIView):
    """
    API endpoint to check the status of a background task.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @swagger_auto_schema(
        operation_description="Get the status of a background task",
        manual_parameters=[
            openapi.Parameter(
                'task_status_id',
                openapi.IN_PATH,
                description="UUID of the task status",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID
            )
        ],
        responses={
            200: openapi.Response(
                description="Task status retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'task_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING),
                        'completed_at': openapi.Schema(type=openapi.TYPE_STRING),
                        'deal_id': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            404: openapi.Response(description="Task status not found")
        }
    )
    def get(self, request, task_status_id):
        try:
            task_status = get_object_or_404(TaskStatus, id=task_status_id)
            
            logger.debug(f"Retrieved task status {task_status_id} for user {request.user}")
            
            return Response({
                "task_id": task_status.task_id,
                "status": task_status.status,
                "message": task_status.message,
                "created_at": task_status.created_at.isoformat(),
                "updated_at": task_status.updated_at.isoformat(),
                "completed_at": task_status.completed_at.isoformat() if task_status.completed_at else None,
                "deal_id": str(task_status.deal.id)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving task status {task_status_id}: {str(e)}")
            return Response(
                {"error": "Failed to retrieve task status"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
