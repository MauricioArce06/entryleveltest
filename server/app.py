from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
from datetime import datetime
from dataclasses import dataclass
from typing import List

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

client = MongoClient("mongodb://localhost:27017/")
db = client['Python']
collection = db['languages']  # Make sure the collection name is 'users'


@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str  # Change from 'user' to 'username' for clarity
    password: str
    roles: List[str]  # Changed from individual boolean flags to a list of roles
    preferences: UserPreferences
    active: bool = True
    created_at: datetime = None
    last_updated_at: datetime = None

@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

from datetime import datetime, timezone
from flask import request, jsonify

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
                
        user_data = User(
            username=data['username'],
            password=data['password'],
            roles=data['roles'],
            preferences=data['preferences'],
            active=data.get('is_user_active', True),
            created_at=datetime.now(timezone.utc),  # Usa UTC
            last_updated_at=datetime.now(timezone.utc)  # Usa UTC
        )

        user_dict = user_data.__dict__
        result = collection.insert_one(user_dict)
        user_dict['_id'] = str(result.inserted_id)
        return jsonify(user_dict), 201
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400
    
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user['_id'] = str(user['_id'])
    return jsonify(user)

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        data['last_updated_at'] = datetime.utcnow()  # Use UTC for the date and time
        data.pop('_id', None)  # Remove _id if it exists
        
        # Prepare the user data for update
        update_data = {
            "username": data['username'],
            "password": data['password'],
            "roles": data['roles'],
            "preferences": data['preferences'],
            "active": data.get('is_user_active', True),
            "last_updated_at": data['last_updated_at'],
        }

        result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        
        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404
        
        # Return the updated user
        updated_user = collection.find_one({"_id": ObjectId(user_id)})
        if updated_user:
            updated_user['_id'] = str(updated_user['_id'])  # Convert ObjectId to string
            return jsonify(updated_user), 200  # Return the updated user

    except Exception as e:
        print(str(e))  # Print the error in the console for debugging
        return jsonify({"error": str(e)}), 400

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"result": "deleted"})

if __name__ == '__main__':
    app.run(debug=True)
