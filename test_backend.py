import sqlite3
import uuid
from backend import create_incident, update_incident, delete_incident, search_incident

# Function to check the number of rows in the Calls table (for testing)
def get_calls_count():
    conn = sqlite3.connect('database/911_Call_Data.db')  # Adjust path if needed
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Calls")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# 1. Test `create_incident()`
def test_create_incident():
    # Generate a unique call_key for each test
    call_key = str(uuid.uuid4())  # Generate a unique UUID as the call_key
    
    # Create a new incident with a unique call_key
    create_incident(call_key, "R001", "2021/12/01 10:00:00+00", "High", "HIT AND RUN", "P210123456", 2, 1, 1)
    
    # Verify if the incident was created by checking the row count
    count_before = get_calls_count()
    call_key_2 = str(uuid.uuid4())  # Generate another unique call_key
    create_incident(call_key_2, "R002", "2021/12/01 11:00:00+00", "Medium", "THEFT", "P210123457", 3, 2, 2)
    count_after = get_calls_count()

    assert count_after == count_before + 1, f"Test failed! Expected {count_before + 1} rows, but got {count_after}."

# 2. Test `update_incident()`
def test_update_incident():
    # Create a new incident to update
    call_key = str(uuid.uuid4())  # Generate a unique call_key
    create_incident(call_key, "R003", "2021/12/01 12:00:00+00", "Low", "BURGLARY", "P210123458", 4, 3, 3)
    
    # Update the incident's priority and description
    update_incident(call_key, priority="High", description="HOME BURGLARY")

    # Fetch the updated incident
    conn = sqlite3.connect('database/911_Call_Data.db')  # Adjust path if needed
    conn.row_factory = sqlite3.Row  # Ensure that the results are returned as Row objects
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Calls WHERE call_key = ?", (call_key,))
    updated_incident = cursor.fetchone()
    conn.close()

    # Check if the values were updated correctly
    assert updated_incident['priority'] == "High", f"Test failed! Expected 'High', but got {updated_incident['priority']}."
    assert updated_incident['description'] == "HOME BURGLARY", f"Test failed! Expected 'HOME BURGLARY', but got {updated_incident['description']}."

# 3. Test `delete_incident()`
def test_delete_incident():
    # Create a new incident to delete
    call_key = str(uuid.uuid4())  # Generate a unique call_key
    create_incident(call_key, "R004", "2021/12/01 13:00:00+00", "Medium", "VANDALISM", "P210123459", 5, 4, 4)

    # Verify if the incident was created
    count_before = get_calls_count()

    # Delete the incident
    delete_incident(call_key)

    # Verify if the incident was deleted by checking the row count
    count_after = get_calls_count()

    assert count_after == count_before - 1, f"Test failed! Expected {count_before - 1} rows, but got {count_after}."

def delete_all_incidents():
    conn = sqlite3.connect('database/911_Call_Data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Calls')  # Clean the Calls table
    conn.commit()
    conn.close()

def test_search_incident():
    # Clean up the database to ensure only test data exists
    delete_all_incidents()

    # Create test incidents
    call_key_1 = str(uuid.uuid4())  # Generate unique call_key
    call_key_2 = str(uuid.uuid4())  # Generate another unique call_key
    create_incident(call_key_1, "R005", "2021/12/01 14:00:00+00", "Low", "ASSAULT", "P210123460", 6, 5, 5)
    create_incident(call_key_2, "R006", "2021/12/01 15:00:00+00", "High", "ROBBERY", "P210123461", 7, 6, 6)
    
    # Test search by priority (Low)
    low_priority_incidents = search_incident(priority="Low")
    assert len(low_priority_incidents) == 1, f"Test failed! Expected 1 incident with Low priority, but got {len(low_priority_incidents)}."

    # Test search by description (ASSAULT)
    assault_incidents = search_incident(description="ASSAULT")
    assert len(assault_incidents) == 1, f"Test failed! Expected 1 incident with 'ASSAULT', but got {len(assault_incidents)}."
    
    # Test search with no results (non-existing priority or description)
    non_existing_incidents = search_incident(description="MISSING")
    assert len(non_existing_incidents) == 0, f"Test failed! Expected 0 incidents with 'MISSING', but got {len(non_existing_incidents)}."

# Running the tests
def run_tests():
    test_create_incident()
    print("create_incident() test passed.")
    
    test_update_incident()
    print("update_incident() test passed.")
    
    test_delete_incident()
    print("delete_incident() test passed.")
    
    test_search_incident()
    print("search_incident() test passed.")

# Execute the tests
run_tests()
