import pandas as pd

def clean_columns(df):
    # Strip spaces and remove BOM from column names
    df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=False)
    # If there's a title column, ensure it's string and trimmed
    if "title" in df.columns:
        df["title"] = df["title"].astype(str).str.strip()
    return df

def load_data(
    ratings_path="ml-20m/ratings.csv",
    movies_path="ml-20m/movies.csv",
    tags_path="ml-20m/tags.csv",
    genome_scores_path="ml-20m/genome-scores.csv",
    genome_tags_path="ml-20m/genome-tags.csv",
    links_path="ml-20m/links.csv"
):
    """
    load the full MovieLens dataset with no filtering

    Returns:
        dict of pandas DataFrames
    """
    ratings = clean_columns(pd.read_csv(ratings_path))
    print(f"Loaded ratings: {ratings.shape}")

    movies = clean_columns(pd.read_csv(movies_path))
    print(f"Loaded movies: {movies.shape}")

    tags = clean_columns(pd.read_csv(tags_path))
    print(f"Loaded tags: {tags.shape}")

    genome_tags = clean_columns(pd.read_csv(genome_tags_path))
    print(f"Loaded genome_tags: {genome_tags.shape}")

    links = clean_columns(pd.read_csv(links_path))
    print(f"Loaded links: {links.shape}")

    genome_scores = clean_columns(pd.read_csv(genome_scores_path))
    print(f"Loaded genome_scores: {genome_scores.shape}")

    return {
        "ratings": ratings,
        "movies": movies,
        "tags": tags,
        "genome_scores": genome_scores,
        "genome_tags": genome_tags,
        "links": links
    }


def load_filtered_data(
    ratings_path="ml-20m/ratings.csv",
    movies_path="ml-20m/movies.csv",
    tags_path="ml-20m/tags.csv",
    genome_scores_path="ml-20m/genome-scores.csv",
    genome_tags_path="ml-20m/genome-tags.csv",
    links_path="ml-20m/links.csv",
    min_user_ratings=200,
    min_movie_ratings=400
):
    """
    load and filter MovieLens dataset: keep active users and popular movies only

    Returns:
        dict of pandas DataFrames
    """
    ratings = clean_columns(pd.read_csv(ratings_path))

    # Filter users
    user_counts = ratings["userId"].value_counts()
    active_users = user_counts[user_counts >= min_user_ratings].index
    ratings = ratings[ratings["userId"].isin(active_users)]

    # Filter movies
    movie_counts = ratings["movieId"].value_counts()
    popular_movies = movie_counts[movie_counts >= min_movie_ratings].index
    ratings = ratings[ratings["movieId"].isin(popular_movies)]

    print(f"Filtered ratings: {ratings.shape}")

    movies = clean_columns(pd.read_csv(movies_path))
    print(f"Loaded movies: {movies.shape}")

    tags = clean_columns(pd.read_csv(tags_path))
    print(f"Loaded tags: {tags.shape}")

    genome_tags = clean_columns(pd.read_csv(genome_tags_path))
    print(f"Loaded genome_tags: {genome_tags.shape}")

    links = clean_columns(pd.read_csv(links_path))
    print(f"Loaded links: {links.shape}")

    selected_movie_ids = ratings["movieId"].unique()
    genome_scores = clean_columns(pd.read_csv(genome_scores_path))
    genome_scores = genome_scores[genome_scores["movieId"].isin(selected_movie_ids)]
    print(f"Filtered genome_scores: {genome_scores.shape}")

    return {
        "ratings": ratings,
        "movies": movies,
        "tags": tags,
        "genome_scores": genome_scores,
        "genome_tags": genome_tags,
        "links": links
    }