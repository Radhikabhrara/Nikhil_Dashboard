import streamlit as st
import pymysql


# Function to create a database connection
def create_connection():
    db_config = {
        'host': 'new-db-1.advasmart.in',
        'user': 'radhika-ro',
        'password': 'sYkcHssQBbUwIuJ',
        'database': 'advasmartdb',
        'port': 3366,  # Replace with your MySQL server's port number
    }
    conn = pymysql.connect(**db_config)
    return conn


# Function to execute SQL queries
def run_query(query):
    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    conn.close()
    return result

# Streamlit App
st.title('MySQL Database Dashboard')

# Connect to the database
conn = create_connection()



# Function to retrieve data from the database
def fetch_data():
    # Replace this with your database connection and query
    conn = sqlite3.connect("advasmartdb")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM order_counts")
    data = cursor.fetchall()
    conn.close()
    return data

# Example: Display a table from your database
st.header('Sample Table from the Database')

import streamlit as st
import pandas as pd
import sqlite3  # Replace with your database library

# Function to retrieve data from the database
def fetch_data(start_date, end_date):
    # Replace this with your database connection and query
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    query = f"SELECT client_name ,stat_date,comp_app_count,approv_app_count ,yet_to_create_app_count,rejected_app_count FROM aggregate_daily_stats_as_on WHERE stat_date BETWEEN '{start_date}' AND '{end_date}'"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# Create a Streamlit app
st.title("Dashboard")

# Date Range Filter
st.sidebar.write("### Date Range Filter")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Default date range for initial data display
if not start_date:
    start_date = pd.to_datetime("2023-10-07")
if not end_date:
    end_date = pd.to_datetime("2023-12-31")

# Load data from the database based on the selected date range
data = fetch_data(start_date, end_date)

# Create a DataFrame from the data
df = pd.DataFrame(data, columns=["Client Name", "Date", "Completed Application" ,"Appproved Applications" ,"Yet to create Appplications", "Rejcted Applications"])

# Display the data
st.write("### Application Count Data")
st.dataframe(df)

# Create a bar chart to visualize the data
st.write("### Application Count Bar Chart")
st.bar_chart(df)

# Create a pie chart to visualize the data distribution
st.write("### Application Count Pie Chart")
st.plotly_chart(df.plot.pie(subplots=True, autopct="%1.1f%%", legend=False, labels=df.index))

# Run the app with 'streamlit run
# Close the database connection
conn.close()
