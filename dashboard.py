

# Import necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# Function to fetch data from the MySQL database
def fetch_data(start_date, end_date, connection, data_level):
    try:
        with connection.cursor() as cursor:
            query = f"""
                SELECT client_name, stat_date, {data_level}
                FROM aggregate_daily_stats_as_on
                WHERE stat_date BETWEEN %s AND %s
            """
            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Error: Unable to fetch data from the database. {e}")
        return []

# Function to generate weekly, monthly, and quarterly reports
def generate_reports(data, data_level, time_period):
    df = pd.DataFrame(data, columns=["Client Name", "Date", data_level])

    if time_period == "Weekly":
        df['Week Start'] = df['Date'] - pd.to_timedelta(df['Date'].dt.dayofweek, unit='d')
        df['Week End'] = df['Week Start'] + pd.DateOffset(days=6)

        # Group by client and week, summing the values
        grouped_df = df.groupby(['Client Name', 'Week Start', 'Week End']).sum().reset_index()

    elif time_period == "Monthly":
        df['Month'] = df['Date'].dt.to_period('M')

        # Group by client and month, summing the values
        grouped_df = df.groupby(['Client Name', 'Month']).sum().reset_index()

    elif time_period == "Quarterly":
        df['Quarter'] = df['Date'].dt.to_period('Q')

        # Group by client and quarter, summing the values
        grouped_df = df.groupby(['Client Name', 'Quarter']).sum().reset_index()

    return grouped_df

# Create a Streamlit app
st.title("MySQL Database Dashboard")

# ... (your existing code)

# Add another page for reports
if st.sidebar.button("Generate Reports"):
    st.title("Generate Reports")

    # Select data level and time period for the report
    data_level_report = st.selectbox("Select Data Level", ["Application", "Order"])
    time_period_report = st.selectbox("Select Time Period", ["Weekly", "Monthly", "Quarterly"])

    # Fetch data based on selected parameters
    report_data = fetch_data(start_date, end_date, conn, data_level_report)

    # Generate the report
    if report_data:
        report_df = generate_reports(report_data, data_level_report.lower(), time_period_report)

        # Display the generated report
        st.write("### Generated Report")
        st.dataframe(report_df)

        # Interactive Bar Chart for the generated report
        st.write(f"### {time_period_report} Bar Chart")
        fig_report = px.bar(report_df, x="Client Name", y=data_level_report, color=time_period_report, title=f"{data_level_report} Count")
        st.plotly_chart(fig_report)

# ... (continue with the rest of your code)

# Import necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# Function to fetch data from the MySQL database
def fetch_data(start_date, end_date, connection, data_level):
    try:
        with connection.cursor() as cursor:
            query = f"""
                SELECT client_name, stat_date, 
                {"comp_app_count, approv_app_count, yet_to_create_app_count, rejected_app_count" if data_level == "Application" else "man_order_count, auto_order_count, remain_order_count, total_order_count"}
                FROM aggregate_daily_stats_as_on
                WHERE stat_date BETWEEN %s AND %s
            """
            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Error: Unable to fetch data from the database. {e}")
        return []

# Function to generate reports
def generate_reports(data, data_level, time_period):
    df = pd.DataFrame(data, columns=["Client Name", "Date", data_level])

    if time_period == "Weekly":
        df['Week Start'] = df['Date'] - pd.to_timedelta(df['Date'].dt.dayofweek, unit='d')
        df['Week End'] = df['Week Start'] + pd.DateOffset(days=6)

        # Group by client and week, summing the values
        grouped_df = df.groupby(['Client Name', 'Week Start', 'Week End']).sum().reset_index()

    elif time_period == "Monthly":
        df['Month'] = df['Date'].dt.to_period('M')

        # Group by client and month, summing the values
        grouped_df = df.groupby(['Client Name', 'Month']).sum().reset_index()

    elif time_period == "Quarterly":
        df['Quarter'] = df['Date'].dt.to_period('Q')

        # Group by client and quarter, summing the values
        grouped_df = df.groupby(['Client Name', 'Quarter']).sum().reset_index()

    return grouped_df

# Create a Streamlit app
st.title("MySQL Database Dashboard")

# Connect to the MySQL database
conn = create_connection()

