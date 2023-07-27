import streamlit as st
import streamlit.components.v1 as components

# Adding Image to web app
st.set_page_config(page_title="Nik",layout="wide",initial_sidebar_state="auto")
st.title("Nikhil_Dashboard")

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

'''

def create_connection():
    connection = psycopg2.connect(
        host="your_host",
        database="your_database",
        user="your_username",
        password="your_password"
    )
    return connection
def fetch_data():
    connection = create_connection()
    query = "SELECT * FROM your_table;"
    data = pd.read_sql(query, connection)
    connection.close()
    return data

def update_data(data):
    connection = create_connection()
    with connection.cursor() as cursor:
        for index, row in data.iterrows():
            query = f"UPDATE your_table SET column1 = '{row['column1']}', column2 = '{row['column2']}' WHERE id = {row['id']};"
            cursor.execute(query)
        connection.commit()
    connection.close()

    '''


