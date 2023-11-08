import streamlit as st
import pymysql

# Function to create a database connection
def create_connection():
    db_config = {
        'host': 'new-db-1.advasmart.in',
        'user'='radhika-ro',
        'password'='sYkcHssQBbUwIuJ',
        'port' = 3366,
        'db'='advasmartdb' # Replace with your MySQL server's port number
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

# Fetch column names from the database
def get_column_names(table_name):
    with conn.cursor() as cursor:
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [row[0] for row in cursor.fetchall()]
    return columns

# Example: Display a table from your database
st.header('Sample Table from the Database')
table_name = 'aggregate_daily_stats'  # Replace with the table name you want to display
columns = get_column_names(table_name)

# Display the table data with column names as headers
if columns:
    query = f"SELECT * FROM {table_name}"
    table_data = run_query(query)
    if table_data:
        # Convert tuples in table_data to lists
        table_data = [list(row) for row in table_data]
        # Insert the column names as the first row of the data
        table_data = [columns] + table_data
        st.table(table_data)  # Display data with column names as headers
    else:
        st.warning('No data available for the selected table.')
else:
    st.warning('No columns available for the selected table.')

# Close the database connection
conn.close()
