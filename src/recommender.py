from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv

@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float

@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float

class Recommender:
    """Agentic AI Recommender System with structured reasoning."""
    def __init__(self, songs: List[Dict]):
        self.songs = songs

    def score_song(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        # 1. Genre Weighting (Primary Feature)
        if song['genre'].lower() == user_prefs['genre'].lower():
            score += 2.0
            reasons.append("Genre match (+2.0)")

        # 2. Mood Weighting (Secondary Feature)
        if song['mood'].lower() == user_prefs['mood'].lower():
            score += 1.0
            reasons.append("Mood match (+1.0)")

        # 3. Energy Proximity (Numerical Feature)
        energy_diff = abs(song['energy'] - user_prefs['energy'])
        energy_score = max(0.0, 1.0 - energy_diff)
        score += energy_score
        reasons.append(f"Energy proximity (+{round(energy_score, 2)})")

        return round(score, 2), reasons

    def recommend(self, user_prefs: Dict, k: int = 3) -> List[Tuple[Dict, float, str]]:
        # Guardrail: Check for missing user input
        required_keys = ['genre', 'mood', 'energy']
        for key in required_keys:
            if key not in user_prefs:
                raise ValueError(f"Guardrail Triggered: Missing required key '{key}' in user preferences.")

        scored_songs = []
        for song in self.songs:
            score, reasons = self.score_song(user_prefs, song)
            explanation = ", ".join(reasons)
            scored_songs.append((song, score, explanation))

        # Sort by highest score first
        ranked_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
        return ranked_songs[:k]


def load_songs(csv_path: str) -> List[Dict]:
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = int(row['tempo_bpm'])
            songs.append(row)
    return songs