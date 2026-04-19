"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
class Album:
    def __init__(self, album_id: str, title: str, artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track) -> None:
        if track not in self.tracks:
            track.album = self
            self.tracks.append(track)
            self.tracks.sort(key=lambda item: item.track_number)

    def track_ids(self) -> set[str]:
        return {track.track_id for track in self.tracks}

    def duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)