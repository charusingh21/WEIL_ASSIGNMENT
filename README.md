# Project Overview
This repository contains a Flask API developed to serve data from a SQLite database. The API is containerized using Docker for easier deployment and management.

**Prerequisites**
Before running the application, make sure you have the following installed on your system:

- Docker
- Git

# Installation 

1. **Clone this repository to your local machine**:
git clone https://github.com/charusingh21/Weil_ML_Challenge.git
2. **Navigate to the project directory**:
cd Weil_ML_Challenge

**TASK 1** 
1. Run the `run_app.sh` script by executing the following command:
- ./run_app.sh
2. Once the application is running,you can access it by visiting http://localhost:5000 in your web browse

**TASK 2**
Run the `build_image.sh` script by executing the following command:
- ./build_image.
Once the application is running,you can access it by visiting http://localhost:8080 in your web browse

**Usage**
Once the Docker container is running, you can access the API endpoints using cURL or your preferred HTTP client.
The API provides the following endpoints:
/chart_data: Retrieves chart data based on provided IDs.
/summary_data: Retrieves summary data from the database using a SQL query.
/summary_data_pandas: Retrieves summary data processed using pandas.
Example cURL commands:
**Retrieve chart data using ID number, following command will return data for ID's 1,2 and 3**
curl -X GET "http://localhost:8080/chart_data?ids=1,2,3" -H "accept: application/json"

 **Retrieve summary data**
curl -X GET "http://localhost:8080/summary_data" -H "accept: application/json"

**Retrieve summary data using pandas**
curl -X GET "http://localhost:8080/summary_data_pandas" -H "accept: application/json"

**Project Structure**
- app.py: Main Flask application code.
- Dockerfile: Instructions for building the Docker image.
- docker-compose.yml: Configuration for Docker Compose.
- requirements.txt: List of Python dependencies.
- randomized_chart_data.sqlite: SQLite database file.
- run_app.sh: Bash script to run the Flask application.
- query_api.sh: Bash script with sample cURL commands to query the API.


This code defines a Flask application that serves as an API for accessing data from a SQLite database and performing various operations on it. Let's break down the code and understand how it works:

1. **Imports**: The code imports necessary modules:
   - `Flask` for creating the web application.
   - `request` for accessing parameters sent with the HTTP request.
   - `jsonify` for converting Python objects to JSON responses.
   - `sqlite3` for interacting with the SQLite database.
   - `pandas` for data manipulation.

2. **Database Connection Function**: `connect_to_database()` establishes a connection to the SQLite database named 'randomized_chart_data.sqlite'.

3. **Data Fetching Functions**:
   - `get_chart_data(ids)`: Fetches chart data based on the provided IDs from the `Chart_Data` table in the SQLite database.
   - `get_summary_data()`: Fetches summary data using a SQL query from the `Chart_Data` table.
   - `process_data()`: Fetches and processes data using pandas DataFrame. It applies filtering conditions, groups the data, and computes summary statistics.

4. **API Endpoints**:
   - `/chart_data`: Accepts GET requests with comma-separated IDs as parameters and returns chart data for the provided IDs.
   - `/summary_data`: Accepts GET requests and returns summary data fetched using SQL queries.
   - `/summary_data_pandas`: Accepts GET requests and returns summary data processed using pandas DataFrame.

5. **Flask Routes**:
   - Each endpoint is defined with the `@app.route()` decorator specifying the route URL and the HTTP methods it accepts.
   - Inside each route function, the corresponding data fetching function is called, and the fetched data is returned as a JSON response using `jsonify()`.

6. **Main Block**: The application is run when the script is executed directly (not imported as a module). The `app.run()` function starts the Flask development server.

**Design Decisions**
I have not considered the subjects with null values in Unit_Of_Measure based on my intution that at every measurement should have a unit associated with it.
In the ERROR column there were only 0s and Nulls. That mean either we do not have information regarding the error (NULL) in the measurement or the values were error free (0).  Also,according to problem statement error and warning should not be 1. That means it can either be 0 or None.However, when error and warning were both 0's , the result_status is also null. Possible outcomes for result could be either null or Final. I chose to ignore if result is Null. So only possibility was to
consider null values in ERROR and WARNING columns so that we can have some meaningful result status that is FINAL.

