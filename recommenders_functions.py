import streamlit as st
import pandas as pd
from recommenders_variables import *





@st.cache(persist=True)
def load_movies():
    data = pd.read_csv(data_path + 'movies_metadata.csv', low_memory=False)
    return data


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


def print_movies(df):
    for i, idx in enumerate(df.index):
        st.subheader(str(i+1) + '. ' + df.loc[idx, 'title'])
        poster_url = tmdb_image_path + df.loc[idx, 'poster_path']
        print(poster_url)
        col1, col2 = st.columns([1,5])
        col1.image(poster_url, use_column_width=True)
        col2.write(df.loc[idx, 'overview'])
        col2.write('SCORE: '+ str(round(df.loc[idx, 'score'], 2)))





def set_data():
    movies = load_movies()
    st.write(movies)

def set_simple():
    movies = load_movies()
    percentile = st.slider('Percentile', value=0.95, min_value=0.5, max_value=1.0, step=0.05)
    best_movies = simple_recommender(movies, percentile)[['title', 'vote_count', 'vote_average', 'score', 'runtime', 'poster_path', 'overview']].head(25)
    print_movies(best_movies)
    #st.dataframe(best_movies)