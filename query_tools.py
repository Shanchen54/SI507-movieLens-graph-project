import pandas as pd
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_movies(title_partial, genome_scores_df, movies_df, top_n=10, restrict_genre=False):
    """
    recommend similar movies based on fuzzy title match and tag similarity

    Parameters:
        title_partial (str): partial movie title
        genome_scores_df (pd.DataFrame): tag relevance
        movies_df (pd.DataFrame): must include movieId, title, genres
        top_n (int): number of results
        restrict_genre (bool): if True, only recommend movies with overlapping genres

    Returns:
        pd.DataFrame with [title, genres, similarity]
    """
    # Ensure titles are strings and stripped
    movies_df["title"] = movies_df["title"].astype(str).str.strip()

    # Fuzzy match by partial title
    matches = movies_df[movies_df["title"].str.contains(title_partial, case=False, na=False)]

    if matches.empty:
        raise ValueError(
            f"No movie title matched '{title_partial}'. "
            f"Try a different keyword, or try 'Title, The' or 'Title, A'."
        )
    if len(matches) > 10:
        print(f"Too many matches ({len(matches)}). Please be more specific.")
        return None

    for _, row in matches.iterrows():
        response = input(f"Did you mean '{row['title']}' (genres: {row['genres']})? [y/n] ")
        if response.strip().lower() == "y":
            target = row
            break
    else:
        print("No movie selected.")
        return None

    target_id = target["movieId"]

    # Pivot matrix: movie × tag
    pivot = genome_scores_df.pivot(index="movieId", columns="tagId", values="relevance").fillna(0)
    if target_id not in pivot.index:
        raise ValueError("Target movie not in genome_scores.")

    sim = cosine_similarity(pivot.loc[[target_id]], pivot)[0]
    result = pd.DataFrame({
        "movieId": pivot.index,
        "similarity": sim
    }).sort_values("similarity", ascending=False)

    result = result[result["movieId"] != target_id]
    result = result.merge(movies_df, on="movieId")

    if restrict_genre:
        target_genres = set(str(target["genres"]).split("|"))
        result = result[result["genres"].apply(
            lambda g: isinstance(g, str) and g.lower() != "no genres listed"
            and bool(target_genres & set(g.split("|")))
        )]

    return result[["title", "genres", "similarity"]].head(top_n)



def shortest_path_between_users(graph, user1, user2, movies_df):
    """
    find and print the shortest path between two users in a bipartite graph

    Parameters:
        graph (nx.Graph): bipartite user-movie graph
        user1, user2 (int): user node IDs
        movies_df (pd.DataFrame): for looking up movieId → title

    Returns:
        None (prints the path and intermediate node count)
    """
    try:
        path = nx.shortest_path(graph, source=user1, target=user2)
    except nx.NetworkXNoPath:
        print(f"No path between user {user1} and user {user2}")
        return
    except nx.NodeNotFound as e:
        print(str(e))
        return

    readable_path = []
    for node in path:
        node_type = graph.nodes[node].get("bipartite")
        if node_type == "user":
            readable_path.append(f"User {node}")
        elif node_type == "movie":
            title = movies_df.loc[movies_df["movieId"] == node, "title"]
            movie_title = title.values[0] if not title.empty else f"Movie {node}"
            readable_path.append(f"Movie: {movie_title}")
        else:
            readable_path.append(str(node))

    print(" → ".join(readable_path))
    print(f"Intermediate nodes: {len(path)}")



def find_most_connected_movies(graph, movies_df, top_n=10):
    """
    find and print top N movies with highest degree centrality in a bipartite user-movie graph

    Parameters:
        graph (nx.Graph)
        movies_df (pd.DataFrame): for mapping movieId → title
        top_n (int): number of top movies to show

    Returns:
        None (prints top N movie titles with degree)
    """
    movie_nodes = [n for n, d in graph.nodes(data=True) if d.get("bipartite") == "movie"]

    movie_degrees = [(m, graph.degree(m)) for m in movie_nodes]
    movie_degrees.sort(key=lambda x: x[1], reverse=True)

    print(f"Top {top_n} most connected movies:")
    for i, (movie_id, degree) in enumerate(movie_degrees[:top_n], start=1):
        title = movies_df.loc[movies_df["movieId"] == movie_id, "title"]
        movie_title = title.values[0] if not title.empty else f"Movie {movie_id}"
        print(f"{i}. {movie_title} - degree: {degree}")



def recommend_similar_users(graph, user_id, top_n=5):
    """
    recommend other users with most similar movie-watching history using Jaccard similarity

    Parameters:
        graph (nx.Graph): bipartite user-movie graph
        user_id (int): user node
        top_n (int): number of similar users to recommend

    Returns:
        list of (user_id, similarity) tuples
    """
    if user_id not in graph:
        print(f"User {user_id} not found in graph.")
        return []

    user_movies = set(graph.neighbors(user_id))
    if not user_movies:
        print(f"User {user_id} has no rated movies.")
        return []

    similarities = []

    for other in graph.nodes:
        if other == user_id:
            continue
        if graph.nodes[other].get("bipartite") != "user":
            continue

        other_movies = set(graph.neighbors(other))
        intersection = user_movies & other_movies
        union = user_movies | other_movies

        if not union:
            continue

        jaccard = len(intersection) / len(union)
        if jaccard > 0:
            similarities.append((other, jaccard))

    similarities.sort(key=lambda x: x[1], reverse=True)
    print(f"Top {top_n} users similar to User {user_id}:")
    for rank, (uid, score) in enumerate(similarities[:top_n], start=1):
        print(f"{rank}. User {uid} (similarity: {score:.3f})")

    return similarities[:top_n]