import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="IMDb Movie Dashboard",
    layout="wide"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

df = pd.read_csv("imdb_top_1000.csv", encoding='latin1')

# -----------------------------------
# TITLE
# -----------------------------------

st.title("🎬 IMDb Movie Ratings Dashboard")

st.markdown("Analysis of Top 1000 IMDb Movies")

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------

st.sidebar.header("Filters")

genre_filter = st.sidebar.multiselect(
    "Select Genre",
    options=df['Genre'].unique(),
    default=df['Genre'].unique()
)

filtered_df = df[df['Genre'].isin(genre_filter)]

# -----------------------------------
# KPI CARDS
# -----------------------------------

avg_rating = round(filtered_df['IMDB_Rating'].mean(), 2)

total_movies = filtered_df['Series_Title'].count()

top_movie = filtered_df.sort_values(
    by='IMDB_Rating',
    ascending=False
)['Series_Title'].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric("⭐ Average Rating", avg_rating)

col2.metric("🎥 Total Movies", total_movies)

col3.metric("🏆 Top Rated Movie", top_movie)

# -----------------------------------
# GENRE ANALYSIS
# -----------------------------------

st.subheader("Average IMDb Rating by Genre")

genre_rating = filtered_df.groupby('Genre')[
    'IMDB_Rating'
].mean().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    x=genre_rating.values,
    y=genre_rating.index,
    ax=ax
)

st.pyplot(fig)

# -----------------------------------
# RATING DISTRIBUTION
# -----------------------------------

st.subheader("Distribution of IMDb Ratings")

fig2, ax2 = plt.subplots(figsize=(10,5))

sns.histplot(
    filtered_df['IMDB_Rating'],
    bins=20,
    kde=True,
    ax=ax2
)

st.pyplot(fig2)

# -----------------------------------
# TOP MOVIES TABLE
# -----------------------------------

st.subheader("Top Rated Movies")

top_movies = filtered_df.sort_values(
    by='IMDB_Rating',
    ascending=False
)[['Series_Title', 'Genre', 'IMDB_Rating']].head(10)

st.dataframe(top_movies)

# -----------------------------------
# MOVIES RELEASED OVER YEARS
# -----------------------------------

st.subheader("Movies Released Over Years")

# Convert year column safely
filtered_df['Released_Year'] = pd.to_numeric(
    filtered_df['Released_Year'],
    errors='coerce'
)

year_data = filtered_df['Released_Year'] \
    .value_counts() \
    .sort_index()

fig3, ax3 = plt.subplots(figsize=(12,5))

ax3.plot(
    year_data.index,
    year_data.values,
    marker='o'
)

# Show fewer year labels
ax3.set_xticks(year_data.index[::10])

plt.xticks(rotation=45)

ax3.set_xlabel("Year")

ax3.set_ylabel("Number of Movies")

ax3.set_title("Movies Released Over Years")

st.pyplot(fig3)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.markdown("Dashboard Created By Ibrahim Khan")