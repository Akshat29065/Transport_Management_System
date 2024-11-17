import streamlit as st
from app import register_user, login_user, add_vehicle, add_schedule, book_schedule
from app import vehicles, schedules, bookings
from bson.objectid import ObjectId
from bson.errors import InvalidId

st.title("Transport Management System")

# Sidebar for Navigation
st.sidebar.title("Navigation")
options = ["Home", "Register", "Login", "Add Vehicle (Admin)", "Add Schedule (Admin)", "Book Schedule"]
choice = st.sidebar.selectbox("Choose Action", options)

# Session state to track the logged-in user
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Home Page
if choice == "Home":
    st.write("Welcome to the Transport Management System!")
    if st.session_state['user']:
        st.write(f"Logged in as {st.session_state['user']['name']}")
    else:
        st.write("Please log in or register to continue.")

# Registration Page
elif choice == "Register":
    st.subheader("User Registration")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Register"):
        message = register_user(name, email, password, role)
        st.success(message)

# Login Page
elif choice == "Login":
    st.subheader("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state['user'] = user
            st.success(f"Logged in as {user['name']}")
        else:
            st.error("Invalid email or password.")

# Add Vehicle (Admin only)
elif choice == "Add Vehicle (Admin)" and st.session_state['user'] and st.session_state['user']['role'] == 'admin':
    st.subheader("Add New Vehicle")
    vehicle_type = st.text_input("Vehicle Type")
    capacity = st.number_input("Capacity", min_value=1)
    status = st.selectbox("Status", ["Available", "Unavailable"])

    if st.button("Add Vehicle"):
        message = add_vehicle(vehicle_type, capacity, status)
        st.success(message)

# Add Schedule (Admin only)
elif choice == "Add Schedule (Admin)" and st.session_state['user'] and st.session_state['user']['role'] == 'admin':
    st.subheader("Add New Schedule")
    route = st.text_input("Route")
    departure_time = st.text_input("Departure Time (YYYY-MM-DD HH:MM)")
    arrival_time = st.text_input("Arrival Time (YYYY-MM-DD HH:MM)")
    vehicle_id = st.selectbox("Vehicle", [(str(v["_id"]), v["type"]) for v in vehicles.find()])  # Ensure _id is a string

    if st.button("Add Schedule"):
        message = add_schedule(route, departure_time, arrival_time, vehicle_id)
        st.success(message)

# Book Schedule (User only)
elif choice == "Book Schedule" and st.session_state['user']:
    st.subheader("Book a Schedule")
    schedule_options = [(str(s["_id"]), s["route"]) for s in schedules.find()]  # Convert _id to string
    selected_schedule = st.selectbox("Schedule", schedule_options)

    if st.button("Book"):
        # Ensure the ID is extracted correctly
        schedule_id = selected_schedule[0]  # Get the string version of _id
        try:
            # Debugging: Check the value and type
            st.write(f"Selected Schedule ID: {schedule_id}, Type: {type(schedule_id)}")
            
            # Convert to ObjectId
            schedule_id_obj = ObjectId(schedule_id)
            message = book_schedule(st.session_state['user']['_id'], schedule_id_obj)
            st.success(message)
        except InvalidId:
            st.error("Invalid schedule ID. Please select a valid schedule.")
        except TypeError as e:
            st.error(f"TypeError: {e}")


# Logout Option
if st.sidebar.button("Logout"):
    st.session_state['user'] = None
    st.success("Logged out successfully.")