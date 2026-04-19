from streaming.artists import Artist
from streaming.tracks import Track


class TestArtists:
    def test_artist_fields(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        assert artist.artist_id == "a1"
        assert artist.name == "Artist"
        assert artist.genre == "pop"

    def test_track_count_starts_zero(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        assert artist.track_count() == 0

    def test_add_track_increments_count(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        track = Track("t1", "Song", 120, "pop")
        artist.add_track(track)
        assert artist.track_count() == 1

    def test_add_multiple_tracks(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        track1 = Track("t1", "Song 1", 120, "pop")
        track2 = Track("t2", "Song 2", 150, "pop")
        artist.add_track(track1)
        artist.add_track(track2)
        assert artist.track_count() == 2

    def test_tracks_list_contains_track(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        track = Track("t1", "Song", 120, "pop")
        artist.add_track(track)
        assert track in artist.tracks

    def test_add_same_track_only_once(self):
        artist = Artist("a1", "Artist", genre="pop")
        track = Track("t1", "Song", 120, "pop")
        artist.add_track(track)
        artist.add_track(track)
        assert artist.track_count() == 1