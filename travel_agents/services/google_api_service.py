"""Google API service for travel planning."""
import os
from typing import List, Dict, Optional
import googlemaps
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GoogleAPIService:
    """Service to interact with Google Maps and Places APIs."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Google API service with API key."""
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set")
        self.client = googlemaps.Client(key=self.api_key)
        logger.info("Google API Service initialized")

    def search_places(self, query: str, location: str, radius: int = 50000) -> List[Dict]:
        """
        Search for places using Google Places API.
        
        Args:
            query: Search query (e.g., "restaurants", "hotels")
            location: Location to search (e.g., "Paris, France")
            radius: Search radius in meters
            
        Returns:
            List of place results
        """
        try:
            geocode_result = self.client.geocode(address=location)
            if not geocode_result:
                logger.warning(f"Could not geocode location: {location}")
                return []

            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']

            places_result = self.client.places_nearby(
                location=(lat, lng),
                radius=radius,
                keyword=query,
                type="point_of_interest"
            )

            results = places_result.get('results', [])
            return results
        except Exception as e:
            logger.error(f"Error searching places: {str(e)}")
            return []

    def get_distance_matrix(
        self,
        origins: List[str],
        destinations: List[str],
        mode: str = "driving"
    ) -> Dict:
        """
        Get distance and duration matrix between locations.
        
        Args:
            origins: List of origin addresses
            destinations: List of destination addresses
            mode: Travel mode ("driving", "walking", "transit", "bicycling")
            
        Returns:
            Distance matrix result
        """
        try:
            matrix = self.client.distance_matrix(
                origins=origins,
                destinations=destinations,
                mode=mode
            )
            return matrix
        except Exception as e:
            logger.error(f"Error getting distance matrix: {str(e)}")
            return {}

    def get_place_details(self, place_id: str) -> Dict:
        """
        Get detailed information about a place.
        
        Args:
            place_id: Google Places ID
            
        Returns:
            Place details
        """
        try:
            place_details = self.client.place(place_id=place_id)
            return place_details.get('result', {})
        except Exception as e:
            logger.error(f"Error getting place details: {str(e)}")
            return {}

    def geocode_location(self, location: str) -> Optional[Dict]:
        """
        Get coordinates for a location.
        
        Args:
            location: Location address
            
        Returns:
            Geocoding result with coordinates
        """
        try:
            result = self.client.geocode(address=location)
            if result:
                return result[0]
            return None
        except Exception as e:
            logger.error(f"Error geocoding location: {str(e)}")
            return None

    def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        """
        Get address from coordinates.
        
        Args:
            lat: Latitude
            lng: Longitude
            
        Returns:
            Address string
        """
        try:
            result = self.client.reverse_geocode((lat, lng))
            if result:
                return result[0]['formatted_address']
            return None
        except Exception as e:
            logger.error(f"Error reverse geocoding: {str(e)}")
            return None

    def get_attractions(self, location: str, radius: int = 50000) -> List[Dict]:
        """
        Get attractions at a location.
        
        Args:
            location: Location to search
            radius: Search radius in meters
            
        Returns:
            List of attractions
        """
        return self.search_places("attractions", location, radius)

    def get_restaurants(self, location: str, radius: int = 50000) -> List[Dict]:
        """Get restaurants at a location."""
        return self.search_places("restaurants", location, radius)

    def get_hotels(self, location: str, radius: int = 50000) -> List[Dict]:
        """Get hotels at a location."""
        return self.search_places("hotels", location, radius)

    def get_weather_info(self, location: str) -> Optional[Dict]:
        """
        Get elevation and general location info (weather would require separate API).
        
        Args:
            location: Location to get info for
            
        Returns:
            Location information
        """
        try:
            geocode_result = self.geocode_location(location)
            if geocode_result:
                return {
                    'location': geocode_result['formatted_address'],
                    'coordinates': geocode_result['geometry']['location'],
                    'place_id': geocode_result['place_id']
                }
            return None
        except Exception as e:
            logger.error(f"Error getting weather info: {str(e)}")
            return None
