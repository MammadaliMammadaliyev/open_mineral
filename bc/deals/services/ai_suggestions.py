from decimal import Decimal
from typing import Dict, Optional, Any


class AISuggestionsService:
    """
    Mock AI service that provides suggestions for commercial terms fields
    """
    
    # Mock market data for different materials
    MARKET_DATA = {
        'lead_concentrate': {
            'treatment_charge_range': (310, 325),
            'refining_charge_range': (4.2, 4.8),
            'materials': ['Lead Concentrate', 'Pb Concentrate', 'Lead']
        },
        'zinc_concentrate': {
            'treatment_charge_range': (180, 200),
            'refining_charge_range': (3.5, 4.2),
            'materials': ['Zinc Concentrate', 'Zn Concentrate', 'Zinc']
        },
        'copper_concentrate': {
            'treatment_charge_range': (120, 140),
            'refining_charge_range': (2.8, 3.5),
            'materials': ['Copper Concentrate', 'Cu Concentrate', 'Copper']
        },
        'iron_ore': {
            'treatment_charge_range': (15, 25),
            'refining_charge_range': (0.5, 1.2),
            'materials': ['Iron Ore', 'Fe Ore', 'Iron']
        },
        'coal': {
            'treatment_charge_range': (8, 15),
            'refining_charge_range': (0.2, 0.8),
            'materials': ['Coal', 'Thermal Coal', 'Coking Coal']
        },
        'gold_concentrate': {
            'treatment_charge_range': (450, 500),
            'refining_charge_range': (8.5, 12.0),
            'materials': ['Gold Concentrate', 'Au Concentrate', 'Gold']
        },
        'silver_concentrate': {
            'treatment_charge_range': (380, 420),
            'refining_charge_range': (6.5, 9.0),
            'materials': ['Silver Concentrate', 'Ag Concentrate', 'Silver']
        }
    }
    
    def get_suggestion(
        self,
        field_name: str,
        field_value: Any,
        material: str = None,
        transport_mode: str = None,
        delivery_term: str = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get AI suggestion for a specific field
        
        Args:
            field_name: Name of the field (e.g., 'treatment_charge', 'refining_charge')
            field_value: Current value entered by user
            material: Material type (optional, for context)
            transport_mode: Transport mode (optional, for packaging suggestions)
        
        Returns:
            Dictionary with suggestion data or None if no suggestion
        """
        
        if field_name == 'treatment_charge':
            return self._get_treatment_charge_suggestion(field_value, material)
        elif field_name == 'refining_charge':
            return self._get_refining_charge_suggestion(field_value, material)
        elif field_name == 'packaging':
            return self._get_packaging_suggestion(transport_mode)
        elif field_name == 'delivery_term':
            return self._get_delivery_term_suggestion(field_value)
        elif field_name == 'transport_mode':
            return self._get_transport_mode_suggestion(field_value)
        else:
            return None
    
    def _get_treatment_charge_suggestion(
        self,
        value: Any,
        material: str = None,
        transport_mode: str = None,
        delivery_term: str = None,
    ) -> Optional[Dict[str, Any]]:
        """Get treatment charge suggestion"""
        try:
            if not value:
                return None
                
            charge_value = float(value)
            material_key = self._get_material_key(material)
            
            if material_key and material_key in self.MARKET_DATA:
                market_range = self.MARKET_DATA[material_key]['treatment_charge_range']
                min_val, max_val = market_range
                
                # Check if value is within market range
                if min_val <= charge_value <= max_val:
                    return {
                        'type': 'info',
                        'message': f"Industry average TC for {material or 'this material'}: ${min_val}-${max_val}/dmt",
                        'suggested_value': None,
                        'show_accept_button': False
                    }
                elif charge_value > max_val:
                    suggested_value = max_val - 5  # Suggest slightly below max
                    return {
                        'type': 'warning',
                        'message': f"Your TC is higher than market average. Suggest lowering to ${suggested_value}?",
                        'suggested_value': suggested_value,
                        'show_accept_button': True
                    }
                elif charge_value < min_val:
                    suggested_value = min_val + 5  # Suggest slightly above min
                    return {
                        'type': 'warning',
                        'message': f"Your TC is lower than market average. Suggest raising to ${suggested_value}?",
                        'suggested_value': suggested_value,
                        'show_accept_button': True
                    }
            else:
                # Generic suggestion for unknown materials
                return {
                    'type': 'info',
                    'message': f"Treatment charge of ${charge_value}/dmt entered. Consider market research for optimal pricing.",
                    'suggested_value': None,
                    'show_accept_button': False
                }
                
        except (ValueError, TypeError):
            return None
    
    def _get_refining_charge_suggestion(
        self,
        value: Any,
        material: str = None,
        transport_mode: str = None,
        delivery_term: str = None,
    ) -> Optional[Dict[str, Any]]:
        """Get refining charge suggestion"""
        try:
            if not value:
                return None

            charge_value = float(value)
            material_key = self._get_material_key(material)
            
            if material_key and material_key in self.MARKET_DATA:
                market_range = self.MARKET_DATA[material_key]['refining_charge_range']
                min_val, max_val = market_range
                
                # Check if value is within market range
                if min_val <= charge_value <= max_val:
                    return {
                        'type': 'info',
                        'message': f"Industry average RC for {material or 'this material'}: ${min_val}-${max_val}/toz",
                        'suggested_value': None,
                        'show_accept_button': False
                    }
                elif charge_value > max_val:
                    suggested_value = max_val - 0.1  # Suggest slightly below max
                    return {
                        'type': 'warning',
                        'message': f"Your RC is higher than market average. Suggest lowering to ${suggested_value}?",
                        'suggested_value': suggested_value,
                        'show_accept_button': True
                    }
                elif charge_value < min_val:
                    suggested_value = min_val + 0.1  # Suggest slightly above min
                    return {
                        'type': 'warning',
                        'message': f"Your RC is lower than market average. Suggest raising to ${suggested_value}?",
                        'suggested_value': suggested_value,
                        'show_accept_button': True
                    }
            else:
                # Generic suggestion for unknown materials
                return {
                    'type': 'info',
                    'message': f"Refining charge of ${charge_value}/toz entered. Consider market research for optimal pricing.",
                    'suggested_value': None,
                    'show_accept_button': False
                }
                
        except (ValueError, TypeError):
            return None
    
    def _get_packaging_suggestion(
        self,
        transport_mode: str = None,
        delivery_term: str = None,
    ) -> Optional[Dict[str, Any]]:
        """Get packaging suggestion based on transport mode"""
        if not transport_mode:
            return None
            
        transport_mode_lower = transport_mode.lower()
        
        if 'rail' in transport_mode_lower:
            return {
                'type': 'info',
                'message': "For Rail transport, consider 'Bulk' or 'Big Bags' packaging options",
                'suggested_value': None,
                'show_accept_button': False,
                'suggested_options': ['Bulk', 'Big Bags']
            }
        elif 'ship' in transport_mode_lower:
            return {
                'type': 'info',
                'message': "For Ship transport, 'Bulk' packaging is typically recommended",
                'suggested_value': 'Bulk',
                'show_accept_button': True,
                'suggested_options': ['Bulk']
            }
        elif 'truck' in transport_mode_lower:
            return {
                'type': 'info',
                'message': "For Truck transport, consider 'Big Bags', 'Containers', or 'Pallets'",
                'suggested_value': None,
                'show_accept_button': False,
                'suggested_options': ['Big Bags', 'Containers', 'Pallets']
            }
        
        return None
    
    def _get_delivery_term_suggestion(
        self,
        value: str = None,
        transport_mode: str = None,
    ) -> Optional[Dict[str, Any]]:
        """Get delivery term suggestion"""
        if not value:
            return None
            
        value_lower = value.lower()
        
        if 'fob' in value_lower:
            return {
                'type': 'info',
                'message': "FOB terms: Seller responsible until goods pass ship's rail. Consider port location carefully.",
                'suggested_value': None,
                'show_accept_button': False
            }
        elif 'cif' in value_lower:
            return {
                'type': 'info',
                'message': "CIF terms: Seller covers cost, insurance, and freight to destination port.",
                'suggested_value': None,
                'show_accept_button': False
            }
        elif 'dap' in value_lower:
            return {
                'type': 'info',
                'message': "DAP terms: Seller delivers goods ready for unloading at named place.",
                'suggested_value': None,
                'show_accept_button': False
            }
        
        return None
    
    def _get_transport_mode_suggestion(
        self,
        value: str = None,
        delivery_term: str = None,
    ) -> Optional[Dict[str, Any]]:
        """Get transport mode suggestion"""
        if not value:
            return None
            
        value_lower = value.lower()
        
        if 'ship' in value_lower:
            return {
                'type': 'info',
                'message': "Ship transport: Most cost-effective for large volumes and long distances.",
                'suggested_value': None,
                'show_accept_button': False
            }
        elif 'rail' in value_lower:
            return {
                'type': 'info',
                'message': "Rail transport: Good for landlocked locations and medium distances.",
                'suggested_value': None,
                'show_accept_button': False
            }
        elif 'truck' in value_lower:
            return {
                'type': 'info',
                'message': "Truck transport: Best for short distances and door-to-door delivery.",
                'suggested_value': None,
                'show_accept_button': False
            }
        
        return None
    
    def _get_material_key(
        self,
        material: str = None,
        transport_mode: str = None,
        delivery_term: str = None,
    ) -> Optional[str]:
        """Get material key from material name"""
        if not material:
            return None
            
        material_lower = material.lower()
        
        for key, data in self.MARKET_DATA.items():
            if any(mat.lower() in material_lower for mat in data['materials']):
                return key
        
        return None
    
    def get_general_suggestion(
        self,
        field_name: str,
        field_value: Any,
        context: Dict[str, Any] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get general suggestions that might apply to any field
        
        Args:
            field_name: Name of the field
            field_value: Current value
            context: Additional context (material, transport_mode, etc.)
        
        Returns:
            Dictionary with suggestion data or None
        """
        context = context or {}
        
        # Check for unusually high values (20% higher than "last month")
        if isinstance(field_value, (int, float, Decimal)) and field_value > 0:
            # Mock: 20% higher than "last month" (simulated)
            last_month_value = float(field_value) * 0.8
            if float(field_value) > last_month_value * 1.2:
                return {
                    'type': 'warning',
                    'message': f"{field_name.replace('_', ' ').title()} 20% higher than last month. Proceed?",
                    'suggested_value': None,
                    'show_accept_button': True,
                    'warning_type': 'trend_analysis'
                }
        
        return None


# Singleton instance
ai_suggestions_service = AISuggestionsService()
