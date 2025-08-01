# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd



# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom Smoothie"
)


name_on_order = st.text_input("Name of Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON')) 
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()


pd_df= my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    )



if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen+' '
        
    #st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order )
            values ('""" + ingredients_string + """','"""""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+name_on_order+ """!!""" , icon="✅")


import requests

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
      ingredients_string += fruit_chosen+''
      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

      st.subheader(fruit_chosen +'Nutrition Information')
      smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/all"+search_on)
      sf_df = st.dataframe(data = smoothiefroot_response.json(),use_container_width = True)





#New section to display smoothiefroot nutrition information
#st.text(smoothiefroot_response.json())

    #if ingredients_string:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")



#commented for old lesson1
#option = st.selectbox(
 #   "What is your favorite fruit?",
  #  ("Banana", "Strawberries", "Peaches"),)

#st.write("Your favorite fruit is:", option)
