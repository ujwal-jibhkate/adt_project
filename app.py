import streamlit as st
import sqlite3
import altair as alt
import pandas as pd
import os, base64
from backend import create_incident, read_incidents, update_incident, delete_incident, search_incident
import uuid


# Function to display the latest 10 incidents
def display_incidents():
    """
    Display the latest 10 incidents in the database.

    This function will show the following details of each incident:
        - Call Key
        - Priority
        - Description
        - Call Time (Date and Time)

    If there are no incidents in the database, it will display a message saying "No incidents found."

    It will not show the delete button in this section anymore. If you want to delete an incident, it will now be handled through the "Search Incidents" tab.
    """
    st.subheader("View Latest 10 Incidents")
    incidents = read_incidents()

    if not incidents:
        st.write("No incidents found.")
    else:
        for incident in incidents:
            # Access columns by name (incident is a sqlite3.Row object)
            call_time = incident['call_date_time']
            st.write(f"**Call Key**: {incident['call_key']} - **Priority**: {incident['priority']} - **Description**: {incident['description']}")
            st.write(f"**Call Time**: {call_time}")  # Added date and time of the incident
            st.markdown("---")
            # Removed the delete button from the "View Latest 10 Incidents" section
            # If you want to delete an incident, it will now be handled through the "Search Incidents" tab

# Function to add a new incident
def add_incident():
    """
    Display a form to add a new incident to the database.

    This function provides a Streamlit form for users to enter details of a new incident,
    including record ID, call date and time, priority, description, call number, incident
    location ID, reporter location ID, and jurisdiction ID. Upon form submission, a new
    incident is created with a unique call key and added to the database. A success message
    is displayed after the incident is successfully added.
    """

    st.subheader("Add New Incident")
    with st.form(key='add_incident_form'):
        record_id = st.text_input("Record ID")
        call_date_time = st.text_input("Call Date and Time (YYYY/MM/DD HH:MM:SS+00)")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Non-Emergency"])
        description = st.text_area("Description")
        call_number = st.text_input("Call Number")
        incident_location_id = st.number_input("Incident Location ID", min_value=1)
        reporter_location_id = st.number_input("Reporter Location ID", min_value=1)
        jurisdiction_id = st.number_input("Jurisdiction ID", min_value=1)
        
        submit_button = st.form_submit_button(label="Add Incident")
        
        if submit_button:
            # Generate call_key automatically
            call_key = str(uuid.uuid4())
            # Create the incident
            create_incident(call_key, record_id, call_date_time, priority, description, call_number, incident_location_id, reporter_location_id, jurisdiction_id)
            
            # Show success message using Streamlit's default format
            st.success(f"Incident has been successfully added with the Call Key: **{call_key}**")


# Function to update an incident
def update_existing_incident():
    """
    Display a form to update an existing incident in the database.

    This function provides a Streamlit form for users to enter a call key to update an incident.
    Upon form submission, the incident is updated with new priority and description, and a success
    message is displayed after the incident is successfully updated.

    If no incident is found with the given call key, an error message is displayed.
    """
    
    st.subheader("Update Incident")
    call_key = st.text_input("Enter Call Key to Update")
    
    if call_key:
        incidents = search_incident(call_key=call_key)
        
        if incidents:
            incident = incidents[0]  # Since call_key is unique, we can assume only one result
            new_priority = st.selectbox("Priority", [incident["priority"], "Low", "Medium", "High", "Non-Emergency"])
            new_description = st.text_area("Description", value=incident["description"])
            
            if st.button(f"Update {call_key}"):
                update_incident(call_key, priority=new_priority, description=new_description)
                st.success(f"Incident {call_key} updated successfully!")
        else:
            st.error(f"No incident found with call key: {call_key}")

# Function to search incidents by call_key and display the result
def search_incident_form():
    """
    Display a form to search for incidents by call_key and display the result.
    
    This function provides a Streamlit form for users to enter a call key to search for an incident.
    Upon form submission, the incident is searched in the database and the result is displayed in a
    clean format using Streamlit's default layout.

    If no incident is found with the given call key, an error message is displayed.

    Additionally, a delete button is provided to delete the incident found.
    """
    st.subheader("Search Incidents by Call Key")
    call_key = st.text_input("Enter Call Key")

    if call_key:
        results = search_incident(call_key=call_key)
        
        if results:
            # Use Streamlit default layout for displaying search results in a readable format
            for incident in results:
                # Display the result in a clean format
                st.markdown("### Incident Details")
                st.write(f"**Call Key**: {incident['call_key']}")
                st.write(f"**Priority**: {incident['priority']}")
                st.write(f"**Description**: {incident['description']}")
                st.write(f"**Call Number**: {incident['call_number']}")
                st.write(f"**Incident Location ID**: {incident['incident_location_id']}")
                st.write(f"**Reporter Location ID**: {incident['reporter_location_id']}")
                st.write(f"**Jurisdiction ID**: {incident['jurisdiction_id']}")
                st.write(f"**Call Date and Time**: {incident['call_date_time']}")
                
                # Add a delete button to delete the incident found
                if st.button(f"Delete Incident {incident['call_key']}"):
                    delete_incident(incident['call_key'])
                    st.success(f"Incident {incident['call_key']} deleted successfully!")
        else:
            st.error(f"No incidents found with call key: {call_key}")

