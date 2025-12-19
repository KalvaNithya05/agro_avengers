class ZoneMapper:
    """
    Maps Indian States to Agro-Climatic Zones (ACZ).
    Based on Planning Commission of India's 15 ACZ classification.
    """
    def __init__(self):
        self.state_zone_map = {
            'jammu and kashmir': 'Western Himalayan Region',
            'himachal pradesh': 'Western Himalayan Region',
            'uttarakhand': 'Western Himalayan Region',
            'punjab': 'Trans-Gangetic Plains',
            'haryana': 'Trans-Gangetic Plains',
            'delhi': 'Trans-Gangetic Plains',
            'uttar pradesh': 'Upper Gangetic Plains',
            'bihar': 'Middle Gangetic Plains',
            'west bengal': 'Lower Gangetic Plains',
            'assam': 'Eastern Himalayan Region',
            'sikkim': 'Eastern Himalayan Region',
            'odisha': 'East Coast Plains and Hills',
            'andhra pradesh': 'East Coast Plains and Hills',
            'tamil nadu': 'Southern Plateau and Hills',
            'telangana': 'Southern Plateau and Hills',
            'karnataka': 'Southern Plateau and Hills',
            'kerala': 'West Coast Plains and Ghats',
            'goa': 'West Coast Plains and Ghats',
            'maharashtra': 'Western Plateau and Hills',
            'gujarat': 'Gujarat Plains and Hills',
            'rajasthan': 'Western Dry Region',
            'madhya pradesh': 'Central Plateau and Hills',
            'chhattisgarh': 'Eastern Plateau and Hills',
            'jharkhand': 'Eastern Plateau and Hills'
        }

    def get_zone(self, state):
        """
        Get the Agro-Climatic Zone for a given state.
        """
        if not state:
            return "Unknown"
        return self.state_zone_map.get(state.lower().strip(), "Unknown Zone")

    def is_crop_suitable_for_zone(self, crop, zone):
        """
        Optional: Check if a crop is traditionally grown in this zone.
        This can be expanded with a database of Zone->Crop mappings.
        """
        # Placeholder logic
        return True
