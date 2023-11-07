import streamlit as st
import pymysql

# Establish a connection to your MySQL database
def create_connection():
    conn = pymysql.connect(
        host='new-db-1.advasmart.in',
        user='radhika-ro',
        password='sYkcHssQBbUwIuJ',
        port = 3366,
        db='advasmartdb'
    )
    return conn

# Streamlit App
st.title('MySQL Database Dashboard')

# Connect to the database
conn = create_connection()

# Define a function to execute SQL queries
def run_query(query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

st.header('Sample Table from the Database')

query = "SELECT * FROM aggregate_daily_stats"
table_data = run_query(query)

# Display the table data with column names as headers
if table_data:
    st.table([column[0] for column in cursor.description])  # Display column names
    st.table(table_data)  # Display data
else:
    st.warning('No data available for the selected table.')

# Close the database connection
conn.close()

