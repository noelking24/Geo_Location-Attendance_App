## Import dependencies
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import distance
import requests
import pandas as pd
import datetime

def report():
    st.title("Attendance Report :bar_chart:")
    st.write(st.session_state.df)
    value = len(st.session_state.df)
    st.write(f"Analysis out of {value} days of registry")
    st.write(st.session_state.df['Attendance'].value_counts())

def done():
    st.success("Attendance Entered! :thumbsup:")

def check_attendance(user_location, company_coordinates):
    geolocator = Nominatim(user_agent="geo_attendance_ip")
    #distance between user and company
    distance_coords = distance(user_location, company_coordinates).kilometers
    if  distance_coords <= 5:   #Radius of the premises
        return True

def get_location():
    try:
        # request for ip address
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        data = response.json()
        ip_address = data["ip"]

        # geolocate the ip address
        geo_api_key = "72277575a8e513ee818f8a88c7ef8775"
        url = f"https://api.ipstack.com/{ip_address}?access_key={geo_api_key}"
        response = requests.get(url)
        response.raise_for_status()
        geo_data = response.json()

        lat = geo_data["latitude"]
        lon = geo_data["longitude"]

        return (lat, lon)
    except Exception as e:
        st.error("Error getting location")
        return None


def attendance():
    st.title("Attendance")

    user_location = get_location()
    company_coordinates = (17.501224, 78.639807)
    geolocator = Nominatim(user_agent="geo_attendance_ip")
    distance_coords = distance(user_location, company_coordinates).kilometers
    if user_location:
        st.write(f"You are in the location: {user_location}")

        st.write(f"Company is in the location {company_coordinates}")

        st.write(f"You are {distance_coords}km away from Company premises")
    if 'button' not in st.session_state:
        st.session_state.button='mark'
    if st.session_state.button=='mark':
        if distance_coords<=5:
            if st.button("Present"):
                if check_attendance(user_location, company_coordinates):
                    st.session_state.df.loc[len(st.session_state.df)] = {"Date": datetime.date.today(), "Time": datetime.datetime.now().time(), "Attendance": "Present", "Reason": "-"}
                    st.success("Attendance marked successfully!")
                    st.session_state.instance='done'
                    st.session_state.button='out'
        else:
            st.error("You are outside the allowed area.")

        reason = st.text_input("Reason for leave")
        if st.button("On Leave", key="leave"):
            st.error("Absent Registered with your stated reason!")
            st.session_state.instance='done'
            st.session_state.df.loc[len(st.session_state.df)] = {"Date": datetime.date.today(), "Time": datetime.datetime.now().time(), "Attendance": "Absent", "Reason":reason}
            st.session_state.button='out'
    if st.session_state.button=='out':
        st.success("Attendance Registered Successfully")


def home():
    st.write("## Welcome to")
    st.title(":red[TeamShares Pvt Ltd] 🏢")
    st.header(":red[Geo-Location] based Attendance Registry.")
    st.write("This application gets ip address of employee's device and uses [:red[ipstack]](ipstack.com) to get location of the employee")
    st.write("\n ")
    st.write("## Attendance:")
    st.divider()
    st.write("- This tab allows Employees to enter your attendance registry.\n - Employee need to be in the Company premises to be able to mark 'Present'.\n - If employee is on leave, state reason for leave and click '**On Leave**'.\n - Attendance is stored in the '**Reports**' tab")
    st.write("## Reports")
    st.divider()
    st.write("- This tab shows the report of employee's Attendance Registry.\n - Attendance report (Date, Time, Attendance('Present' or 'Absent'), Reason) are shown in this tab\n - Analysis on Attendance of employee is shown in this tab.")

def welcome():
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["Date", "Time", "Attendance", "Reason"])

    with st.sidebar:
        if st.session_state.u_name == "noeldavid":
            st.sidebar.title(f"Welcome Noel David!")
        if st.session_state.u_name == "daniel":
            st.sidebar.title(f"Welcome Daniel")
        home_button = st.button("Home Page")
        attendance_button = st.button("Attendance")
        report_button = st.button("Reports")

    if 'instance' not in st.session_state:
        st.session_state.instance = ''

    if home_button:
        st.session_state.instance = 'home_page'

    if attendance_button:
        st.session_state.instance = "attendance"
    
    if report_button:
        st.session_state.instance = 'report'
    
    if st.session_state.instance == 'home_page':
        home()
    if st.session_state.instance == "attendance":
        attendance()
    if st.session_state.instance == 'done':
        done()
    if st.session_state.instance == 'report':
        report()

def login():
    users = [
        {"username": "noeldavid", "password": "noel12345"},
        {"username": "daniel", "password": "dan12345"}
    ]
    st.title("Welcome to :red[TeamShares Pvt Ltd]")
    st.header("Login to register you attendance")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        for user in users:
            if user["username"] == username and user["password"]==password:
                if 'u_name' not in st.session_state:
                    st.session_state.u_name = user["username"]
                st.success("Login Successful!")
                st.session_state.pages="welcome"
                break

            else:
                st.error("Enter valid Credentials!")
    return True


def main():
    if 'pages' not in st.session_state:
        st.session_state.pages = "login"
    
    if st.session_state.pages=="login":
        login()
    
    if st.session_state.pages=='welcome':
        welcome()

if __name__ == "__main__":
    main()