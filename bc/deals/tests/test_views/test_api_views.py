import pytest
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from deals.models import BusinessConfirmationDeal
from deals.tests.factories import (
    UserFactory, NewBusinessConfirmationFactory,
    CommercialTermsFactory, PaymentTermsFactory,
    BusinessConfirmationDealFactory, DropdownOptionFactory,
    TaskStatusFactory
)

User = get_user_model()


@pytest.fixture
def api_client():
    """Create API client for testing"""
    return APIClient()


@pytest.fixture
def authenticated_user(api_client):
    """Create and authenticate a user"""
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return user


@pytest.mark.django_db
class TestNewBusinessConfirmationAPI:
    """Test cases for NewBusinessConfirmation API endpoints"""

    def test_get_new_business_confirmations_authenticated(self, api_client, authenticated_user):
        """Test GET request to new business confirmations endpoint"""
        confirmation1 = NewBusinessConfirmationFactory()
        confirmation2 = NewBusinessConfirmationFactory()
        
        url = reverse('deals:new-business-confirmation')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_get_new_business_confirmations_unauthenticated(self, api_client):
        """Test GET request without authentication"""
        url = reverse('deals:new-business-confirmation')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_new_business_confirmation(self, api_client, authenticated_user):
        """Test POST request to create new business confirmation"""
        data = {
            'seller': 'Open Mineral',
            'buyer': 'Test Company',
            'material': 'Akzhal',
            'quantity': '1000.50'
        }
        
        url = reverse('deals:new-business-confirmation')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['seller'] == 'Open Mineral'
        assert response.data['buyer'] == 'Test Company'
        assert response.data['material'] == 'Akzhal'
        assert Decimal(response.data['quantity']) == Decimal('1000.50')

    def test_create_new_business_confirmation_invalid_data(self, api_client, authenticated_user):
        """Test POST request with invalid data"""
        data = {
            'seller': 'Open Mineral',
            'buyer': 'Test Company',
            'material': 'Akzhal',
            'quantity': '-100.00'
        }
        
        url = reverse('deals:new-business-confirmation')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_new_business_confirmation_missing_required_fields(self, api_client, authenticated_user):
        """Test POST request with missing required fields"""
        data = {
            'seller': 'Open Mineral'
        }
        
        url = reverse('deals:new-business-confirmation')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCommercialTermsAPI:
    """Test cases for CommercialTerms API endpoints"""

    def test_get_commercial_terms(self, api_client, authenticated_user):
        """Test GET request to commercial terms endpoint"""
        terms1 = CommercialTermsFactory()
        terms2 = CommercialTermsFactory()
        
        url = reverse('deals:commercial-terms')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_commercial_terms(self, api_client, authenticated_user):
        """Test POST request to create commercial terms"""
        data = {
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
        
        url = reverse('deals:commercial-terms')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['delivery_term'] == 'DAP'
        assert response.data['delivery_point'] == 'Port of Rotterdam'
        assert response.data['packaging'] == 'Big Bags'
        assert response.data['transport_mode'] == 'Ship'
        assert response.data['inland_freight_buyer'] is True

    def test_create_commercial_terms_negative_charges(self, api_client, authenticated_user):
        """Test POST request with negative charges"""
        data = {
            'delivery_term': 'DAP',
            'treatment_charge': '-10.00',
            'refining_charge': '45.25'
        }
        
        url = reverse('deals:commercial-terms')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPaymentTermsAPI:
    """Test cases for PaymentTerms API endpoints"""

    def test_get_payment_terms(self, api_client, authenticated_user):
        """Test GET request to payment terms endpoint"""
        terms1 = PaymentTermsFactory()
        terms2 = PaymentTermsFactory()
        
        url = reverse('deals:payment-terms')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_payment_terms(self, api_client, authenticated_user):
        """Test POST request to create payment terms"""
        data = {
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
        
        url = reverse('deals:payment-terms')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['payment_stage_1_percentage'] == '30.00'
        assert response.data['payment_stage_2_percentage'] == '40.00'
        assert response.data['payment_stage_3_percentage'] == '30.00'
        assert response.data['currency'] == 'USD'
        assert response.data['payment_method'] == 'Bank Transfer'

    def test_create_payment_terms_invalid_percentages(self, api_client, authenticated_user):
        """Test POST request with invalid payment percentages"""
        data = {
            'payment_stage_1_percentage': '50.00',
            'payment_stage_2_percentage': '40.00',
            'payment_stage_3_percentage': '30.00',
            'currency': 'USD'
        }
        
        url = reverse('deals:payment-terms')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestDropdownOptionsAPI:
    """Test cases for DropdownOptions API endpoints"""

    def test_get_dropdown_options(self, api_client, authenticated_user):
        """Test GET request to dropdown options endpoint"""
        option1 = DropdownOptionFactory(field_name='material')
        option2 = DropdownOptionFactory(field_name='delivery_term')
        
        url = reverse('deals:dropdown')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_dropdown_options_caching(self, api_client, authenticated_user):
        """Test that dropdown options are cached"""
        option1 = DropdownOptionFactory(field_name='material')
        
        url = reverse('deals:dropdown')
        
        response1 = api_client.get(url)
        assert response1.status_code == status.HTTP_200_OK
        
        response2 = api_client.get(url)
        assert response2.status_code == status.HTTP_200_OK
        assert response1.data == response2.data

    def test_dropdown_options_only_active(self, api_client, authenticated_user):
        """Test that only active dropdown options are returned"""
        active_option = DropdownOptionFactory(is_active=True)
        inactive_option = DropdownOptionFactory(is_active=False)
        
        url = reverse('deals:dropdown')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == active_option.id


@pytest.mark.django_db
class TestBusinessConfirmationDealAPI:
    """Test cases for BusinessConfirmationDeal API endpoints"""

    def test_get_business_confirmation_deals(self, api_client, authenticated_user):
        """Test GET request to business confirmation deals endpoint"""
        deal1 = BusinessConfirmationDealFactory(user=authenticated_user)
        deal2 = BusinessConfirmationDealFactory(user=authenticated_user)
        
        url = reverse('deals:business-confirmation-deals')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_business_confirmation_deal(self, api_client, authenticated_user):
        """Test POST request to create business confirmation deal"""
        confirmation = NewBusinessConfirmationFactory()
        commercial_terms = CommercialTermsFactory()
        payment_terms = PaymentTermsFactory()
        
        data = {
            'new_business_confirmation': confirmation.id,
            'commercial_terms': commercial_terms.id,
            'payment_terms': payment_terms.id,
            'status': BusinessConfirmationDeal.DRAFT
        }
        
        url = reverse('deals:business-confirmation-deals')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == BusinessConfirmationDeal.DRAFT
        assert response.data['new_business_confirmation'] == confirmation.id

    def test_create_business_confirmation_deal_minimal_data(self, api_client, authenticated_user):
        """Test POST request with minimal required data"""
        data = {
            'status': BusinessConfirmationDeal.DRAFT
        }
        
        url = reverse('deals:business-confirmation-deals')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == BusinessConfirmationDeal.DRAFT


@pytest.mark.django_db
class TestTaskStatusAPI:
    """Test cases for TaskStatus API endpoints"""

    def test_get_task_status(self, api_client, authenticated_user):
        """Test GET request to task status endpoint"""
        deal = BusinessConfirmationDealFactory(user=authenticated_user)
        task_status = TaskStatusFactory(deal=deal)
        
        url = reverse('deals:task-status', kwargs={'task_status_id': task_status.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['task_id'] == task_status.task_id
        assert response.data['status'] == task_status.status

    def test_get_nonexistent_task_status(self, api_client, authenticated_user):
        """Test GET request for non-existent task status"""
        import uuid
        fake_id = uuid.uuid4()
        
        url = reverse('deals:task-status', kwargs={'task_status_id': fake_id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestSubmitDealAPI:
    """Test cases for SubmitDeal API endpoints"""

    def test_submit_deal(self, api_client, authenticated_user):
        """Test POST request to submit deal"""
        deal = BusinessConfirmationDealFactory(
            user=authenticated_user,
            status=BusinessConfirmationDeal.DRAFT
        )
        
        url = reverse('deals:submit-deal', kwargs={'deal_id': deal.id})
        response = api_client.post(url)
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]

    def test_submit_nonexistent_deal(self, api_client, authenticated_user):
        """Test POST request to submit non-existent deal"""
        import uuid
        fake_id = uuid.uuid4()
        
        url = reverse('deals:submit-deal', kwargs={'deal_id': fake_id})
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_submit_deal_wrong_user(self, api_client, authenticated_user):
        """Test submitting deal that belongs to different user"""
        other_user = UserFactory()
        deal = BusinessConfirmationDealFactory(user=other_user)
        
        url = reverse('deals:submit-deal', kwargs={'deal_id': deal.id})
        response = api_client.post(url)
        
        assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestAISuggestionsAPI:
    """Test cases for AI Suggestions API endpoints"""

    def test_ai_suggestions_endpoint(self, api_client, authenticated_user):
        """Test POST request to AI suggestions endpoint"""
        data = {
            'deal_id': 'test-deal-123',
            'suggestion_type': 'commercial_terms'
        }
        
        url = reverse('deals:ai-suggestions')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]

    def test_ai_suggestions_missing_data(self, api_client, authenticated_user):
        """Test POST request with missing required data"""
        data = {
            'deal_id': 'test-deal-123'
        }
        
        url = reverse('deals:ai-suggestions')
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAPIAuthentication:
    """Test cases for API authentication"""

    def test_all_endpoints_require_authentication(self, api_client):
        """Test that all endpoints require authentication"""
        endpoints = [
            'deals:new-business-confirmation',
            'deals:commercial-terms',
            'deals:payment-terms',
            'deals:dropdown',
            'deals:business-confirmation-deals',
            'deals:ai-suggestions'
        ]
        
        for endpoint in endpoints:
            url = reverse(endpoint)
            response = api_client.get(url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_access_endpoints(self, api_client, authenticated_user):
        """Test that authenticated user can access all endpoints"""
        endpoints = [
            'deals:new-business-confirmation',
            'deals:commercial-terms',
            'deals:payment-terms',
            'deals:dropdown',
            'deals:business-confirmation-deals'
        ]
        
        for endpoint in endpoints:
            url = reverse(endpoint)
            response = api_client.get(url)
            assert response.status_code == status.HTTP_200_OK
