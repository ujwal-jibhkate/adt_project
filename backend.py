import sqlite3
import uuid

# Function to generate a unique call_key
def generate_unique_call_key():
    return str(uuid.uuid4())  # Generate a unique UUID and convert it to a string

# Create Incident (Insert New Incident)
def create_incident(call_key=None, record_id=None, call_date_time=None, priority=None, description=None, 
                    call_number=None, incident_location_id=None, reporter_location_id=None, jurisdiction_id=None):
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
    with sqlite3.connect('database/911_Call_Data.db') as conn:
        conn.row_factory = sqlite3.Row  # Ensure we can access columns by name
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Calls WHERE call_key = ?', (call_key,))
        conn.commit()  # Save changes to the database


# Search Incident by call_key (Return a dictionary)
def search_incident(call_key=None):
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
