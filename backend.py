import sqlite3
import uuid

# Function to generate a unique call_key
def generate_unique_call_key():
    """
    Generate a unique call_key for a new incident.

    This function generates a unique string (a UUID) to serve as the call_key for a new incident.

    Returns:
        str: A unique call_key (a UUID) in string format.
    """
    return str(uuid.uuid4())  # Generate a unique UUID and convert it to a string

# Create Incident (Insert New Incident)
def create_incident(call_key=None, record_id=None, call_date_time=None, priority=None, description=None, 
                    call_number=None, incident_location_id=None, reporter_location_id=None, jurisdiction_id=None):
    """
    Create a new incident in the database.

    This function inserts a new incident into the Calls table in the database. If a call_key is not provided, a unique call_key is generated using the generate_unique_call_key function.

    Parameters:
    - call_key (str, optional): The unique identifier for the incident to create. If not provided, a unique call_key is generated.
    - record_id (str): The record ID for the incident.
    - call_date_time (str): The date and time of the call in the format "YYYY/MM/DD HH:MM:SS+00".
    - priority (str): The priority of the incident (Low, Medium, High, Non-Emergency).
    - description (str): The description of the incident.
    - call_number (str): The call number for the incident.
    - incident_location_id (int): The ID of the location where the incident occurred.
    - reporter_location_id (int): The ID of the location of the reporter.
    - jurisdiction_id (int): The ID of the jurisdiction where the incident occurred.

    Returns:
    - str: The generated or provided call_key.
    """
    if not call_key:
        call_key = generate_unique_call_key()

    with sqlite3.connect('database/911_Call_Data.db') as conn:
        conn.row_factory = sqlite3.Row  # Ensure we can access columns by name
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Calls (call_key, record_id, call_date_time, priority, description, call_number, 
                               incident_location_id, reporter_location_id, jurisdiction_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (call_key, record_id, call_date_time, priority, description, call_number, incident_location_id, 
              reporter_location_id, jurisdiction_id))
        
        conn.commit()  # Save changes to the database
    
    return call_key  # Return the generated or provided call_key

# Read the latest 10 Incidents (Fetch Latest 10 Incidents)
def read_incidents():
    """
    Fetch the latest 10 incidents from the database.

    This function fetches the latest 10 incidents from the Calls table in the database, ordered by call_date_time in descending order (newest first).

    Returns:
        list of sqlite3.Row: A list of the latest 10 incidents, where each incident is a dictionary-like object with column names as keys.
    """
    
    with sqlite3.connect('database/911_Call_Data.db') as conn:
        conn.row_factory = sqlite3.Row  # Ensure we can access columns by name
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Calls
            ORDER BY call_date_time DESC
            LIMIT 10
        ''')
        incidents = cursor.fetchall()  # Fetch the latest 10 incidents
    return incidents

# Update Incident (Modify Incident Details)
def update_incident(call_key, priority=None, description=None, call_date_time=None):
    """
    Update an incident in the database.

    This function updates an existing incident in the Calls table in the database. The incident is identified by its call_key.

    Parameters:
    - call_key (str): The unique identifier for the incident to update.
    - priority (str, optional): The new priority of the incident (Low, Medium, High, Non-Emergency).
    - description (str, optional): The new description of the incident.
    - call_date_time (str, optional): The new date and time of the call in the format "YYYY/MM/DD HH:MM:SS+00".

    Raises:
    - ValueError: If no fields (priority, description, or call_date_time) are provided to update.

    Returns:
        None
    """
    with sqlite3.connect('database/911_Call_Data.db') as conn:
        conn.row_factory = sqlite3.Row  # Ensure we can access columns by name
        cursor = conn.cursor()
        update_values = []
        query = "UPDATE Calls SET "
        update_parts = []

        if priority:
            update_parts.append("priority = ?")
            update_values.append(priority)
        if description:
            update_parts.append("description = ?")
            update_values.append(description)
        if call_date_time:
            update_parts.append("call_date_time = ?")
            update_values.append(call_date_time)

        if not update_parts:
            raise ValueError("At least one field (priority, description, or call_date_time) must be provided to update.")

        query += ", ".join(update_parts) + " WHERE call_key = ?"
        update_values.append(call_key)

        cursor.execute(query, tuple(update_values))
        conn.commit()  # Save changes to the database

# Delete Incident (Remove Incident)
def delete_incident(call_key):
    """
    Delete an incident from the Calls table in the database.

    Parameters:
    - call_key (str): The unique identifier of the incident to delete.

    Returns:
        None
    """

    with sqlite3.connect('database/911_Call_Data.db') as conn:
        conn.row_factory = sqlite3.Row  # Ensure we can access columns by name
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Calls WHERE call_key = ?', (call_key,))
        conn.commit()  # Save changes to the database


# Search Incident by call_key (Return a dictionary)
def search_incident(call_key=None):
    """
    Search for incidents in the database based on the given parameters.

    This function queries the `Calls` table in the database and returns 
    incidents that match the specified criteria. If no criteria are provided, 
    all incidents are returned.

    Parameters:
    - call_key (str, optional): The unique identifier for the incident to search for.

    Returns:
    - list of sqlite3.Row: A list of rows representing the incidents that match 
      the search criteria. Each row is a dictionary-like object with column names 
      as keys.
    """

    with sqlite3.connect('database/911_Call_Data.db') as conn:
        conn.row_factory = sqlite3.Row  # Ensure rows are returned as dictionary-like objects
        cursor = conn.cursor()

        query = "SELECT * FROM Calls WHERE 1=1"
        params = []

        if call_key:
            query += " AND call_key = ?"
            params.append(call_key)
        
        cursor.execute(query, tuple(params))
        incidents = cursor.fetchall()  # Get all matching records
    return incidents
