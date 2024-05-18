import pandas as pd

# Fetching fruit options from Snowflake
try:
    cursor.execute("SELECT FRUIT_NAME, SEARCH_ON FROM smoothies.public.fruit_options")
    fruit_options = [(row['FRUIT_NAME'], row['SEARCH_ON']) for row in cursor.fetchall()]
    pd_df = pd.DataFrame(fruit_options, columns=['FRUIT_NAME', 'SEARCH_ON'])
except Exception as e:
    st.error(f"Error: Failed to fetch fruit options: {str(e)}")

# Multiselect for ingredients
if 'pd_df' in locals():
    ingredients_list = st.multiselect('Choose up to 5 ingredients:', pd_df['FRUIT_NAME'].tolist())
    if ingredients_list:
        ingredients_string = ' '.join(ingredients_list)
        
        for fruit_chosen in ingredients_list:
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write('The search value for ', fruit_chosen,' is ', search_on, ',')
            
            st.subheader(fruit_chosen+ ' Nutrition Information')
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
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
