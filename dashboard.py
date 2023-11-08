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

# Function to fetch application data from the MySQL database
def fetch_application_data(start_date, end_date, client, connection):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT client_name, stat_date, comp_app_count, approv_app_count, yet_to_create_app_count, rejected_app_count
                FROM aggregate_daily_stats_as_on
                WHERE stat_date BETWEEN %s AND %s AND client_name = %s
            """
            cursor.execute(query, (start_date, end_date, client))
            data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Error: Unable to fetch application data from the database. {e}")
        return []

# Function to fetch order data from the MySQL database
def fetch_order_data(start_date, end_date, client, connection):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT client_name, stat_date, man_order_count, auto_order_count, remain_order_count, total_order_count
                FROM aggregate_daily_stats_as_on
                WHERE stat_date BETWEEN %s AND %s AND client_name = %s
            """
            cursor.execute(query, (start_date, end_date, client))
            data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Error: Unable to fetch order data from the database. {e}")
        return []

# Create a Streamlit app
st.title("MySQL Database Dashboard")

# Connect to the MySQL database
conn = create_connection()

if conn is not None:
    # Select data level (application, order, or both)
    data_level = st.radio("Select Data Level:", ["Application Level", "Order Level", "Both"])

    # Date Range Filter
    st.sidebar.write("### Date Range Filter")
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    # Client Selection
    client = st.sidebar.selectbox("Select Client:", ["Client A", "Client B", "Client C"])

    # Default date range for initial data display
    if not start_date:
        start_date = pd.to_datetime("2023-01-01")
    if not end_date:
        end_date = pd.to_datetime("2023-12-31")

    if data_level in ["Application Level", "Both"]:
        # Example: Display a table from your database - Application Level
        st.header('Application Level Data')
        application_data = fetch_application_data(start_date, end_date, client, conn)

        # Create a DataFrame for application data
        df_app = pd.DataFrame(application_data, columns=["Client Name", "Date", "Completed Application", "Approved Applications", "Yet to Create Applications", "Rejected Applications"])

        # Display the application data
        st.write("### Application Count Data")
        st.dataframe(df_app)

        # Interactive Bar Chart for Application Level
        st.write("### Application level Bar Chart")
        fig_app = px.bar(df_app, x="Client Name", y=["Completed Application", "Approved Applications", "Yet to Create Applications", "Rejected Applications"], title="Application Count")
        st.plotly_chart(fig_app)

    if data_level in ["Order Level", "Both"]:
        # Example: Display a table from your database - Order Level
        st.header('Order Level Data')
        order_data = fetch_order_data(start_date, end_date, client, conn)

        # Create a DataFrame for order data
        df_order = pd.DataFrame(order_data, columns=["Client Name", "Date", "Manual Orders", "Auto Orders", "Remaining Orders", "Total Orders"])

        # Display the order data
        st.write("### Order Count Data")
        st.dataframe(df_order)

        # Interactive Bar Chart for Order Level
        st.write("### Order level Bar Chart")
        fig_order = px.bar(df_order, x="Client Name", y=["Manual Orders", "Auto Orders", "Remaining Orders", "Total Orders"], title="Order Count")
        st.plotly_chart(fig_order)

    # Close the database connection
    conn.close()
else:
    st.error("Unable to connect to the database.")
