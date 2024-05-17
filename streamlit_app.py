import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor
import requests

# Snowflake connection parameters
snowflake_config = {
    "account": "JABHSPH-JI44714",
    "user": "BISHALDATAARMY",
    "password": "Meronamebishal@12",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC",
    "client_session_keep_alive": True
}

# Establish Snowflake connection
try:
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor(DictCursor)
except Exception as e:
    st.error(f"Error: Failed to connect to Snowflake: {str(e)}")
    st.stop()

# Streamlit app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input('Name On Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Fetching fruit options from Snowflake
try:
    cursor.execute("SELECT FRUIT_NAME FROM smoothies.public.fruit_options")
    fruit_options = [row['FRUIT_NAME'] for row in cursor.fetchall()]
except Exception as e:
    st.error(f"Error: Failed to fetch fruit options: {str(e)}")
    st.stop()

# Multiselect for ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_options)
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    
    # Prepare the insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order.strip()}')
    """

    # Button to submit the order
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        try:
            cursor.execute(my_insert_stmt)
            conn.commit()
            st.success('Your Smoothie is ordered!')
        except Exception as e:
            st.error(f"Error: Failed to insert order: {str(e)}")

# Close Snowflake connection
conn.close()
