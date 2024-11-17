from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import bson


# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client['MYDB1']

# Collections
users = db['users']
vehicles = db['vehicles']
schedules = db['schedules']
bookings = db['bookings']


# User Registration
def register_user(name, email, password, role='user'):
    if users.find_one({"email": email}):
        return "Email already exists."
    hashed_password = generate_password_hash(password)
    users.insert_one({"name": name, "email": email, "password": hashed_password, "role": role})
    return "Registration successful!"


# User Login
def login_user(email, password):
    user = users.find_one({"email": email})
    if user and check_password_hash(user['password'], password):
        return user
    return None


# Add Vehicle
def add_vehicle(vehicle_type, capacity, status):
    vehicles.insert_one({"type": vehicle_type, "capacity": capacity, "status": status})
    return "Vehicle added successfully."


# Add Schedule
def add_schedule(route, departure_time, arrival_time, vehicle_id):
    try:
        object_id = bson.ObjectId(vehicle_id)  # Ensure vehicle_id is a valid ObjectId
    except bson.errors.InvalidId:
        return "Invalid vehicle ID format."

    schedules.insert_one({
        "route": route,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "vehicle_id": object_id
    })
    return "Schedule added successfully."


# Book Schedule
def book_schedule(user_id, schedule_id):
    try:
        user_object_id = bson.ObjectId(user_id)  # Validate user_id
        schedule_object_id = bson.ObjectId(schedule_id)  # Validate schedule_id
    except bson.errors.InvalidId:
        return "Invalid ID format for user or schedule."

    booking_date = datetime.now().strftime('%Y-%m-%d')
    bookings.insert_one({
        "user_id": user_object_id,
        "schedule_id": schedule_object_id,
        "booking_date": booking_date,
        "status": "confirmed"
    })
    return "Booking confirmed."


# Example Debugging Utility Function
def debug_collection(collection_name):
    collection = db[collection_name]
    for document in collection.find():
        print(document)


# Example Test Calls
if __name__ == "__main__":
    # Register a new user
    print(register_user("John Doe", "john@example.com", "password123"))

    # Login a user
    user = login_user("john@example.com", "password123")
    if user:
        print(f"Logged in user: {user['name']}")

    # Add a vehicle
    print(add_vehicle("Bus", 50, "available"))

    # Add a schedule (use a valid ObjectId for vehicle_id from your vehicles collection)
    print(add_schedule("Route A", "2024-11-16 09:00:00", "2024-11-16 12:00:00", "64f9d0e8e418bfa123456789"))

    # Book a schedule (use valid ObjectIds for user_id and schedule_id from your users and schedules collections)
    print(book_schedule("64f9d0e8e418bfa123456789", "64f9d0e8e418bfa987654321"))
