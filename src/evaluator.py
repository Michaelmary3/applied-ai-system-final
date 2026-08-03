from src.recommender import Recommender

def run_test_harness():
    print("=" * 60)
    print("RUNNING AUTOMATED AI SYSTEM RELIABILITY EVALUATOR")
    print("=" * 60)

    # In-memory test catalog so it never fails on missing CSV paths
    mock_songs = [
        {"id": 1, "title": "Blinding Lights", "artist": "The Weeknd", "genre": "pop", "mood": "happy", "energy": 0.8, "tempo_bpm": 171},
        {"id": 2, "title": "Coffee Shop Vibes", "artist": "Lofi Chill", "genre": "lofi", "mood": "chill", "energy": 0.2, "tempo_bpm": 80},
        {"id": 3, "title": "Back In Black", "artist": "AC/DC", "genre": "rock", "mood": "sad", "energy": 0.8, "tempo_bpm": 115}
    ]

    recommender = Recommender(mock_songs)

    test_cases = [
        {
            "name": "Standard Pop Preference",
            "input": {"genre": "pop", "mood": "happy", "energy": 0.8},
            "expected_top_genre": "pop",
            "min_score": 3.0
        },
        {
            "name": "Low Energy Lofi Preference",
            "input": {"genre": "lofi", "mood": "chill", "energy": 0.2},
            "expected_top_genre": "lofi",
            "min_score": 3.0
        },
        {
            "name": "Guardrail Test (Missing Key)",
            "input": {"genre": "rock", "mood": "sad"},
            "should_fail": True
        }
    ]

    passed = 0
    total = len(test_cases)

    for case in test_cases:
        print(f"\n[Test Case] {case['name']}")
        try:
            if case.get("should_fail"):
                try:
                    recommender.recommend(case['input'])
                    print("❌ FAIL: Guardrail failed to trigger on missing input.")
                except ValueError as e:
                    print(f"✅ PASS: Guardrail caught invalid input -> {e}")
                    passed += 1
            else:
                results = recommender.recommend(case['input'], k=1)
                top_song, score, explanation = results[0]
                if top_song['genre'].lower() == case['expected_top_genre'] and score >= case['min_score']:
                    print(f"✅ PASS: Top result '{top_song['title']}' (Score: {score}) matched criteria.")
                    passed += 1
                else:
                    print(f"❌ FAIL: Top result '{top_song['title']}' (Score: {score}) failed criteria.")
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"EVALUATION SUMMARY: {passed}/{total} Test Cases Passed ({round((passed/total)*100, 1)}%)")
    print("=" * 60)

if __name__ == "__main__":
    run_test_harness()