import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="AdvaInsight",initial_sidebar_state="auto")
# Add a logo and title using HTML



hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

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
def fetch_application_data(start_date, end_date, connection):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT client_name, stat_date, comp_app_count, approv_app_count, yet_to_create_app_count, rejected_app_count
                FROM aggregate_daily_stats_as_on
                WHERE stat_date BETWEEN %s AND %s
            """
            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Error: Unable to fetch application data from the database. {e}")
        return []

# Function to fetch order data from the MySQL database
def fetch_order_data(start_date, end_date, connection):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT client_name, stat_date, man_order_count, auto_order_count, remain_order_count, total_order_count
                FROM aggregate_daily_stats_as_on
                WHERE stat_date BETWEEN %s AND %s
            """
            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Error: Unable to fetch order data from the database. {e}")
        return []

def fetch_comparison_data(start_date, end_date, data_level, time_frame, connection):
    try:
        with connection.cursor() as cursor:
            # Customize the query based on the selected time frame and data level
            if time_frame == "Weekly":
                group_by_clause = "WEEK(stat_date)"
            elif time_frame == "Monthly":
                group_by_clause = "MONTH(stat_date)"
            elif time_frame == "Quarterly":
                group_by_clause = "QUARTER(stat_date)"

            if data_level == "Application":
                query = f"""
                    SELECT stat_date, 
                          SUM(comp_app_count) as total_comp_app_count, 
                          SUM(approved_app_count) as total_approved_app_count,
                          SUM(yet_to_create_app_count) as total_yet_to_create_app_count,
                          SUM(rejected_app_count) as total_rejected_app_count
                    FROM aggregate_daily_stats_as_on
                    WHERE stat_date BETWEEN %s AND %s
                    GROUP BY stat_date, {group_by_clause};
                """
            elif data_level == "Order":
                query = f"""
                    SELECT stat_date, 
                          SUM(man_order_count) as total_man_order_count, 
                          SUM(auto_order_count) as total_auto_order_count,
                          SUM(remain_order_count) as total_remain_order_count,
                          SUM(total_order_count) as total_total_order_count
                    FROM aggregate_daily_stats_as_on
                    WHERE stat_date BETWEEN %s AND %s
                    GROUP BY stat_date, {group_by_clause};
                """
            else:  # Both data levels
                query = f"""
                    SELECT stat_date, 
                          SUM(comp_app_count) as total_comp_app_count, 
                          SUM(approved_app_count) as total_approved_app_count,
                          SUM(yet_to_create_app_count) as total_yet_to_create_app_count,
                          SUM(rejected_app_count) as total_rejected_app_count,
                          SUM(man_order_count) as total_man_order_count, 
                          SUM(auto_order_count) as total_auto_order_count,
                          SUM(remain_order_count) as total_remain_order_count,
                          SUM(total_order_count) as total_total_order_count
                    FROM aggregate_daily_stats_as_on
                    WHERE stat_date BETWEEN %s AND %s
                    GROUP BY stat_date, {group_by_clause};
                """
            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()
        return data
    except Exception as e:
        st.error(f"Error: Unable to fetch comparison data from the database. {e}")
        return []


# Create a Streamlit app
st.title("AdvaInsights")

# Connect to the MySQL database
conn = create_connection()

if conn is not None:
    # Navigation menu with a default selection of "AdvaInsights"
    st.sidebar.title("AdvaInsights Menu")
    page = st.sidebar.radio("Navigation", ["AdvaInsights", "Customized Insights", "Generate Reports"], index=0)

    if page == "AdvaInsights":
        st.write("Under construction")

    elif page == "Customized Insights":
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

        if data_level == "Application" or data_level == "Both":
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
                selected_client = st.sidebar.selectbox("Select Client", df_order['Client Name'].unique(), key=f"client_selectbox_{page}")

                #selected_client = st.sidebar.selectbox("Select Client", df_order['Client Name'].unique())
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
            fig_order_pie = px.pie(df_order, names="Client Name", values="Values", title="Order Count")
            st.plotly_chart(fig_order_pie)

 
      
    elif page == "Generate Reports":
        # Options for data level selection
        data_level_options = ["Application", "Order", "Both"]
        selected_data_level = st.selectbox("Select Data Level", data_level_options)

        # Options for time frame selection
        time_frame_options = ["Weekly", "Monthly", "Quarterly"]
        selected_time_frame = st.selectbox("Select Time Frame", time_frame_options)

        st.write("### Date Range Filter")

        # Date Range Filter
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

        # Default date range for initial data display
        if not start_date:
            start_date = pd.to_datetime("2023-01-01")
        if not end_date:
            end_date = pd.to_datetime("2023-12-31")

        # Fetch comparison data
        comparison_data = fetch_comparison_data(start_date, end_date, selected_data_level, selected_time_frame, conn)

        # Define column names based on the selected data level
        if selected_data_level == "Application":
            columns = ["Stat Date", "Total Completed Applications", "Total Approved Applications", "Total Yet to Create Applications", "Total Rejected Applications"]
        elif selected_data_level == "Order":
            columns = ["Stat Date", "Total Manual Orders", "Total Auto Orders", "Total Remaining Orders", "Total Total Orders"]
        else:
            columns = [
                "Stat Date",
                "Total Completed Applications", "Total Approved Applications", "Total Yet to Create Applications", "Total Rejected Applications",
                "Total Manual Orders", "Total Auto Orders", "Total Remaining Orders", "Total Total Orders"
            ]

        # Create a DataFrame for comparison data
        df_comparison = pd.DataFrame(comparison_data, columns=columns)

        # Display the comparison data
        st.write("### Comparison Data")
        st.dataframe(df_comparison)

        # Interactive Line Chart for Comparison
        st.write(f"### {selected_time_frame} Comparison")
        fig_comparison = px.line(df_comparison, x="Stat Date", y=columns[1:], title=f"{selected_data_level} {selected_time_frame} Comparison")
        st.plotly_chart(fig_comparison)
   

    # Close the database connection
    # conn.close()
else:
    st.error("Unable to connect to the database.")
