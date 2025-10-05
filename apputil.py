# your code here ...
import requests
import pandas as pd
from typing import List, Dict, Optional, Any


class Genius:
    """
    A Python class to interact with the Genius API.
    Handles artist searches and data retrieval.
    """
    
    def __init__(self, access_token: str):
        """
        Initialize the Genius API client with an access token.
        
        Args:
            access_token (str): The Genius API access token
        """
        self.access_token = access_token
        self.base_url = "https://api.genius.com"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Helper method to make API requests.
        
        Args:
            endpoint (str): The API endpoint to call
            params (dict, optional): Query parameters for the request
        
        Returns:
            dict: The JSON response from the API
        
        Raises:
            Exception: If the API request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def _search_artist(self, search_term: str) -> Dict:
        """
        Helper method to search for an artist by name.
        
        Args:
            search_term (str): The artist name to search for
        
        Returns:
            dict: The search results from the API
        """
        params = {"q": search_term}
        return self._make_request("/search", params)
    
    def _extract_artist_id(self, search_data: Dict) -> Optional[int]:
        """
        Helper method to extract the primary artist ID from search results.
        
        Args:
            search_data (dict): The search results from the API
        
        Returns:
            int or None: The artist ID if found, None otherwise
        """
        try:
            # Get the first hit from search results
            hits = search_data.get("response", {}).get("hits", [])
            
            if not hits:
                return None
            
            # Extract the primary artist from the first hit
            first_hit = hits[0]
            primary_artist = first_hit.get("result", {}).get("primary_artist", {})
            
            return primary_artist.get("id")
        except (KeyError, IndexError):
            return None
    
    def get_artist(self, search_term: str) -> Dict:
        """
        Get detailed information about an artist based on a search term.
        
        This method:
        1. Searches for the artist using the search term
        2. Extracts the primary artist ID from the first hit
        3. Fetches detailed artist information using the artist ID
        
        Args:
            search_term (str): The artist name to search for
        
        Returns:
            dict: The artist information from the API
        
        Raises:
            Exception: If no artist is found or API request fails
        """
        # Step 1: Search for the artist
        search_results = self._search_artist(search_term)
        
        # Step 2: Extract the artist ID
        artist_id = self._extract_artist_id(search_results)
        
        if not artist_id:
            raise Exception(f"No artist found for search term: {search_term}")
        
        # Step 3: Get artist information using the artist ID
        artist_endpoint = f"/artists/{artist_id}"
        artist_data = self._make_request(artist_endpoint)
        
        return artist_data
    
    def get_artists(self, search_terms: List[str]) -> pd.DataFrame:
        """
        Get information about multiple artists and return as a DataFrame.
        
        Args:
            search_terms (list): A list of artist names to search for
        
        Returns:
            pandas.DataFrame: A DataFrame with columns:
                - search_term: The original search term
                - artist_name: The artist's name from the API
                - artist_id: The Genius artist ID
                - followers_count: Number of followers (if available)
        """
        results = []
        
        for search_term in search_terms:
            try:
                # Get artist data
                artist_data = self.get_artist(search_term)
                artist_info = artist_data.get("response", {}).get("artist", {})
                
                # Extract relevant information
                result = {
                    "search_term": search_term,
                    "artist_name": artist_info.get("name", ""),
                    "artist_id": artist_info.get("id", ""),
                    "followers_count": artist_info.get("followers_count", 0)
                }
                
                results.append(result)
                
            except Exception as e:
                # If an error occurs, add a row with empty/default values
                print(f"Error fetching data for '{search_term}': {str(e)}")
                result = {
                    "search_term": search_term,
                    "artist_name": "",
                    "artist_id": "",
                    "followers_count": 0
                }
                results.append(result)
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        return df


# Example usage and testing functions
def test_genius_class():
    """
    Test function to demonstrate the Genius class functionality.
    Replace 'YOUR_ACCESS_TOKEN' with your actual Genius API access token.
    """
    
    # Initialize the Genius object
    access_token = "YOUR_ACCESS_TOKEN"  # Replace with your actual token
    genius = Genius(access_token=access_token)
    
    print("Testing Exercise 1: Initialization")
    print(f"Access token stored: {'Yes' if genius.access_token else 'No'}")
    print()
    
    print("Testing Exercise 2: get_artist()")
    print("-" * 40)
    try:
        artist_data = genius.get_artist("Radiohead")
        artist_info = artist_data.get("response", {}).get("artist", {})
        print(f"Artist Name: {artist_info.get('name')}")
        print(f"Artist ID: {artist_info.get('id')}")
        print(f"Followers: {artist_info.get('followers_count', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    print()
    
    print("Testing Exercise 3: get_artists()")
    print("-" * 40)
    try:
        artists_df = genius.get_artists(['Rihanna', 'Tycho', 'Seal', 'U2'])
        print(artists_df.to_string())
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Run tests if this file is executed directly
    print("Genius API Class Implementation Test")
    print("=" * 40)
    test_genius_class()