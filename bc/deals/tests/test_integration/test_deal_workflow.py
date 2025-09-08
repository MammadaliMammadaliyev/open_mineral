import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from deals.models import (
    NewBusinessConfirmation, BusinessConfirmationDeal,
    CommercialTerms, PaymentTerms, TaskStatus
)
from deals.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestCompleteDealWorkflow:
    """Integration tests for complete deal workflow"""

    def test_complete_deal_creation_workflow(self):
        """Test complete workflow from deal creation to submission"""
        # Setup
        api_client = APIClient()
        user = UserFactory()
        api_client.force_authenticate(user=user)
        
        # Step 1: Create New Business Confirmation
        confirmation_data = {
            'seller': 'Open Mineral',
            'buyer': 'Test Company Ltd',
            'material': 'Akzhal',
            'quantity': '1000.50'
        }
        
        from django.urls import reverse
        confirmation_url = reverse('deals:new-business-confirmation')
        confirmation_response = api_client.post(confirmation_url, confirmation_data, format='json')
        
        assert confirmation_response.status_code == 201
        confirmation_id = confirmation_response.data['id']
        
        # Step 2: Create Commercial Terms
        commercial_terms_data = {
            'delivery_term': 'DAP',
            'delivery_point': 'Port of Rotterdam',
            'packaging': 'Big Bags',
            'transport_mode': 'Ship',
            'inland_freight_buyer': True,
            'treatment_charge': '75.50',
            'refining_charge': '45.25',
            'treatment_charge_unit': 'dmt',
            'refining_charge_unit': 'dmt'
        }
        
        commercial_terms_url = reverse('deals:commercial-terms')
        commercial_terms_response = api_client.post(commercial_terms_url, commercial_terms_data, format='json')
        
        assert commercial_terms_response.status_code == 201
        commercial_terms_id = commercial_terms_response.data['id']
        
        # Step 3: Create Payment Terms
        payment_terms_data = {
            'payment_stage_1_percentage': '30.00',
            'payment_stage_1_days': 30,
            'payment_stage_2_percentage': '40.00',
            'payment_stage_2_days': 60,
            'payment_stage_3_percentage': '30.00',
            'payment_stage_3_days': 90,
            'currency': 'USD',
            'payment_method': 'Bank Transfer',
            'credit_terms_days': 30,
            'guarantee_required': True
        }
        
        payment_terms_url = reverse('deals:payment-terms')
        payment_terms_response = api_client.post(payment_terms_url, payment_terms_data, format='json')
        
        assert payment_terms_response.status_code == 201
        payment_terms_id = payment_terms_response.data['id']
        
        # Step 4: Create Business Confirmation Deal
        deal_data = {
            'new_business_confirmation': confirmation_id,
            'commercial_terms': commercial_terms_id,
            'payment_terms': payment_terms_id,
            'status': 'draft'
        }
        
        deal_url = reverse('deals:business-confirmation-deals')
        deal_response = api_client.post(deal_url, deal_data, format='json')
        
        assert deal_response.status_code == 201
        deal_id = deal_response.data['id']
        
        # Step 5: Verify deal relationships
        deal = BusinessConfirmationDeal.objects.get(id=deal_id)
        assert deal.user == user
        assert deal.new_business_confirmation.id == confirmation_id
        assert deal.commercial_terms.id == commercial_terms_id
        assert deal.payment_terms.id == payment_terms_id
        assert deal.status == 'draft'
        
        # Step 6: Submit deal (if endpoint exists)
        submit_url = reverse('deals:submit-deal', kwargs={'deal_id': deal_id})
        submit_response = api_client.post(submit_url)
        
        # This might return 200 or 202 depending on implementation
        assert submit_response.status_code in [200, 202]

    def test_deal_validation_workflow(self):
        """Test deal validation workflow with invalid data"""
        api_client = APIClient()
        user = UserFactory()
        api_client.force_authenticate(user=user)
        
        from django.urls import reverse
        
        # Test with invalid quantity
        invalid_confirmation_data = {
            'seller': 'Open Mineral',
            'buyer': 'Test Company',
            'material': 'Akzhal',
            'quantity': '-100.00'  # Invalid negative quantity
        }
        
        confirmation_url = reverse('deals:new-business-confirmation')
        response = api_client.post(confirmation_url, invalid_confirmation_data, format='json')
        
        assert response.status_code == 400
        assert 'quantity' in str(response.data)

    def test_deal_with_ai_suggestions_workflow(self):
        """Test deal workflow with AI suggestions"""
        api_client = APIClient()
        user = UserFactory()
        api_client.force_authenticate(user=user)
        
        from django.urls import reverse
        
        # Create a basic deal first
        deal = BusinessConfirmationDeal.objects.create(
            user=user,
            status='draft'
        )
        
        # Test AI suggestions
        ai_suggestions_data = {
            'deal_id': str(deal.id),
            'suggestion_type': 'commercial_terms'
        }
        
        ai_url = reverse('deals:ai-suggestions')
        ai_response = api_client.post(ai_url, ai_suggestions_data, format='json')
        
        # This might return 200 or 202 depending on implementation
        assert ai_response.status_code in [200, 202]

    def test_deal_task_status_workflow(self):
        """Test deal task status workflow"""
        api_client = APIClient()
        user = UserFactory()
        api_client.force_authenticate(user=user)
        
        from django.urls import reverse
        
        # Create a deal
        deal = BusinessConfirmationDeal.objects.create(
            user=user,
            status='processing'
        )
        
        # Create a task status
        task_status = TaskStatus.objects.create(
            task_id='test-task-123',
            deal=deal,
            status='processing',
            message='Task is being processed'
        )
        
        # Test getting task status
        task_url = reverse('deals:task-status', kwargs={'task_status_id': task_status.id})
        task_response = api_client.get(task_url)
        
        assert task_response.status_code == 200
        assert task_response.data['task_id'] == 'test-task-123'
        assert task_response.data['status'] == 'processing'

    def test_deal_permissions_workflow(self):
        """Test deal permissions workflow"""
        api_client = APIClient()
        user1 = UserFactory()
        user2 = UserFactory()
        
        # Create deal for user1
        deal = BusinessConfirmationDeal.objects.create(
            user=user1,
            status='draft'
        )
        
        # Try to access deal as user2
        api_client.force_authenticate(user=user2)
        
        from django.urls import reverse
        submit_url = reverse('deals:submit-deal', kwargs={'deal_id': deal.id})
        submit_response = api_client.post(submit_url)
        
        # Should return 404 or 403
        assert submit_response.status_code in [404, 403]

    def test_deal_data_consistency_workflow(self):
        """Test data consistency across deal workflow"""
        api_client = APIClient()
        user = UserFactory()
        api_client.force_authenticate(user=user)
        
        from django.urls import reverse
        
        # Create all components
        confirmation_data = {
            'seller': 'Open Mineral',
            'buyer': 'Test Company',
            'material': 'Akzhal',
            'quantity': '1000.50'
        }
        
        confirmation_url = reverse('deals:new-business-confirmation')
        confirmation_response = api_client.post(confirmation_url, confirmation_data, format='json')
        confirmation_id = confirmation_response.data['id']
        
        # Create deal with confirmation
        deal_data = {
            'new_business_confirmation': confirmation_id,
            'status': 'draft'
        }
        
        deal_url = reverse('deals:business-confirmation-deals')
        deal_response = api_client.post(deal_url, deal_data, format='json')
        deal_id = deal_response.data['id']
        
        # Verify data consistency
        deal = BusinessConfirmationDeal.objects.get(id=deal_id)
        confirmation = NewBusinessConfirmation.objects.get(id=confirmation_id)
        
        assert deal.new_business_confirmation == confirmation
        assert deal.user == user
        assert confirmation.seller == 'Open Mineral'
        assert confirmation.buyer == 'Test Company'
        assert confirmation.material == 'Akzhal'
        assert Decimal(str(confirmation.quantity)) == Decimal('1000.50')
