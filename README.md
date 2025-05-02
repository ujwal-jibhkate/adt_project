# **911 Incident Management System**

This is a **911 Incident Management System** built using **Streamlit**, **SQLite**, and **Altair**. It allows users to manage, update, delete, and search 911 incidents in a visually interactive way. The project provides a **dashboard**, an **incident viewing interface**, and other functionalities like adding, updating, and searching for incidents, all backed by a robust database.

The **main features** of the system include:

* **Dashboard**: Displays interactive visualizations of the incidents.
* **Incident Management**: Add new incidents, update existing ones, or delete incidents.
* **Search Incidents**: Search for incidents by call key.
* **Data Visualization**: The dashboard provides insights like priority distribution, call volume by hour, and incident distribution by district.

---

## **Table of Contents**

* [Features](#features)
* [Tech Stack](#tech-stack)
* [Installation](#installation)
* [Usage](#usage)
* [How it Works](#how-it-works)


---

## **Features**

1. **Dashboard**:

   * Displays visual insights with **interactive charts** powered by **Altair**.
   * Includes charts like **Priority Distribution**, **Calls by Hour of Day**, **Calls by District**, **Calls by Neighborhood**, and more.

2. **Incident Management**:

   * **Add Incidents**: Users can add new incidents, with the **call key** auto-generated.
   * **Update Incidents**: Modify details like **priority**, **description**, and **call time** for any incident.
   * **Delete Incidents**: Remove any incident from the system.

3. **Search Incidents**:

   * Search for an incident by **call key**.
   * Results are displayed in a user-friendly format with incident details and an option to delete.

4. **User Interface**:

   * Clean and modern UI using **Streamlit**.
   * **Tabs** for navigating different sections like Dashboard, Add Incident, Update Incident, etc.
   * **Interactive charts** for dynamic data visualization.

---

## **Tech Stack**

* **Frontend**:

  * **Streamlit**: For building the web app's interactive UI.

* **Backend**:

  * **SQLite3**: For storing incident data in a lightweight, serverless database.
  * **Python**: For writing the backend logic and processing data.

* **Data Visualization**:

  * **Altair**: For creating interactive visualizations of the incident data.

* **Hosting**:

  * **Streamlit Cloud**: For deploying the app.

---

## **Installation**

### **Step 1**: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/911-incident-management-system.git
cd 911-incident-management-system
```

### **Step 2**: Set Up a Virtual Environment

It’s a good practice to use a virtual environment to avoid dependency conflicts:

```bash
python -m venv env
```

Activate the virtual environment:

* On Windows:

  ```bash
  .\env\Scripts\activate
  ```

* On macOS/Linux:

  ```bash
  source env/bin/activate
  ```

### **Step 3**: Install Dependencies

Install the required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

* The **`requirements.txt`** file includes the following packages:

  * `streamlit`
  * `pandas`
  * `altair`
  * `sqlite3`

### **Step 4**: Run the App Locally

To run the app locally, use:

```bash
streamlit run app.py
```

This will launch the application, and you can access it by opening your browser and going to `http://localhost:8501`.

---

## **Usage**

Once the app is running, you can interact with it via the **Streamlit interface**.

### **Tabs and Features**:

1. **Dashboard**: View interactive charts, including:

   * **Priority Distribution**
   * **Calls by Hour of Day**
   * **Number of Calls by District**
   * **Number of Calls by Neighborhood**
   * **Total Calls by Priority Over Time**

2. **View Latest 10 Incidents**: Display the latest incidents added to the database.

3. **Add Incident**:

   * Fill in the **incident details** (Record ID, Call Date, Priority, Description, etc.).
   * The **call key** is automatically generated and shown in the success message after submission.

4. **Update Incident**:

   * Search for incidents by **call key**.
   * Modify the **priority**, **description**, or **call time**.

5. **Search Incidents**:

   * Search for incidents using the **call key**.
   * Results are displayed in a clean and readable format.
   * You can also **delete incidents** directly from the search results.


---

## **How it Works**

1. **Backend Logic**:

   * The backend is powered by **SQLite3** to store incident data.
   * **Incident Management** functions include `create_incident()`, `update_incident()`, `delete_incident()`, and `search_incident()`.
   * The **database** contains tables for `Calls`, `Jurisdictions`, and `Locations`.

2. **Data Flow**:

   * Data is fetched using SQL queries (such as `SELECT` to read and `INSERT` to add new records).
   * The application allows users to add new incidents, update existing incidents, delete incidents, and search incidents by **call key**.

3. **Visualizations**:

   * The system provides **interactive charts** using **Altair** to represent the incident data, making it easier to analyze trends, such as call priorities, volume by hour, and geographical data (district and neighborhood).
   * **Altair's interactivity** allows users to hover, zoom, and explore the charts in detail.

4. **Deployment**:

   * The app is deployed on **Streamlit Cloud**, making it publicly available.
   * All the features (adding, updating, deleting incidents, and visualizations) are fully functional on the cloud version.


### **Conclusion**

This **911 Incident Management System** provides an interactive and user-friendly way to manage 911 incidents and visualize trends in the data. With its simple **Streamlit UI** and interactive **Altair charts**, the app makes it easy for users to manage and explore incident data. Deploying this system on **Streamlit Cloud** allows it to be easily shared and accessed by others.
