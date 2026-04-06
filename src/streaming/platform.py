from collections import defaultdict
from datetime import timedelta

from .tracks import Song
from .users import PremiumUser, FamilyMember
from .playlists import Playlist, CollaborativePlaylist


class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self.tracks = []
        self.users = []
        self.artists = []
        self.albums = []
        self.playlists = []
        self.sessions = []

        self.track_by_id = {}
        self.user_by_id = {}
        self.artist_by_id = {}
        self.album_by_id = {}

    # Registration methods
    def add_track(self, track) -> None:
        self.tracks.append(track)
        self.track_by_id[track.track_id] = track

    def add_user(self, user) -> None:
        self.users.append(user)
        self.user_by_id[user.user_id] = user

    def add_artist(self, artist) -> None:
        self.artists.append(artist)
        self.artist_by_id[artist.artist_id] = artist

    def add_album(self, album) -> None:
        self.albums.append(album)
        self.album_by_id[album.album_id] = album

    def add_playlist(self, playlist) -> None:
        self.playlists.append(playlist)

    def record_session(self, session) -> None:
        self.sessions.append(session)

    # Accessors
    def get_track(self, track_id: str):
        return self.track_by_id.get(track_id)

    def get_user(self, user_id: str):
        return self.user_by_id.get(user_id)

    def get_artist(self, artist_id: str):
        return self.artist_by_id.get(artist_id)

    def get_album(self, album_id: str):
        return self.album_by_id.get(album_id)

    def all_users(self):
        return list(self.users)

    def all_tracks(self):
        return list(self.tracks)

    # Q1
    def total_listening_time_minutes(self, start, end) -> float:
        total_seconds = 0

        for session in self.sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds

        return total_seconds / 60.0

    # Q2
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        premium_users = [user for user in self.users if isinstance(user, PremiumUser)]

        if len(premium_users) == 0:
            return 0.0

        if len(self.sessions) == 0:
            return 0.0

        latest_timestamp = max(session.timestamp for session in self.sessions)
        cutoff_date = latest_timestamp - timedelta(days=days)

        total_unique_tracks = 0

        for user in premium_users:
            unique_track_ids = set()

            for session in self.sessions:
                if session.user == user and session.timestamp >= cutoff_date:
                    unique_track_ids.add(session.track.track_id)

            total_unique_tracks += len(unique_track_ids)

        return total_unique_tracks / len(premium_users)

    # Q3
    def track_with_most_distinct_listeners(self):
        if len(self.sessions) == 0:
            return None

        listeners_by_track = defaultdict(set)

        for session in self.sessions:
            listeners_by_track[session.track.track_id].add(session.user.user_id)

        best_track = None
        highest_listener_count = 0

        for track in self.tracks:
            listener_count = len(listeners_by_track[track.track_id])

            if listener_count > highest_listener_count:
                highest_listener_count = listener_count
                best_track = track

        return best_track

    # Q4
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        durations = defaultdict(list)

        for session in self.sessions:
            user_type = type(session.user).__name__
            durations[user_type].append(session.duration_listened_seconds)

        result = []

        for user_type, values in durations.items():
            average = sum(values) / len(values)
            result.append((user_type, average))

        result.sort(key=lambda item: item[1], reverse=True)
        return result

    # Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total_seconds = 0

        for session in self.sessions:
            if isinstance(session.user, FamilyMember):
                if session.user.age < age_threshold:
                    total_seconds += session.duration_listened_seconds

        return total_seconds / 60.0

    # Q6
    def top_artists_by_listening_time(self, n: int = 5):
        totals = defaultdict(int)

        for session in self.sessions:
            if isinstance(session.track, Song):
                artist = session.track.artist
                totals[artist] += session.duration_listened_seconds

        ranked = []

        for artist, seconds in totals.items():
            ranked.append((artist, seconds / 60.0))

        ranked.sort(key=lambda item: item[1], reverse=True)

        return ranked[:n]

    # Q7
    def user_top_genre(self, user_id: str):
        user = self.get_user(user_id)

        if user is None:
            return None

        genre_totals = defaultdict(int)

        for session in self.sessions:
            if session.user == user:
                genre_totals[session.track.genre] += session.duration_listened_seconds

        if len(genre_totals) == 0:
            return None

        total_seconds = sum(genre_totals.values())

        top_genre = None
        top_seconds = 0

        for genre, seconds in genre_totals.items():
            if seconds > top_seconds:
                top_seconds = seconds
                top_genre = genre

        percentage = (top_seconds / total_seconds) * 100

        return top_genre, percentage

    # Q8
    def collaborative_playlists_with_many_artists(self, threshold: int = 3):
        result = []

        for playlist in self.playlists:
            if isinstance(playlist, CollaborativePlaylist):
                artist_ids = set()

                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artist_ids.add(track.artist.artist_id)

                if len(artist_ids) > threshold:
                    result.append(playlist)

        return result

    # Q9
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        standard_playlists = []
        collaborative_playlists = []

        for playlist in self.playlists:
            if type(playlist) is Playlist:
                standard_playlists.append(playlist)
            elif isinstance(playlist, CollaborativePlaylist):
                collaborative_playlists.append(playlist)

        if len(standard_playlists) > 0:
            avg_standard = sum(len(p.tracks) for p in standard_playlists) / len(standard_playlists)
        else:
            avg_standard = 0.0

        if len(collaborative_playlists) > 0:
            avg_collaborative = sum(len(p.tracks) for p in collaborative_playlists) / len(collaborative_playlists)
        else:
            avg_collaborative = 0.0

        return {
            "Playlist": avg_standard,
            "CollaborativePlaylist": avg_collaborative
        }

    # Q10
    def users_who_completed_albums(self):
        result = []

        for user in self.users:
            listened_track_ids = set()

            for session in self.sessions:
                if session.user == user:
                    listened_track_ids.add(session.track.track_id)

            completed_albums = []

            for album in self.albums:
                if len(album.tracks) == 0:
                    continue

                album_track_ids = {track.track_id for track in album.tracks}

                if album_track_ids.issubset(listened_track_ids):
                    completed_albums.append(album.title)

            if len(completed_albums) > 0:
                result.append((user, completed_albums))

        return result