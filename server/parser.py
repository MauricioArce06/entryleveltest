import json
from dataclasses import dataclass
from pymongo import MongoClient
from datetime import datetime

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str  # Change from 'user' to 'username' for clarity
    password: str
    roles: list  # Changed from individual boolean flags to a list of roles
    preferences: UserPreferences
    active: bool = True
    created_at: datetime = None
    last_updated_at: datetime = None

def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
        return None

def insert_data_to_mongo(users):
    try:
        client = MongoClient("mongodb://localhost:27017/")  # Adjust URI as needed
        db = client['Python']  # Change the database name as required
        collection = db['languages']  # Change the collection name to 'users'

        for user in users:
            created_ts = datetime.fromisoformat(user['created_at'].replace("Z", "+00:00")).timestamp()
            
            # Map roles based on the boolean flags
            roles = []
            if user.get('is_user_admin', False):
                roles.append('Admin')
            if user.get('is_user_manager', False):
                roles.append('Manager')
            if user.get('is_user_tester', False):
                roles.append('Tester')

            # Create UserPreferences
            preferences = UserPreferences(timezone=user.get('user_timezone', None))

            # Create User instance
            user_data = User(
                username=user['user'],
                password=user['password'],
                roles=roles,
                preferences=preferences,
                active=user.get('is_user_active', True),
                created_at=datetime.fromtimestamp(created_ts),
                last_updated_at=datetime.now()  # Assign current date and time
            )

            user_dict = user_data.__dict__
            user_dict['preferences'] = user_dict['preferences'].__dict__  # Convert preferences to a dict
            collection.insert_one(user_dict)

        print("Data imported successfully.")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")

if __name__ == "__main__":
    data = load_data("users.json")  # Ensure the JSON file is in the same directory
    if data:
        insert_data_to_mongo(data['users'])
