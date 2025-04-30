import networkx as nx

def build_user_movie_graph(ratings_df):
    """
    build a bipartite user-movie graph using ratings data

    Parameters:
        ratings_df (DataFrame): should contain userId, movieId, rating

    Returns:
        networkx.Graph: bipartite graph
    """
    B = nx.Graph()

    # Add user and movie nodes
    user_ids = ratings_df["userId"].unique()
    movie_ids = ratings_df["movieId"].unique()

    B.add_nodes_from(user_ids, bipartite="user")
    B.add_nodes_from(movie_ids, bipartite="movie")

    # Add edges: user → movie with rating as weight
    edges = [
        (row["userId"], row["movieId"], {"weight": row["rating"]})
        for _, row in ratings_df.iterrows()
    ]
    B.add_edges_from(edges)

    return B