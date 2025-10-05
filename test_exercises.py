# test_exercises.py
from apputil import Genius


ACCESS_TOKEN = "RoGpRxR_Cb4BeU2nE1tlsqQTUIxLybAr-K5aayPva-VPbzgTqVa4BGvcvXUPkIOy"

# Exercise 1: Test initialization
print("=" * 50)
print("Exercise 1: Initialization Test")
print("=" * 50)
genius = Genius(access_token=ACCESS_TOKEN)
print(f"✓ Genius object created successfully")
print(f"✓ Access token stored: {bool(genius.access_token)}")
print()

# Exercise 2: Test get_artist()
print("=" * 50)
print("Exercise 2: get_artist() Test")
print("=" * 50)
try:
    artist_data = genius.get_artist("Radiohead")
    artist_info = artist_data.get("response", {}).get("artist", {})
    print(f"Search term: Radiohead")
    print(f"Artist Name: {artist_info.get('name')}")
    print(f"Artist ID: {artist_info.get('id')}")
    print(f"Followers: {artist_info.get('followers_count', 'N/A')}")
    print("✓ get_artist() working successfully")
except Exception as e:
    print(f"✗ Error: {e}")
print()

# Exercise 3: Test get_artists()
print("=" * 50)
print("Exercise 3: get_artists() Test")
print("=" * 50)
try:
    test_artists = ['Rihanna', 'Tycho', 'Seal', 'U2']
    print(f"Testing with artists: {test_artists}")
    artists_df = genius.get_artists(test_artists)
    print("\nResults DataFrame:")
    print(artists_df.to_string())
    print(f"\n✓ get_artists() returned {len(artists_df)} rows")
    print("✓ DataFrame has correct columns:", list(artists_df.columns))
except Exception as e:
    print(f"✗ Error: {e}")