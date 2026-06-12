import requests
import random
import json
import unicodedata
import re
import string

def get_prepared_words(num_words):
    search_terms = [
        "define",
        "explain",
        "example of",
        "how to pronounce",
        "what is",
        "meaning of",
        "synonym for",
        "antonym of",
        "use of",
        "origin of",
        "interesting facts about the",
        "history of",
        "etymology of",
        "definition of"
    ]

    # Fallback words in case the API is unavailable or returns invalid JSON
    fallback_words = [
        "technology", "music", "travel", "health", "finance", "science", "history",
        "art", "education", "sports", "nature", "culture", "food", "weather",
        "computer", "internet", "language", "mathematics", "physics", "chemistry",
        "biology", "geography", "philosophy", "psychology", "economics", "literature",
        "astronomy", "engineering", "architecture", "photography", "cinema", "theater",
        "poetry", "mythology", "anthropology", "sociology", "politics", "law",
        "environment", "ecology", "ocean", "mountain", "forest", "desert",
        "river", "island", "volcano", "planet", "galaxy"
    ]

    # Sanitize requested number of words
    try:
        requested_words = int(num_words)
        if requested_words <= 0:
            requested_words = 30
    except (TypeError, ValueError):
        requested_words = 30

    api_url = f"https://random-word-api.herokuapp.com/word?number={requested_words}"

    words_list = None
    try:
        response = requests.get(api_url, timeout=8)
        response.raise_for_status()
        # Try safe JSON parsing; response.json() can be used directly
        words = response.json()
        if isinstance(words, list) and all(isinstance(w, str) for w in words):
            words_list = words
        else:
            # Unexpected shape
            words_list = None
    except Exception:
        # Primary API failed; try secondary API before local fallback
        words_list = None

    # Secondary fallback API (extract 'word' field from objects), request exact count via query param
    if not words_list:
        try:
            secondary_api_url = f"https://random-words-api.kushcreates.com/api?language=en&words={requested_words}"
            resp = requests.get(secondary_api_url, timeout=8)
            resp.raise_for_status()
            data = resp.json()

            candidate_words = []
            if isinstance(data, list):
                # Expecting list of objects with a 'word' key
                for item in data:
                    if isinstance(item, dict):
                        w = item.get("word")
                        if isinstance(w, str) and w:
                            candidate_words.append(w)

            # If we collected candidates, sample/choose to the requested size
            if candidate_words:
                if len(candidate_words) >= requested_words:
                    words_list = random.sample(candidate_words, k=requested_words)
                else:
                    # Not enough unique words; allow repeats
                    words_list = [random.choice(candidate_words) for _ in range(requested_words)]
                print(f"[words_module] Using secondary word API: random-words-api.kushcreates.com ({len(candidate_words)} candidates)")
        except Exception:
            words_list = None

    if not words_list:
        # Build a list to the requested size using fallback words (with replacement)
        words_list = [random.choice(fallback_words) for _ in range(requested_words)]
        print("[words_module] Using local fallback word list")

    def sanitize_for_selenium(text):
        # Normalize and strip diacritics, then remove non-ASCII and unwanted characters
        normalized = unicodedata.normalize('NFKD', str(text))
        ascii_text = normalized.encode('ascii', 'ignore').decode('ascii', 'ignore')
        allowed_chars = set(string.ascii_letters + string.digits + " -_'\"/&()[],:;.!?")
        cleaned = ''.join(ch if ch in allowed_chars else ' ' for ch in ascii_text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    prepared_list = []
    for word in words_list:
        term = random.choice(search_terms)
        safe_word = sanitize_for_selenium(word)
        if not safe_word:
            # Replace with a safe placeholder if sanitization removes everything
            safe_word = "information"
        phrase = f"{term} {safe_word}"
        prepared_list.append(phrase)
    return prepared_list