import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w185" + data['poster_path']

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    recommended_movies_posters=[]
    
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from API 
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        
            # print(i[0])
    return recommended_movies,recommended_movies_posters


movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommonder System')

selected_movie_name=st.selectbox('How would be like to be contacted?',
movies['title'].values)


if st.button('Recommend'):
    names,poster=recommend(selected_movie_name)
    cols= st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(poster[i])
      
      
      
      