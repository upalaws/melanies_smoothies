# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col 

# Write directly to the app
st.title(":tropical_drink: Customize your smoothie! :tropical_drink:")
st.write(
    """
    Choose the fruits you want to add in your custom smoothie!
    
    """
)

name_on_smoothie = st.text_input("Name on Smoothie !!!")
st.write("The name on your smoothie will be :",name_on_smoothie)

option = st.selectbox(
    'What is your favourite fruit ?',
    ('Banana', 'Orange', 'Strawberry','Apple'))

st.write('Your favourite fruit is :', option)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
##st.dataframe(data = my_dataframe,use_container_width =  True)
ingredients_list = st.multiselect('Choose upto 5 ingredients',
                                  my_dataframe,
                                  max_selections = 5)

ingredients_list_string =''

if ingredients_list:
    st.write(ingredients_list) ; 
    st.text(ingredients_list) ; 
    ingredients_list_string = '' 
    for x in ingredients_list:
        ingredients_list_string += x+','

    my_sql =  """ insert into smoothies.public.orders (INGREDIENTS,NAME_ON_ORDER) 
             values ( '""" + ingredients_list_string + """','""" + name_on_smoothie + """')"""
    st.write (my_sql)
    time_to_insert = st.button('Submit Order')

    if(time_to_insert):
        session.sql(my_sql).collect()
        st.success('Your smoothie is ordered !!!' )
        
    

    