##1
import streamlit as st                              
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout='wide')      # [For Zooming Everything]
tracks = pd.read_csv ("data/dataset.csv")

# pd.isnull(tracks).sum()                             
# tracks.info()


##2
#Delete missing values
tracks=tracks.dropna()


##3
#Check for duplicate rows 
duplicate_rows = tracks[tracks.duplicated(subset=['track_id'])]


##4
#Delete Duplicates
track_clean = tracks.drop_duplicates(subset="track_id", keep='first', inplace=False)


##5
# track_clean.describe().transpose()
#Populatiry sorting

st.title('SPOTIFY DATA ANALYSIS')


##6
most_popular = track_clean.query ('popularity>90', inplace = False).sort_values('popularity', ascending = False)
st.subheader('Most popular track ')
st.dataframe(most_popular[:20], use_container_width=True)


##7
popularity_genre = track_clean.groupby([track_clean['track_genre']])['popularity'].mean().sort_values(ascending = False)
st.subheader('Most popular genre ')
st.dataframe(popularity_genre[:20], use_container_width=True)


##8
popularity_artist = track_clean.groupby([track_clean['artists']])['popularity'].mean().sort_values(ascending = False)
st.subheader('Most popular artist ')
st.dataframe(popularity_artist[:20], use_container_width=True)


##9
popularity_album = track_clean.groupby([track_clean['album_name']])['popularity'].mean().sort_values(ascending = False)
st.subheader('Most popular album ')
st.dataframe(popularity_album[:20], use_container_width=True)


##10
popularity_explicit = track_clean.groupby([track_clean['explicit']== True])['popularity'].mean().sort_values(ascending = False)
st.subheader('Most popular explicit ')
st.dataframe(popularity_explicit[:20], use_container_width=True)


##11
#Popularity and Speechiness

track_clean = track_clean.copy()  # Create a copy of the DataFrame

def categorize_speechiness(value):
    if value > 0.66:
        return 'entirely of spoken'
    elif value > 0.33:
        return 'music and speech'
    else:
        return 'non-speech-like'

track_clean['speechiness_category'] = track_clean['speechiness'].apply(categorize_speechiness)

popularity_speechiness = track_clean.groupby('speechiness_category')['popularity'].mean().sort_values(ascending=False)
st.subheader('Speechiness')
st.dataframe(popularity_speechiness[:20], use_container_width=True)


##12
#Changing ms to s

track_clean['duration'] = track_clean['duration_ms'].apply(lambda x: round(x/1000))
track_clean.drop('duration_ms', inplace = True, axis = 1)


##13
#I will focus on the top 20 to do the following analysis 

genre_popularity = track_clean.groupby('track_genre')['popularity'].mean()

genre_popularity_sorted = genre_popularity.sort_values(ascending=False)
#This code calculates the average popularity for each genre and sorts them in descending order. 
#It provides insights into which genres tend to have higher or lower popularity ratings.
top_genres = genre_popularity_sorted.head(20)


##14
#Correlation between all the variables

corr_pop = track_clean.drop(['key', 'mode', 'time_signature', 'tempo', 'Unnamed: 0'], axis=1).corr(method='pearson', numeric_only=True)
#This code calculates the Pearson correlation coefficient between popularity and other musical features,
# excluding irrelevant columns.

plt.figure(figsize=(14,6))
heatmap = sns.heatmap(corr_pop,annot=True,fmt='.3f', vmin=-1.0, vmax=1.0, center=0.05, cmap='inferno', linewidths=1, linecolor='Black')
heatmap.set_title("Correlation HeatMap Between Variables")
heatmap.set_xticklabels(heatmap.get_xticklabels(),rotation=90)
#The heatmap helps identify which features have a stronger positive or negative correlation with popularity.


##15
#Genre-based analysis of popularity
st.subheader('Average Popularity by Genre')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_genres.index, y=top_genres.values, palette="husl")
plt.title("Average Popularity by Genre")
plt.xlabel('Genre')
plt.ylabel('Average Popularity')
plt.xticks(rotation=90)
plt.tight_layout()
st.pyplot(fig)
#This code creates a bar plot that displays the average popularity for each genre.


##16
#Energy distribution in different genres 
high_energy_genres = top_genres.head(20)  # Select the top 20 genres with highest popularity

st.subheader('Distribution of Energy in High Energy Genres')
fig, ax = plt.subplots(figsize=(12, 6))

# Box plot or violin plot for high energy genres
sns.boxplot(x=track_clean[track_clean['track_genre'].isin(high_energy_genres.index)]['track_genre'], y='energy', data=track_clean, palette="husl")
plt.title("Distribution of Energy in High Energy Genres")
plt.xlabel("Genre")
plt.ylabel("Energy")
plt.xticks(rotation=45)
st.pyplot(fig)


##17
#Relation between speechiness and popularity
#Filter the tracks_clean DataFrame to include only the rows for top genres
top_genres_data = track_clean[track_clean['track_genre'].isin(top_genres.index)]

#Calculating the average popularity by speechiness category within the filtered DataFrame
popularity_speechiness_filtered = top_genres_data.groupby('speechiness_category')['popularity'].mean()

#Creating the bar plot
st.subheader('Average Popularity by Speechiness Category for Top Genres ')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=popularity_speechiness_filtered.index, y=popularity_speechiness_filtered.values, palette="husl")
plt.title("Average Popularity by Speechiness Category for Top Genres")
plt.xlabel("Speechiness Category")
plt.ylabel("Average Popularity")
st.pyplot(fig)
#This code creates a bar plot showing the average popularity by speechiness category for the top genres.


##18
#Regression between danceability and top 20 popularity

danceability = track_clean['danceability']
popularity = track_clean['popularity']

st.subheader('Relation Between Danceabililty and Popularity')
fig, ax = plt.subplots(figsize=(12, 6))
sns.scatterplot(x=top_genres_data['danceability'], y=top_genres_data['popularity'])
plt.title("Relationship between Danceability and Popularity (Top 20 Songs)")
plt.xlabel("Danceability")
plt.ylabel("Popularity")
st.pyplot(fig)
#This code creates a scatter plot to visualize the relationship between danceability and popularity for the top 20 songs.


##19
#Correlation between duration and popularity
st.subheader('Correlation between Duration and Popularity by Genre')
fig, ax = plt.subplots(figsize=(12, 6))

sns.scatterplot(x='duration', y='popularity', hue='track_genre', data=track_clean[track_clean['track_genre'].isin(top_genres.index)], alpha=0.7, palette='husl')
plt.title("Duration vs. Popularity by Genre")
plt.xlabel("Duration in seconds")
plt.ylabel("Popularity")
st.pyplot(fig)
#This code creates a scatter plot to explore the correlation between duration and popularity for each genre within the top genres.
