from config import MONGO_URL, MONGO_DB_NAME
from pymongo import MongoClient
from pydantic import BaseModel, Field
from config import MONGO_URL, MONGO_DB_NAME, MONGO_COLLECTION_USERS
from passlib.context import CryptContext


client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_USERS]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_user_data(username):
    """
    Retrieve user data from MongoDB collection.
    """
    try:
        # Find the user data in the collection
        user_data = collection.find_one({"username": username})
        if user_data:
            return user_data
        else:
            print("User not found")
            return None
    except Exception as e:
        print(f"Error retrieving user data: {e}")
        return None

def insert_user_data(username, pwd):
    """
    Insert user data into MongoDB collection.
    """

    pwd_hashed = pwd_context.hash(pwd)

    message = {
        'username': username,
        'password': pwd_hashed
    }
    user_exists = get_user_data(username)
    
    if user_exists is None:
        print("User does not exist, inserting new user data.")
        try:
            # Insert the user data into the collection
            result = collection.insert_one(message)
            print(f"User data inserted with id: {result.inserted_id}")
        except Exception as e:
            print(f"Error inserting user data: {e}")
    else:
        kb_input = input("User already exists, updating password ? (y/n)")
        if kb_input.lower() == 'y':
            print("Updating password for existing user.")
            try:
                # Update the password for the existing user
                collection.update_one({"username": username}, {"$set": {"password": pwd_hashed}})
                print(f"Password updated for user: {username}")
            except Exception as e:
                print(f"Error updating password: {e}")
        else:
            print("User data not updated.")



if __name__ == "__main__":
    # Example usage
    username = "admin"
    password = "admin"
    
    # Insert user data
    insert_user_data(username, password)
    hashed_pwd = collection.find_one({"username": username}).get('password')
    print(hashed_pwd)
    print(pwd_context.verify(password, hashed_pwd))
