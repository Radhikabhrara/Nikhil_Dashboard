import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

# Function to connect to the MySQL database
def create_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host='new-db-1.advasmart.in',
            user='radhika-ro',
            password='sYkcHssQBbUwIuJ',
            port=3366,
            db='advasmartdb'
        )
    except Exception as e:
        st.error(f"Error: Unable to connect to the database. {e}")
    return connection

# Function to fetch data from the MySQL database
def fetch_data(start_date, end_date, connection):
    try:
        with connection.cursor() as cursor:
            query = f"""
                SELECT client_name, stat_date, comp_app_count, approv_app_count, yet_to_create_app_count, rejected_app_count
                FROM aggregate_daily_stats_as_on
                WHERE stat_date BETWEEN %s AND %s
            """
            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Error: Unable to fetch data from the database. {e}")
        return []

# Create a Streamlit app
st.title("MySQL Database Dashboard")

# Connect to the MySQL database
conn = create_connection()

if conn is not None:
    # Date Range Filter
    st.sidebar.write("### Date Range Filter")
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    # Default date range for initial data display
    if not start_date:
        start_date = pd.to_datetime("2023-10-07")
    if not end_date:
        end_date = pd.to_datetime("2023-12-31")

    # Example: Display a table from your database
    st.header('Sample Table from the Database')

    # Load data from the database based on the selected date range
    data = fetch_data(start_date, end_date, conn)

    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=["Client Name", "Date", "Completed Application", "Approved Applications", "Yet to Create Applications", "Rejected Applications"])

    # Display the data
    st.write("### Application Count Data")
    st.dataframe(df)

    # Interactive Bar Chart
    st.write("### Application level Bar Chart")
    fig = px.bar(df, x="Client Name", y=["Completed Application", "Approved Applications", "Yet to Create Applications", "Rejected Applications"], title="Application Count")
    st.plotly_chart(fig)

    st.write("### Client level Pie Chart")
    # Concatenate the values from multiple columns into a single 'Values' column
    df['Values'] = df[['Completed Application', 'Approved Applications', 'Yet to Create Applications', 'Rejected Applications']].sum(axis=1)

    # Create the pie chart using Plotly Express
    fig = px.pie(df, names="Client Name", values="Values", title="Application Count")

    # Display the chart using st.plotly_chart
    st.plotly_chart(fig)

    # Close the database connection
    conn.close()
else:
    st.error("Unable to connect to the database.")
