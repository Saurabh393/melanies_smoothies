# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customise your smoothies :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie.")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on the cup of smoothie will be :", name_on_order)


#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert snowpark dataframe to Pandas, so we can use LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

Ingredient_List = st.multiselect("Chosse upto 5 ingredient"
                                , my_dataframe
                                , max_selections=6)

Ingredient_string = ''

if Ingredient_List :
    #st.write(Ingredient_List)
    #st.text(Ingredient_List)


    for Fruit_chosen in Ingredient_List:
        Ingredient_string += (Fruit_chosen + ' ')

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(Fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + Fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


st.write("You've chosen : " + Ingredient_string)
st.write("*Please check the selected ingredients and then submit your order*.")

        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + Ingredient_string + """', '""" + name_on_order + """')"""

#st.write(my_insert_stmt)
#st.stop()
time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' + name_on_order +'!', icon="✅")

