import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """)

name_on_order =  st.text_input('Name On Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe)
if ingredients_list: 
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)
    
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{}', '{}')
    """.format(ingredients_string.strip(), name_on_order.strip())
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert: 
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon='✅')
