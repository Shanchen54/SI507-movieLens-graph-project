import os
import pickle
from bipartite_graph import build_user_movie_graph

def load_or_build_graph(ratings_df, cache_path="graph_filtered.pkl"):
    """
    Load the bipartite graph from a local cache file if it exists.
    Otherwise, build the graph from ratings_df and save it to cache.

    Parameters:
        ratings_df (pd.DataFrame): the ratings used to build the graph
        cache_path (str): file path for caching the graph

    Returns:
        nx.Graph: the user-movie bipartite graph
    """
    if os.path.exists(cache_path):
        print(f"Loading graph from cache: {cache_path}")
        with open(cache_path, "rb") as f:
            return pickle.load(f)
    else:
        print("Building bipartite graph from scratch...")
        B = build_user_movie_graph(ratings_df)
        with open(cache_path, "wb") as f:
            pickle.dump(B, f)
        print(f"Graph cached to: {cache_path}")
        return B