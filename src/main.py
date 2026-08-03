from src.recommender import Recommender, load_songs
from src.evaluator import run_test_harness

def main():
    # 1. Load Data
    songs = load_songs("data/songs.csv")
    recommender = Recommender(songs)

    print("\n" + "="*50)
    print("      APPLIED AI MUSIC RECOMMENDER SYSTEM      ")
    print("="*50)

    # 2. Sample User Profiles
    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.2},
        "Deep Intense Rock": {"genre": "rock", "mood": "sad", "energy": 0.8}
    }

    # 3. Execution Run
    for name, user_prefs in profiles.items():
        print(f"\n--- Output for Profile: {name} ---")
        recs = recommender.recommend(user_prefs, k=3)
        for idx, (song, score, explanation) in enumerate(recs, 1):
            print(f"{idx}. {song['title']} (Score: {score})")
            print(f"   Reason: {explanation}")

    # 4. Run System Reliability Harness
    print("\n")
    run_test_harness()

if __name__ == "__main__":
    main()