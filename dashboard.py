# Import necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import timedelta
from dateutil.relativedelta import relativedelta

def fetch_data(start_date, end_date, connection, data_level):
    try:
        with connection.cursor() as cursor:
            query = f"""
                SELECT client_name, stat_date, 
                {"comp_app_count, approv_app_count, yet_to_create_app_count, rejected_app_count" if data_level == "Application" else "man_order_count, auto_order_count, remain_order_count, total_order_count"}
                FROM aggregate_daily_stats_as_on
                WHERE stat_date BETWEEN %s AND %s
            """
            print("Generated Query:", query)  # Add this line for debugging
            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Error: Unable to fetch data from the database. {e}")
        return []



# Function to generate reports
def generate_reports(data, data_levels, time_period):
    dfs = []

    for data_level in data_levels:
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

        dfs.append(grouped_df)

    return dfs

# Create a Streamlit app
st.title("MySQL Database Dashboard")

# Connect to the MySQL database
conn = create_connection()

if conn is not None:
    st.sidebar.title("AdvaInsights")

    st.sidebar.write("### Data Level and Report Generation")

    # Dropdown to select data level (application, order, or both)
    data_level = st.sidebar.selectbox("Select Data Level", ["Application", "Order", "Both"])

    # Date Range Filter
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))

    # Checkbox to filter data
    filter_data = st.sidebar.checkbox("Filter Data")

    # Multiselect to choose data levels for report generation
    data_levels_for_report = st.sidebar.multiselect("Select Data Levels for Report", ["Application", "Order"])

    if st.sidebar.button("Generate Reports"):
        st.title("Generate Reports")

        # Select time period for the report
        time_period_report = st.selectbox("Select Time Period", ["Weekly", "Monthly", "Quarterly"])

        # Fetch data based on selected parameters
        report_data = fetch_data(start_date, end_date, conn, data_level)

        # Generate the report
        if report_data:
            generated_reports = generate_reports(report_data, data_levels_for_report, time_period_report)

            for i, data_level_report in enumerate(data_levels_for_report):
                # Display the generated report
                st.write(f"### Generated {data_level_report} Report ({time_period_report} Trend)")
                st.dataframe(generated_reports[i])

                # Interactive Bar Chart for the generated report
                st.write(f"### {data_level_report} {time_period_report} Bar Chart")
                fig_report = px.bar(generated_reports[i], x="Client Name", y=data_level_report.lower(), color=time_period_report, title=f"{data_level_report} Count")
                st.plotly_chart(fig_report)

    # Display data based on selected data level
    if data_level in ["Application", "Both"]:
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

    if data_level in ["Order", "Both"]:
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
        fig_order_pie = px.pie(df_order, names="Client Name",
