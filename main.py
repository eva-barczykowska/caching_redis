import redis
import requests
import json
import time

# this will only run if docker is up and Redis is running, see README for more details.
# Step 1: Connect to the Redis server
# The decode_responses=True flag ensures that Redis returns strings, not bytes[5].
try:
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    # Ping the server to check the connection
    r.ping()
    print("Successfully connected to Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    exit()

def get_user_data(user_id: int):
    """
    Retrieves user data, using Redis as a cache.
    """
    # Define a unique key for this user's data in the cache[1]
    cache_key = f"user:{user_id}"

    # Step 2: Check if the data is in the cache
    cached_user = r.get(cache_key) # redis get the value associated with the key cache_key

    if cached_user:
        # --- Cache Hit ---
        print(f"Cache hit for user {user_id}.")
        # The data is stored as a JSON string, so we parse it back into a dictionary
        return json.loads(cached_user)
    else:
        # --- Cache Miss ---
        print(f"Cache miss for user {user_id}. Fetching from API.")
        try:
            # Step 3: Fetch data from the external API
            response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            user_data = response.json()

            # Step 4: Store the fetched data in Redis with an expiration time
            # We use setex (SET with EXpiration) to automatically remove the key after 30 seconds[1][3].
            # The data is converted to a JSON string for storage.
            r.setex(cache_key, 30, json.dumps(user_data))

            return user_data

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

# --- Demonstration ---
if __name__ == "__main__":
    USER_ID = 1

    # First call: Should be a "cache miss"
    print("--- First Request ---")
    user = get_user_data(USER_ID)
    if user:
        print(f"Fetched user: {user.get('name')}, Email: {user.get('email')}")

    print("\n" + "="*30 + "\n")

    # Second call (immediately after): Should be a "cache hit"
    print("--- Second Request (within 30s) ---")
    user = get_user_data(USER_ID)
    if user:
        print(f"Fetched user from cache: {user.get('name')}, Email: {user.get('email')}")

    print("\n" + "="*30 + "\n")

    # Wait for the cache to expire
    print("Waiting for 35 seconds for the cache to expire...")
    time.sleep(35)

    # Third call (after expiration): Should be a "cache miss" again
    print("\n--- Third Request (after 30s) ---")
    user = get_user_data(USER_ID)
    if user:
        print(f"Fetched user: {user.get('name')}, Email: {user.get('email')}")
