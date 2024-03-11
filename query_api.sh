#!/bin/bash

# Sample curl command to query the API for chart data
curl -X GET "http://localhost:5000/chart_data?ids=1,2,3" -H "Content-Type: application/json"

# Sample curl command to query the API for summary data
curl -X GET "http://localhost:5000/summary_data" -H "Content-Type: application/json"

# Sample curl command to query the API for summary data using pandas
curl -X GET "http://localhost:5000/summary_data_pandas" -H "Content-Type: application/json"
