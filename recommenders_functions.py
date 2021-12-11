import streamlit as st
import numpy as np
import pandas as pd
from ast import literal_eval

from recommenders_variables import *



@st.experimental_memo()
def load_movies():
    data = pd.read_csv(data_path + 'movies_metadata_v2.csv', low_memory=False)
    return data

@st.experimental_memo(persist='disk')
def extract_year(df_input):
    df = df_input.copy()
    
    #Extract year from release_date
    df['year'] = df['release_date'].apply(lambda x: str(x)[:4] if x != np.nan else 0)
    
    #Convert years to integers and 'nan' as 0
    df['year'] = df['year'].apply(lambda x: int(x) if x != 'nan' else 0)

    return df

@st.experimental_memo(persist='disk')
def explode_genre(df_input):
    df = df_input.copy()

    #Convert NaNs into string of empty lists
    df['genres'] = df['genres'].fillna('[]')

    #Apply literal_eval to convert string into list object
    df['genres'] = df['genres'].apply(literal_eval)

    #Convert list of dictionaries to a list of strings
    df['genres'] = df['genres'].apply(lambda x: [g['name'] for g in x] if len(x)>0 else [])
    df.head()

    #Create a new feature by exploding genres
    g = df.apply(lambda x: pd.Series(x['genres']),axis=1).stack().reset_index(level=1, drop=True)
    g.name = 'genre'

    #Create a new dataframe gen_df which by dropping the old 'genres' feature and adding the new 'genre'.
    gen_df = df.drop('genres', axis=1).join(g)

    return gen_df

    
@st.experimental_memo()
def get_genres(df):
    genres = tuple(set(df.genre.unique().astype('str'))-set(str(np.nan)))
    return genres




def simple_recommender(df, percentile):
    movies = df.copy()
    
    #Compute the values of C and m for the filtered movies
    C = movies['vote_average'].mean()
    m = movies['vote_count'].quantile(percentile)
    
    #Only consider movies longer than 45 minutes and shorter than 300 minutes
    q_movies = movies[(movies['runtime'] >= 45) & (movies['runtime'] <= 300)]
    
    #Only consider movies that have higher than m votes. Save this in a new dataframe q_movies
    q_movies = q_movies.copy().loc[q_movies['vote_count'] >= m]
    
    #Calculate score using the IMDB formula
    q_movies['score'] = q_movies.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) 
                                                   + (m/(m+x['vote_count']) * C),
                                       axis=1)

    #Sort movies in descending order of their scores
    q_movies = q_movies.sort_values('score', ascending=False)
    
    return q_movies


def knowledge_recommender(df, percentile, genre, low_time, high_time, low_year, high_year):   
    #Define a new movies variable to store the preferred movies. Copy the contents to movies
    movies = df.copy()
    
    #Filter based on the condition
    movies = movies[(movies['genre'] == genre) & 
                    (movies['runtime'] >= low_time) & 
                    (movies['runtime'] <= high_time) & 
                    (movies['year'] >= low_year) & 
                    (movies['year'] <= high_year)]
    
    #Compute the values of C and m for the filtered movies
    C = movies['vote_average'].mean()
    m = movies['vote_count'].quantile(percentile)
    
    #Only consider movies that have higher than m votes. Save this in a new dataframe q_movies
    q_movies = movies.copy().loc[movies['vote_count'] >= m]
    
    #Calculate score using the IMDB formula
    q_movies['score'] = q_movies.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) 
                                                   + (m/(m+x['vote_count']) * C),
                                       axis=1)

    #Sort movies in descending order of their scores
    q_movies = q_movies.sort_values('score', ascending=False)
    
    return q_movies



def print_movies(df):
    for i, idx in enumerate(df.index):        
        poster_url = tmdb_image_path + df.loc[idx, 'poster_path']
        tmdb_url = tmbd_path + str(df.loc[idx, 'id'])
        vote_count = f"{df.loc[idx, 'vote_count']:,}"

        col1, col2 = st.columns([1,8])
        col1.image(poster_url, use_column_width=True)
        col2.markdown(f"##### {str(i+1)}. {df.loc[idx, 'title']}")
        col2.caption(df.loc[idx, 'overview'])
        col2.markdown(f"""Recommender score:  **{str(round(df.loc[idx, 'score'], 2))}**  
                          TMDb rating: **{str(round(df.loc[idx, 'vote_average'], 2))}**   |   {vote_count} votes   |   [TMDb page]({tmdb_url})""")
    



def set_data():
    st.title('Movies Recommender Systems - Data')

    movies = load_movies()
    st.header('`movies_metadata_v2`')
    st.dataframe(movies)


def set_simple():
    st.title('Simple Recommender System')
    st.subheader('TMDb Top 250')

    movies = load_movies()
    percentile = st.slider('Percentile', value=0.95, min_value=0.5, max_value=1.0, step=0.05)
    best_movies = simple_recommender(movies, percentile)[['title', 'id', 'imdb_id', 'score', 'vote_average', 'vote_count', 'runtime', 'poster_path', 'overview']].head(250)
    print_movies(best_movies)
    #st.dataframe(best_movies)


def set_knowledge():
    st.title('Knowledge-based Recommender System')
    movies = load_movies()
    
    # Get new feature year
    y_movies = extract_year(movies)

    # Explode genres to a new column
    y_g_movies = explode_genre(y_movies)

    with st.form("knowledge_form"):
        st.subheader('Filter movies')

        col1, col2 = st.columns(2)
        percentile = col1.slider('Percentile', value=0.95, min_value=0.5, max_value=1.0, step=0.05)
        genre = col2.selectbox('Choose a genre',
             get_genres(y_g_movies))
        low_time = col1.number_input('Minimun minutes:', min_value=20, max_value=240, value=45, step=1)
        high_time = col1.number_input('Maximun minutes:', min_value=20, max_value=240, value=120, step=1)
        low_year = col2.slider('From year:', min_value=1870, max_value=2017, value=2010, step=1)
        high_year = col2.slider('To year:', min_value=1870, max_value=2017, value=2017, step=1)

        recommend_button = st.form_submit_button("Recommend")
        
    if recommend_button:
        best_movies = knowledge_recommender(y_g_movies, percentile, genre, low_time, high_time, low_year, high_year).head(50)
        print_movies(best_movies)
