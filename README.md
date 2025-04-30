# SI507-movieLens-graph-project

This project analyzes and explores the MovieLens dataset using a bipartite graph between users and movies. It also integrates with the TMDb API to retrieve movie details.

## Features

- Recommend similar movies using genome tags and cosine similarity
- Find the shortest path between two users in the graph
- Show most connected (popular) movies by degree
- Recommend similar users based on Jaccard similarity
- Query detailed movie information from TMDb
- Optional graph caching to speed up repeated runs

## Files

- main.py — main entry point with interactive command-line interface
- movieLens.py — data loading and cleaning (including column name handling)
- bipartite_graph.py — construct bipartite user-movie graph
- query_tools.py — graph query functions (recommendation, path, centrality)
- tmdb_api.py — TMDb movie info retrieval via Bearer token
- graph_cache.py — optional graph caching utility
- ml-20m/ — Please download the MovieLens 20M dataset separately from [https://grouplens.org/datasets/movielens/20m/] and place it in a folder named ml-20m.

## Requirements

- pandas
- networkx
- requests
- IPython (optional, for poster display in Jupyter)

## How to Run

1. Make sure the MovieLens `ml-20m` dataset is placed in the correct folder.
2. Make sure your TMDb Bearer token is set correctly in `tmdb_api.py`.
3. Run the main program:  
   `python main.py`
4. Follow the prompts to explore recommendations and query movie or user information.

## Notes

- By default, the program loads filtered data (active users and popular movies only). You can choose to load the full dataset at startup.
- You can choose whether to use a cached graph (if available) or rebuild from data each time.
- Poster display is optional and only works in Jupyter environments.


## Author
Developed by Shanchen Liu for SI 507 final project.
