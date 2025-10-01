"""
Online Leaderboard Module for Snake Game
Uses a simple JSON API backend for storing and retrieving scores
"""

import json
import logging
from typing import List, Dict, Optional
from urllib import request
import socket

# Simple free JSON storage API (можно заменить на свой backend)
API_BASE_URL = "https://api.jsonbin.io/v3/b"
API_KEY = "$2a$10$YOUR_API_KEY_HERE"  # Замените на свой ключ от jsonbin.io
BIN_ID = "YOUR_BIN_ID"  # ID вашего bin после создания

# Fallback: используем локальное хранилище если API недоступен
LOCAL_LEADERBOARD_FILE = "leaderboard_local.json"


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
        except (OSError, socket.timeout):
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
        entry = {
            "name": player_name,
            "score": score,
            "mode": mode,
            "timestamp": __import__('time').time()
        }

        if self.online:
            try:
                return self._submit_online(entry)
            except Exception as e:
                logging.error(f"Failed to submit score online: {e}")
                return self._submit_local(entry)
        else:
            return self._submit_local(entry)

    def _submit_online(self, entry: Dict) -> bool:
        """Submit score to online API"""
        try:
            # Get current leaderboard
            current_data = self.get_leaderboard()

            # Add new entry
            if not current_data:
                current_data = []
            current_data.append(entry)

            # Sort by score (descending)
            current_data.sort(key=lambda x: x['score'], reverse=True)

            # Keep only top 100
            current_data = current_data[:100]

            # Update online
            url = f"{API_BASE_URL}/{BIN_ID}"
            headers = {
                'Content-Type': 'application/json',
                'X-Master-Key': API_KEY
            }
            data = json.dumps(current_data).encode('utf-8')

            req = request.Request(
                url, data=data, headers=headers, method='PUT'
            )
            with request.urlopen(req, timeout=self.timeout) as response:
                return response.status == 200

        except Exception as e:
            logging.error(f"Online submit failed: {e}")
            raise

    def _submit_local(self, entry: Dict) -> bool:
        """Submit score to local file"""
        try:
            # Load existing data
            try:
                with open(LOCAL_LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            # Add new entry
            data.append(entry)

            # Sort and keep top 100
            data.sort(key=lambda x: x['score'], reverse=True)
            data = data[:100]

            # Save
            with open(LOCAL_LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            logging.error(f"Local submit failed: {e}")
            return False

    def get_leaderboard(
        self,
        mode: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Get top scores from leaderboard"""
        if self.online:
            try:
                return self._get_online(mode, limit)
            except Exception as e:
                logging.error(f"Failed to get online leaderboard: {e}")
                return self._get_local(mode, limit)
        else:
            return self._get_local(mode, limit)

    def _get_online(
        self,
        mode: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Get leaderboard from online API"""
        try:
            url = f"{API_BASE_URL}/{BIN_ID}/latest"
            headers = {'X-Master-Key': API_KEY}

            req = request.Request(url, headers=headers)
            with request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode('utf-8'))
                data = result.get('record', [])

                # Filter by mode if specified
                if mode:
                    data = [
                        entry for entry in data
                        if entry.get('mode') == mode
                    ]

                return data[:limit]

        except Exception as e:
            logging.error(f"Online get failed: {e}")
            raise

    def _get_local(
        self,
        mode: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Get leaderboard from local file"""
        try:
            with open(LOCAL_LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Filter by mode if specified
            if mode:
                data = [
                    entry for entry in data
                    if entry.get('mode') == mode
                ]

            return data[:limit]

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_player_rank(self, player_name: str, mode: str) -> Optional[int]:
        """Get player's rank in leaderboard (1-based)"""
        leaderboard = self.get_leaderboard(mode=mode, limit=100)
        for i, entry in enumerate(leaderboard, 1):
            if entry.get('name') == player_name:
                return i
        return None


# Global instance
leaderboard = LeaderboardManager()
