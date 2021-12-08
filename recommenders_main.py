import streamlit as st
from recommenders_functions import *


st.set_page_config(page_title='Movie Recommenders Systems',
                   page_icon='https://www.themoviedb.org/assets/2/favicon-32x32-543a21832c8931d3494a68881f6afcafc58e96c5d324345377f3197a37b367b5.png',
                   layout="wide")



# Pone el radio-button en horizontal. Afecta a todos los radio button de una página.
# Por eso está puesto en este que es general a todo
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)


st.sidebar.image('images/blue_square_1-5bdc75aaebeb75dc7ae79426ddd9be3b2be1e342510f8202baf6bffa71d7f5c4.png', width=260)
st.sidebar.write('             ')
st.sidebar.image('images/movielens-logo.svg', width=100)
st.sidebar.header('Movie Recommenders Systems')
#st.sidebar.markdown('Knowledge, Content and Colaborative Recommender Systems ')


menu = st.sidebar.radio(
    "Data & Recommender Systems",
    ("Data", "Simple - IMDb Top 250", "Knowledge-based", "Content-based"),
)

st.sidebar.markdown('---')
st.sidebar.write('Ana Blanco | Diciembre 2021 anablancodelgado@gmail.com https://casiopa.github.io/')

if menu == 'Data':
    set_data()
    #pass
elif menu == 'Simple - IMDb Top 250':
    set_simple()
    #pass
elif menu == 'Knowledge-based':
    #set_knowledge()
    pass
elif menu == 'Content-based':
    #set_content()
    pass







