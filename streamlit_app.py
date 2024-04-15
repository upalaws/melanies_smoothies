# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 
import requests

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
cnx = st.connection("snowflake") 
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("SEARCH_ON"),col("FRUIT_NAME")).filter(col("SEARCH_ON").isNotNull())
st.dataframe(data = my_dataframe,use_container_width =  True)
ingredients_list = st.multiselect('Choose upto 5 ingredients',
                                  my_dataframe,
                                  max_selections = 5)

if ingredients_list:
    st.write(ingredients_list) ; 
    st.text(ingredients_list) ; 
    ingredients_list_string = '' 
    for fruit_chosen in ingredients_list:
        ingredients_list_string += fruit_chosen+','
        st.subheader(fruit_chosen + ' Nutrition Information' )
        fruityvice_response  = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data = fruityvice_response.json() , use_container_width = True )
        

    my_sql =  """ insert into smoothies.public.orders (INGREDIENTS,NAME_ON_ORDER) 
             values ( '""" + ingredients_list_string + """','""" + name_on_smoothie + """')"""
    st.write (my_sql)
    time_to_insert = st.button('Submit Order')

    if(time_to_insert):
        session.sql(my_sql).collect()
        st.success('Your smoothie is ordered !!!' )
        
   ### Calling Fruityvice app API 
## fruityvice_response  = requests.get("https://fruityvice.com/api/fruit/watermelon")

 



    
