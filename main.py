import pandas as pd
from data_movieLens import load_data, load_filtered_data
from bipartite_graph import build_user_movie_graph
from query_tools import (
    find_similar_movies,
    shortest_path_between_users,
    find_most_connected_movies,
    recommend_similar_users
)
from tmdb_api import get_movie_info
from graph_cache import load_or_build_graph
import os

# for poster display in Jupyter
try:
    from IPython.display import Image, display
    JUPYTER_MODE = True
except ImportError:
    JUPYTER_MODE = False

def main():
    # ask whether to load the full dataset
    print("Load full dataset? This may take more memory and time. [y/N]: ", end="")
    use_full = input().strip().lower() == "y"

    # ask whether to use cached graph
    print("Use cached graph if available? [y/N]: ", end="")
    use_cache = input().strip().lower() == "y"

    # load data
    print("Loading MovieLens data...")
    if use_full:
        data = load_data()
    else:
        data = load_filtered_data()

    # build or load bipartite graph
    print("Preparing bipartite graph (user-movie)...")
    cache_file = "graph_full.pkl" if use_full else "graph_filtered.pkl"
    if use_cache and os.path.exists(cache_file):
        B = load_or_build_graph(data["ratings"], cache_path=cache_file)
    else:
        if use_cache:
            print(f"Cache file not found: {cache_file}. Building from scratch.")
        B = build_user_movie_graph(data["ratings"])
    print("Data and graph ready.\n")

    while True:
        # menu display
        print("\n===== MovieLens Graph Tool =====")
        print("1. Recommend similar movies")
        print("2. Find shortest path between users")
        print("3. Show most connected movies")
        print("4. Recommend similar users")
        print("5. Get movie info from TMDb")
        print("0. Exit")
        choice = input("Choose an option (0~5): ").strip()

        if choice == "1":
            title = input("Enter partial movie title: ").strip()
            restrict = input("Restrict to same genre? [y/n]: ").strip().lower() == "y"
            try:
                df = find_similar_movies(title, data["genome_scores"], data["movies"], restrict_genre=restrict)
                print("\nTop similar movies:")
                print(df.to_string(index=False))
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            try:
                u1 = int(input("Enter source user ID: "))
                u2 = int(input("Enter target user ID: "))
                shortest_path_between_users(B, u1, u2, data["movies"])
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "3":
            try:
                topn = int(input("How many top movies? "))
                find_most_connected_movies(B, data["movies"], top_n=topn)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            try:
                uid = int(input("Enter user ID: "))
                recommend_similar_users(B, uid)
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            title = input("Enter movie title to query TMDb: ").strip()
            try:
                info = get_movie_info(title, data["links"])
                print("\nMovie Info:")
                for k, v in info.items():
                    if k != "poster_url":
                        print(f"{k}: {v}")
                if info.get("poster_url") and JUPYTER_MODE:
                    display(Image(url=info["poster_url"]))
                elif info.get("poster_url"):
                    print(f"[Poster URL] {info['poster_url']}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "0":
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please enter a number from 0 to 5.")

if __name__ == "__main__":
    main()