"""
Online Leaderboard Module for Snake Game
Uses a simple JSON API backend for storing and retrieving scores.
"""

from __future__ import annotations

import json
import logging
import socket
import time
from typing import TypedDict
from urllib.parse import urljoin, urlparse

import requests

# Simple free JSON storage API (можно заменить на свой backend)
API_BASE_URL = "https://api.jsonbin.io/v3/b"
API_KEY = "$2a$10$YOUR_API_KEY_HERE"  # Замените на свой ключ от jsonbin.io
BIN_ID = "YOUR_BIN_ID"  # ID вашего bin после создания

# Fallback: используем локальное хранилище если API недоступен
LOCAL_LEADERBOARD_FILE = "leaderboard_local.json"

_SAFE_URL_SCHEMES = {"http", "https"}


class ScoreEntry(TypedDict):
    name: str
    score: int
    mode: str
    timestamp: float


def _ensure_safe_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in _SAFE_URL_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")
    return url


class LeaderboardManager:
    """Manager for online and offline leaderboard"""

    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.online = False
        self._check_connection()

    def _check_connection(self) -> bool:
        """Check if we have internet connection"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            self.online = True
            return True
        except (OSError, TimeoutError):
            self.online = False
            logging.warning("No internet connection, using local leaderboard")
            return False

    def submit_score(
        self,
        player_name: str,
        score: int,
        mode: str = "mvp"
    ) -> bool:
        """Submit a score to the leaderboard"""
        entry: ScoreEntry = {
            "name": player_name,
            "score": score,
            "mode": mode,
            "timestamp": time.time(),
        }

        if self.online:
            try:
                return self._submit_online(entry)
            except Exception as e:
                logging.error(f"Failed to submit score online: {e}")
                return self._submit_local(entry)
        return self._submit_local(entry)

    def _submit_online(self, entry: ScoreEntry) -> bool:
        """Submit score to online API"""
        try:
            # Get current leaderboard
            current_data = self.get_leaderboard()

            # Add new entry
            updated = list(current_data) if current_data else []
            updated.append(entry)

            # Sort by score (descending)
            updated.sort(key=lambda item: item["score"], reverse=True)

            # Keep only top 100
            trimmed = updated[:100]

            # Update online
            url = _ensure_safe_url(urljoin(f"{API_BASE_URL}/", BIN_ID))
            headers = {
                "Content-Type": "application/json",
                "X-Master-Key": API_KEY,
            }
            response = requests.put(
                url,
                data=json.dumps(trimmed, ensure_ascii=False),
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.status_code == 200

        except requests.RequestException as exc:
            logging.error("Online submit failed: %s", exc)
            raise
        except Exception as exc:  # noqa: BLE001 - bubble unexpected issues
            logging.error("Online submit failed: %s", exc)
            raise

    def _submit_local(self, entry: ScoreEntry) -> bool:
        """Submit score to local file"""
        try:
            # Load existing data
            try:
                with open(LOCAL_LEADERBOARD_FILE, encoding="utf-8") as src:
                    data: list[ScoreEntry] = json.load(src)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            # Add new entry
            data.append(entry)

            # Sort and keep top 100
            data.sort(key=lambda item: item["score"], reverse=True)
            trimmed = data[:100]

            # Save
            with open(LOCAL_LEADERBOARD_FILE, "w", encoding="utf-8") as dst:
                json.dump(trimmed, dst, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            logging.error(f"Local submit failed: {e}")
            return False

    def get_leaderboard(
        self,
        mode: str | None = None,
        limit: int = 10
    ) -> list[ScoreEntry]:
        """Get top scores from leaderboard"""
        if self.online:
            try:
                return self._get_online(mode, limit)
            except Exception as e:
                logging.error(f"Failed to get online leaderboard: {e}")
                return self._get_local(mode, limit)
        return self._get_local(mode, limit)

    def _get_online(
        self,
        mode: str | None,
        limit: int
    ) -> list[ScoreEntry]:
        """Get leaderboard from online API"""
        try:
            url = _ensure_safe_url(
                urljoin(f"{API_BASE_URL}/", f"{BIN_ID}/latest")
            )
            response = requests.get(
                url,
                headers={"X-Master-Key": API_KEY},
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = response.json()
            data: list[ScoreEntry] = result.get("record", [])

            # Filter by mode if specified
            if mode:
                data = [
                    entry for entry in data
                    if entry.get("mode") == mode
                ]

            return data[:limit]

        except requests.RequestException as exc:
            logging.error("Online get failed: %s", exc)
            raise
        except Exception as exc:  # noqa: BLE001
            logging.error("Online get failed: %s", exc)
            raise

    def _get_local(
        self,
        mode: str | None,
        limit: int
    ) -> list[ScoreEntry]:
        """Get leaderboard from local file"""
        try:
            with open(LOCAL_LEADERBOARD_FILE, encoding="utf-8") as src:
                data: list[ScoreEntry] = json.load(src)

            # Filter by mode if specified
            if mode:
                data = [
                    entry for entry in data
                    if entry.get("mode") == mode
                ]

            return data[:limit]

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_player_rank(self, player_name: str, mode: str) -> int | None:
        """Get player's rank in leaderboard (1-based)"""
        leaderboard = self.get_leaderboard(mode=mode, limit=100)
        for i, entry in enumerate(leaderboard, 1):
            if entry.get("name") == player_name:
                return i
        return None


# Global instance
leaderboard = LeaderboardManager()