if conn is not None:
    st.sidebar.title("AdvaInsights")

    # Dropdown to select data level (application, order, or both)
    data_level = st.sidebar.selectbox("Select Data Level", ["", "Application", "Order", "Both"])

    st.sidebar.write("### Date Range Filter")
    
    # Date Range Filter
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    # Default date range for initial data display
    if not start_date:
        start_date = pd.to_datetime("2023-01-01")
    if not end_date:
        end_date = pd.to_datetime("2023-12-31")

    st.sidebar.write("### Client Wise Filter")
    # Checkbox to filter data
    filter_data = st.sidebar.checkbox("Filter Data")

    # Add another page for generating reports
    if st.sidebar.button("Generate Reports"):
        st.title("Generate Reports")

        # Select data level and time period for the report
        data_level_report = st.selectbox("Select Data Level", ["Application", "Order"])
        time_period_report = st.selectbox("Select Time Period", ["Weekly", "Monthly", "Quarterly"])

        # Fetch data based on selected parameters
        report_data = fetch_data(start_date, end_date, conn, data_level_report)

        # Generate the report
        if report_data:
            report_df = generate_reports(report_data, data_level_report.lower(), time_period_report)

            # Display the generated report
            st.write("### Generated Report")
            st.dataframe(report_df)

            # Interactive Bar Chart for the generated report
            st.write(f"### {time_period_report} Bar Chart")
            fig_report = px.bar(report_df, x="Client Name", y=data_level_report.lower(), color=time_period_report, title=f"{data_level_report} Count")
            st.plotly_chart(fig_report)

    if data_level == "Application" or data_level == "Both":
        # Example: Display a table from your database - Application Level
        st.header('Application Level Data')
        application_data = fetch_application_data(start_date, end_date, conn)

        # Create a DataFrame for application data
        df_app = pd.DataFrame(application_data, columns=["Client Name", "Date", "Completed Application", "Approved Applications", "Yet to Create Applications", "Rejected Applications"])

        if filter_data:
            # Filter data based on the checkbox
            selected_client = st.sidebar.selectbox("Select Client", df_app['Client Name'].unique())
            df_app = df_app[df_app['Client Name'] == selected_client]

        # Display the application data
        st.write("### Application Count Data")
        st.dataframe(df_app)

        # Interactive Bar Chart for Application Level
        st.write("### Application level Bar Chart")
        fig_app = px.bar(df_app, x="Client Name", y=["Completed Application", "Approved Applications", "Yet to Create Applications", "Rejected Applications"], title="Application Count")
        st.plotly_chart(fig_app)

        # Create a pie chart using Plotly Express for Application Level
        st.write("### Application level Pie Chart")
        df_app['Values'] = df_app[['Completed Application', 'Approved Applications', 'Yet to Create Applications', 'Rejected Applications']].sum(axis=1)
        fig_app_pie = px.pie(df_app, names="Client Name", values="Values", title="Application Count")
        st.plotly_chart(fig_app_pie)

    if data_level == "Order" or data_level == "Both":
        # Example: Display a table from your database - Order Level
        st.header('Order Level Data')
        order_data = fetch_order_data(start_date, end_date, conn)

        # Create a DataFrame for order data
        df_order = pd.DataFrame(order_data, columns=["Client Name", "Date", "Manual Orders", "Auto Orders", "Remaining Orders", "Total Orders"])

        if filter_data:
            # Filter data based on the checkbox
            selected_client = st.sidebar.selectbox("Select Client", df_order['Client Name'].unique())
            df_order = df_order[df_order['Client Name'] == selected_client]

        # Display the order data
        st.write("### Order Count Data")
        st.dataframe(df_order)

        # Interactive Bar Chart for Order Level
        st.write("### Order level Bar Chart")
        fig_order = px.bar(df_order, x="Client Name", y=["Manual Orders", "Auto Orders", "Remaining Orders", "Total Orders"], title="Order Count")
        st.plotly_chart(fig_order)

        # Create a pie chart using Plotly Express for Order Level
        st.write("### Order level Pie Chart")
        df_order['Values'] = df_order[['Manual Orders', 'Auto Orders', 'Remaining Orders', 'Total Orders']].sum(axis=1)
        fig_order_pie = px.pie(df_order, names="Client Name", values



