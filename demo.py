import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

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


def fetch_data():
    # Fetch data from the PostgreSQL database using Pandas
    # Replace the following line with your database query
    data = pd.DataFrame({
        'Column1': [1, 2, 3, 4, 5, 6, 7, 8, 7, 2],
        'Column2': ['A', 'B', 'C', 'D', 'E' ,'F' ,'G','H' ,'d' ,'A'],
    })

    return data
def main():
    
    # Fetch data from the database
    data = fetch_data()

    # Display the data in a Streamlit dataframe
    st.write("Current Data:")
    st.dataframe(data)

    # Add a search bar
    st.write("Search Bar in Streamlit")

    search_query = st.text_input("Search:", "")

    # Filter the data based on the search query
    if search_query:
        filtered_data = data[data.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]
        st.write("Filtered Data:")
        st.dataframe(filtered_data)

if __name__ == "__main__":
    main()

def main():
    st.title("Editable and Interactive Table with Streamlit")

    # Fetch data from the database
    data = fetch_data()

    # Display the data in a Streamlit dataframe
    st.write("Current Data:")
    st.dataframe(data)

    # Create an empty DataFrame to hold edited data
    edited_data = pd.DataFrame(data.values, columns=data.columns)
    user_input = st.number_input("Select row / index :", step=1, value=0, format="%d")
    # Display the result
    st.write(f"You entered: {user_input}")

    # Edit the data in the Streamlit dataframe
    for index, row in data.iterrows():
       if index ==user_input:
              for col in data.columns:
                     edited_data.at[index, col] = st.text_input(f"Edit {col}:", value=row[col])

    # If the user clicks the 'Submit' button, update the data
    if st.button("Submit"):
        # Here, you would implement the logic to update the PostgreSQL database with the edited data
        # For this example, we'll just display the edited data
        st.write("Edited Data:")
        st.dataframe(edited_data)

if __name__ == "__main__":
    main()

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


