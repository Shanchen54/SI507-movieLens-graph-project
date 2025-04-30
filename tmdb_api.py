import requests
import pandas as pd

TMDB_BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0N2ZiNDlhMTk4MmViZDA4ZDc2OTc4Mjc1Y2NiYzk3NiIsIm5iZiI6MTcxNjIyMTk4Ny4wNjksInN1YiI6IjY2NGI3ODIzNmY0MGMzOTVmNDkzM2FhMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rZXU05L8soDJ2_ON9BHKD_gaPH-9fSdy0W-XMeXo2Ec"

def get_movie_info(movie_title, links_df, movies_path="ml-20m/movies.csv"):
    """
    Query TMDb for detailed movie info using TMDb Bearer Token auth.

    Parameters:
        movie_title (str): fuzzy or exact movie title from MovieLens
        links_df (pd.DataFrame): must include movieId and tmdbId
        movies_path (str): path to MovieLens movies.csv

    Returns:
        dict: movie info or error message
    """
    # movie title
    movies_df = pd.read_csv(movies_path)
    movies_df["title"] = movies_df["title"].astype(str).str.strip()
    matches = movies_df[movies_df["title"].str.contains(movie_title, case=False, na=False)]

    if matches.empty:
        return {"error": f"No movie title contains: {movie_title}"}
    if len(matches) > 10:
        return {"error": f"Too many matches for '{movie_title}', please be more specific."}

    for _, row in matches.iterrows():
        response = input(f"Did you mean: {row['title']}? [y/n] ")
        if response.strip().lower() == "y":
            target_id = row["movieId"]
            break
    else:
        return {"error": "No movie confirmed."}

    # search tmdbId
    tmdb_row = links_df[links_df["movieId"] == target_id]
    if tmdb_row.empty or pd.isna(tmdb_row["tmdbId"].values[0]):
        return {"error": f"No TMDb ID found for movieId {target_id}"}
    
    tmdb_id = int(tmdb_row["tmdbId"].values[0])

    # TMDb API
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"TMDb API error: {response.status_code}"}

    data = response.json()

    return {
        "title": data.get("title"),
        "overview": data.get("overview"),
        "release_date": data.get("release_date"),
        "runtime": data.get("runtime"),
        "vote_average": data.get("vote_average"),
        "genres": [g["name"] for g in data.get("genres", [])],
        "poster_url": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else None
    }
