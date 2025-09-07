from typing import Dict, Optional, Any


class AISuggestionsService:
    """
    Singleton AI service that provides hardcoded suggestions for commercial terms fields
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AISuggestionsService, cls).__new__(cls)
        return cls._instance

    def get_suggestion(
        self,
        field_name: str,
        field_value: Any,
        material: Optional[str] = None,
        transport_mode: Optional[str] = None,
        delivery_term: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get AI suggestion for a specific field
        
        Args:
            field_name: Name of the field (e.g., 'prepayment', 'treatment_charge', etc.)
            field_value: Current value entered by user
            material: Material type for context (optional)
            transport_mode: Transport mode for context (optional)
        
        Returns:
            Dictionary with suggestion data or None if no suggestion
        """
        
        # Hardcoded suggestions for specific fields
        suggestions = {
            'prepayment': {
                'type': 'info',
                'message': 'Most deals use 20-40%',
                'suggested_value': None,
                'show_accept_button': False
            },
            'provisional_payment_terms': {
                'type': 'info',
                'message': 'Common for this route: 95% provisional on rail bill copy.',
                'suggested_value': None,
                'show_accept_button': False
            },
            'triggering_event': {
                'type': 'info',
                'message': 'Common timing for provisional payments is 3-5 days post RWB',
                'suggested_value': None,
                'show_accept_button': False
            },
            'cost_sharing': {
                'type': 'info',
                'message': 'Typical share is 50/50.',
                'suggested_value': None,
                'show_accept_button': False
            },
            'treatment_charge': {
                'type': 'info',
                'message': 'Industry average TC for Lead: $310-$325/dmt',
                'suggested_value': None,
                'show_accept_button': False
            },
            'refining_charge': {
                'type': 'warning',
                'message': 'Your RC is higher than average, adjust to $4.50?',
                'suggested_value': 4.50,
                'show_accept_button': True
            }
        }
        
        return suggestions.get(field_name)
    
    def get_general_suggestion(
        self,
        field_name: str,
        field_value: Any,
        context: Optional[Dict[str, Any]] = None,
        material: Optional[str] = None,
        transport_mode: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get general suggestions that might apply to any field
        This method is kept for compatibility but returns None since we use hardcoded suggestions
        """
        return None


# Singleton instance
ai_suggestions_service = AISuggestionsService()
