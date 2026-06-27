import io
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_URL = "https://hacker-news.firebaseio.com/v0"


# --- HackerNews API ---

def get_item(item_id: int) -> dict:
    url = f"{BASE_URL}/item/{item_id}.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_top_story_ids(limit: int = 10) -> list[int]:
    url = f"{BASE_URL}/topstories.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()[:limit]


def get_new_story_ids(limit: int = 10) -> list[int]:
    url = f"{BASE_URL}/newstories.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()[:limit]


def get_best_story_ids(limit: int = 10) -> list[int]:
    url = f"{BASE_URL}/beststories.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()[:limit]


def get_ask_story_ids(limit: int = 10) -> list[int]:
    url = f"{BASE_URL}/askstories.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()[:limit]


def get_show_story_ids(limit: int = 10) -> list[int]:
    url = f"{BASE_URL}/showstories.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()[:limit]


def get_job_story_ids(limit: int = 10) -> list[int]:
    url = f"{BASE_URL}/jobstories.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()[:limit]


def get_user(user_id: str) -> dict:
    url = f"{BASE_URL}/user/{user_id}.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_max_item_id() -> int:
    url = f"{BASE_URL}/maxitem.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_updates() -> dict:
    url = f"{BASE_URL}/updates.json"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


# --- Claude analysis (see analyze.py for the AI logic) ---

def analyze_top_stories(limit: int = 10) -> None:
    from analyze import extract_story, StoryAnalysis

    ids = get_top_story_ids(limit)
    for i, story_id in enumerate(ids, 1):
        item = get_item(story_id)
        title = item.get("title", "(no title)")
        url = item.get("url", "")
        result = extract_story(title, url)
        if isinstance(result, StoryAnalysis):
            print(result.format(i, title))
        else:
            print(f'[{i}] "{title}"\n    → {result}')
        print()


if __name__ == "__main__":
    analyze_top_stories()
