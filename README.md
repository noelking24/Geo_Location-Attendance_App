# Geo Location Attendance Application

This  application is designed to mark the attendance of employees based on their geo location. It uses [ipstack](ipstack.com) to locate the employee using the employee device's ip address.

### Steps to build the application:
- Import Dependencies

    - Streamlit
    - Pandas
    - Geopy
- Request IP address
- Use ipstack to get the location of the employee
- Use geopy to calculate the geographical distance between the coordinates of the organization and the employee.
- Set radius of Allowed Premises
- Compare the distance of the employee with the radius of allowed premises to mark attendance
- Store the attendance in a DataFrame

### Dependencies Required:
- Streamlit
- Pandas
- Geopy