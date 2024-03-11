from flask import Flask, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

# Function to establish database connection
def connect_to_database():
    return sqlite3.connect('randomized_chart_data.sqlite')

# Function to fetch chart data based on provided IDs
def get_chart_data(ids):
    conn = connect_to_database()
    cursor = conn.cursor()
    ids_str = ','.join(map(str, ids))
    query = f"""
    SELECT Chart_Data.Id, 
           Chart_Data.CHARTTIME, 
           Chart_Data.VALUENUM, 
           Chart_Data.WARNING, 
           Chart_Data.ERROR, 
           Chart_Data.STOPPED, 
           Observation_Type.Name AS Observation_Type_Name, 
           Result_Status.Name AS Result_Status_Name, 
           Unit_Of_Measure.Name AS Unit_Of_Measure_Name
    FROM Chart_Data
    LEFT JOIN Observation_Type ON Chart_Data.Observation_Type_Id = Observation_Type.Id
    LEFT JOIN Result_Status ON Chart_Data.Result_Status_Id = Result_Status.Id
    LEFT JOIN Unit_Of_Measure ON Chart_Data.Unit_Of_Measure_Id = Unit_Of_Measure.Id
    WHERE Chart_Data.Id IN ({ids_str});
    """
    cursor.execute(query)
    #data = cursor.fetchall()
    rows = cursor.fetchall()
    conn.close()
    column_names = [description[0] for description in cursor.description]
    data = []
    for row in rows:
        data.append(dict(zip(column_names, row)))
    return data

# Function to fetch summary data
def get_summary_data():
    try:
        conn = connect_to_database()
        query = """
        SELECT ROW_NUMBER() OVER (ORDER BY Observation_Type.Name, Unit_Of_Measure.Name) AS row_number,
               Observation_Type.Name AS Observation_Type, 
               Unit_Of_Measure.Name AS Unit_Of_Measure,
               COUNT(*) AS Num_Records,
               COUNT(DISTINCT Chart_Data.SUBJECT_ID) AS Num_Admissions,
               MIN(Chart_Data.VALUENUM) AS Min_Value, 
               MAX(Chart_Data.VALUENUM) AS Max_Value,
               Chart_Data.ERROR,
               Chart_Data.WARNING
            
        FROM Chart_Data
        JOIN Observation_Type ON Chart_Data.Observation_Type_Id = Observation_Type.Id
        JOIN Unit_Of_Measure ON Chart_Data.Unit_Of_Measure_Id = Unit_Of_Measure.Id
        WHERE (Chart_Data.ERROR != 1 OR Chart_Data.ERROR IS NULL)
        AND (Chart_Data.WARNING != 1 OR Chart_Data.WARNING IS NULL)
        AND Chart_Data.Result_Status_Id != (SELECT Id FROM Result_Status WHERE Name = 'Manual')
        GROUP BY Observation_Type.Name, Unit_Of_Measure.Name;
        """
        cursor = conn.cursor()
        cursor.execute(query)
        #data = cursor.fetchall()
        rows = cursor.fetchall()
        conn.close()

        column_names = [description[0] for description in cursor.description]
        data = []
        for row in rows:
            data.append(dict(zip(column_names, row)))
        return data
    except Exception as e:
        print("Error:", e)
        return None

# Function to fetch data and compute summary statistics
def process_data():
    try:
        conn = connect_to_database()
        query = """
        SELECT Observation_Type.Name AS Observation_Type, 
               Unit_Of_Measure.Name AS Unit_Of_Measure,
               Chart_Data.SUBJECT_ID, 
               Chart_Data.VALUENUM, 
               Chart_Data.ERROR, 
               Chart_Data.WARNING,
               Result_Status.Name AS Result_Status_Name
        FROM Chart_Data
        JOIN Observation_Type ON Chart_Data.Observation_Type_Id = Observation_Type.Id
        JOIN Unit_Of_Measure ON Chart_Data.Unit_Of_Measure_Id = Unit_Of_Measure.Id
        JOIN Result_Status ON Chart_Data.Result_Status_Id = Result_Status.Id
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Apply filtering conditions directly on DataFrame
        df = df[((df['ERROR'] != 1) | df['ERROR'].isnull()) & \
                ((df['WARNING'] != 1) | df['WARNING'].isnull()) & \
                (df['Result_Status_Name'] != 'Manual')]
        
        # Group by Observation_Type and Unit_Of_Measure
        grouped_df = df.groupby(['Observation_Type', 'Unit_Of_Measure']).agg(
            Num_Records=('VALUENUM', 'count'),
            Num_Admissions=('SUBJECT_ID', pd.Series.nunique),
            Min_Value=('VALUENUM', 'min'),
            Max_Value=('VALUENUM', 'max')
        ).reset_index()
        
        return grouped_df
    except Exception as e:
        print("Error:", e)
        return None

# Endpoint to handle requests for chart data
@app.route('/chart_data', methods=['GET'])
def chart_data():
    ids = request.args.get('ids')
    if not ids:
        return jsonify({'error': 'Please provide a comma-separated list of IDs'}), 400
    
    ids = [int(id.strip()) for id in ids.split(',')]
    if not ids:
        return jsonify({'error': 'Invalid IDs provided'}), 400
    
    chart_data = get_chart_data(ids)
    if not chart_data:
        return jsonify({'error': 'No data found for provided IDs'}), 404
    
    return jsonify(chart_data), 200



# Endpoint to handle requests for summary data
@app.route('/summary_data', methods=['GET'])
def summary_data():
    summary_data = get_summary_data()
    if summary_data is None:
        return jsonify({'error': 'Error fetching summary data'}), 500
        # Extract column names from the first row of data

    
    
    return jsonify(summary_data), 200

# Endpoint to handle requests for summary data using pandas
@app.route('/summary_data_pandas', methods=['GET'])
def summary_data_pandas():
    summary_data = process_data()
    if summary_data is None:
        return jsonify({'error': 'Error processing summary data'}), 500
    
    # Convert DataFrame to dictionary with index as key
    summary_json = summary_data.to_dict(orient='index')
    
    return jsonify(summary_json), 200

if __name__ == '__main__':
    app.run(debug=True)
