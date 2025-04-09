import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom smoothie!
 """)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
#option = st.selectbox(
#    "What is your favorite fruit ?",
#    ("Banana", "strawberries", "Peaches"),
#)

#st.write("You selected:", option)
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingredients_list=st.multiselect(
    'choose up to 5 ingredients',
     my_dataframe,
     max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+= fruit_chosen+' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        st_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""
    time_to_insert=st.button('Submit Order')
    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

#my_dataframe1 = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#editable_df = st.data_editor(my_dataframe1)


#st.text(smoothiefroot_response.json())