# Function to display the Dashboard with interactive Altair charts
def dashboard():
    """
    Displays a dashboard with interactive Altair charts for incident analysis.

    The dashboard consists of six charts:

    1. Priority Distribution (Bar Chart)
    2. Distribution of Calls by Hour of Day (Line Chart)
    3. Number of Calls by District (Bar Chart)
    4. Number of Calls by Neighborhood (Bar Chart)
    5. Total Calls by Priority Over Time (Line Chart)
    6. Calls by Location (Bar Chart)

    The charts are interactive, allowing users to hover over the data points to see more
    information about each incident.

    This function uses the Altair library to create the charts and Streamlit to display them in a
    dashboard layout.

    :return: None
    """
    st.subheader("Dashboard: Incident Analysis")

    # Connect to the database and fetch data for the charts
    conn = sqlite3.connect('database/911_Call_Data.db')
    df_calls = pd.read_sql_query("SELECT * FROM Calls;", conn)

    # Plot 1: Priority Distribution (Bar Chart)
    st.subheader("Priority Distribution")
    priority_counts = df_calls['priority'].value_counts().reset_index()
    priority_counts.columns = ['Priority', 'Count']

    priority_chart = alt.Chart(priority_counts).mark_bar().encode(
        x='Priority:N',
        y='Count:Q',
        color='Priority:N'
    ).properties(
        title='Priority Distribution'
    ).interactive()  # Add interactivity to the chart
    st.altair_chart(priority_chart, use_container_width=True)

    # Plot 2: Distribution of Calls by Hour of Day (Line Chart)
    st.subheader("Distribution of Calls by Hour of Day")
    df_calls['call_date_time'] = pd.to_datetime(df_calls['call_date_time'], errors='coerce')
    df_calls = df_calls.dropna(subset=['call_date_time'])
    df_calls['hour'] = df_calls['call_date_time'].dt.hour

    df_hourly = df_calls.groupby('hour').size().reset_index(name="count")

    hour_chart = alt.Chart(df_hourly).mark_line().encode(
        x='hour:O',
        y='count:Q',
        tooltip=['hour:O', 'count:Q']
    ).properties(
        title="Calls by Hour of Day"
    ).interactive()  # Add interactivity to the chart
    st.altair_chart(hour_chart, use_container_width=True)

    # Plot 3: Number of Calls by District (Bar Chart)
    st.subheader("Number of Calls by District")
    query_district = """
    SELECT J.district, COUNT(*) as count
    FROM Calls C
    JOIN Jurisdictions J ON C.jurisdiction_id = J.jurisdiction_id
    GROUP BY J.district;
    """
    df_district = pd.read_sql_query(query_district, conn)

    district_chart = alt.Chart(df_district).mark_bar().encode(
        x='district:N',
        y='count:Q',
        color='district:N'
    ).properties(
        title="Number of Calls by District"
    ).interactive()  # Add interactivity to the chart
    st.altair_chart(district_chart, use_container_width=True)

    # Plot 4: Number of Calls by Neighborhood (Bar Chart)
    st.subheader("Number of Calls by Neighborhood")
    query_neighborhood = """
    SELECT L.neighborhood, COUNT(*) AS count
    FROM Calls C
    JOIN Locations L ON C.reporter_location_id = L.location_id
    GROUP BY L.neighborhood;
    """
    df_neighborhood = pd.read_sql_query(query_neighborhood, conn)

    neighborhood_chart = alt.Chart(df_neighborhood).mark_bar().encode(
        x='neighborhood:N',
        y='count:Q',
        color='neighborhood:N'
    ).properties(
        title="Number of Calls by Reporter Neighborhood"
    ).interactive()  # Add interactivity to the chart
    st.altair_chart(neighborhood_chart, use_container_width=True)

    # Plot 5: Total Calls by Priority Over Time (Line Chart)
    st.subheader("Total Calls by Priority Over Time")
    df_calls['date'] = df_calls['call_date_time'].dt.date
    df_priority_over_time = df_calls.groupby(['date', 'priority']).size().reset_index(name='count')

    priority_time_chart = alt.Chart(df_priority_over_time).mark_line().encode(
        x='date:T',
        y='count:Q',
        color='priority:N',
        tooltip=['date:T', 'count:Q', 'priority:N']
    ).properties(
        title="Total Calls by Priority Over Time"
    ).interactive()  # Add interactivity to the chart
    st.altair_chart(priority_time_chart, use_container_width=True)

    # Plot 6: Calls by Location (Bar Chart)
    st.subheader("Calls by Location")
    query_location = """
    SELECT L.location_id, COUNT(*) AS count
    FROM Calls C
    JOIN Locations L ON C.reporter_location_id = L.location_id
    GROUP BY L.location_id;
    """
    df_location = pd.read_sql_query(query_location, conn)

    location_chart = alt.Chart(df_location).mark_bar().encode(
        x='location_id:N',
        y='count:Q',
        color='location_id:N'
    ).properties(
        title="Number of Calls by Location"
    ).interactive()  # Add interactivity to the chart
    st.altair_chart(location_chart, use_container_width=True)

    conn.close()

st.title("911 Incident Management System")
# Streamlit sidebar for navigation
menu = ["Dashboard", "View Latest 10 Incidents", "Add Incident", "Update Incident", "Search & Delete Incidents"]
choice = st.sidebar.selectbox("Select an Option", menu, index=0)  # Set "Dashboard" as the default option

if choice == "Dashboard":
    dashboard()  # Load the dashboard
elif choice == "View Latest 10 Incidents":
    display_incidents()
elif choice == "Add Incident":
    add_incident()
elif choice == "Update Incident":
    update_existing_incident()
elif choice == "Search & Delete Incidents":
    search_incident_form()
