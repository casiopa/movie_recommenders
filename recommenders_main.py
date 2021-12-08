import streamlit as st
from recommenders_functions import *


st.set_page_config(page_title='Movie Recommenders Systems',
                   page_icon='https://www.google.com/s2/favicons?domain=www.imdb.com',
                   layout="wide")



# Pone el radio-button en horizontal. Afecta a todos los radio button de una página.
# Por eso está puesto en este que es general a todo
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)


#st.sidebar.image('images/800px-IMDB_Logo_2016.svg.png', width=200)
st.sidebar.header('Movie Recommenders Systems')
st.sidebar.markdown('Knowledge, Content and Colaborative Recommender Systems ')


menu = st.sidebar.radio(
    "",
    ("Data", "Simple", "Knowledge-based", "Content-based"),
)


st.sidebar.markdown('---')
st.sidebar.write('Ana Blanco | Julio 2021 anablancodelgado@gmail.com https://casiopa.github.io/')


if menu == 'Data':
    set_data()
    #pass
elif menu == 'Simple':
    set_simple()
    #pass
elif menu == 'Knowledge-based':
    #set_knowledge()
    pass
elif menu == 'Content-based':
    #set_content()
    pass







