from datetime import date

from streaming.tracks import (
    Track,
    Song,
    SingleRelease,
    AlbumTrack,
    Podcast,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.artists import Artist


class TestTracks:
    def test_duration_minutes(self) -> None:
        track = Track("t1", "Base", 90, "pop")
        assert track.duration_minutes() == 1.5

    def test_equality_same_id(self) -> None:
        t1 = Track("t1", "A", 60, "pop")
        t2 = Track("t1", "B", 120, "rock")
        assert t1 == t2

    def test_equality_different_id(self) -> None:
        t1 = Track("t1", "A", 60, "pop")
        t2 = Track("t2", "A", 60, "pop")
        assert t1 != t2

    def test_equality_non_track(self) -> None:
        t1 = Track("t1", "A", 60, "pop")
        assert (t1 == object()) is False

    def test_song_stores_artist(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        song = Song("t1", "Song", 120, "pop", artist)
        assert song.artist is artist

    def test_single_release_has_release_date(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        release_date = date(2024, 1, 1)
        single = SingleRelease("t1", "Single", 120, "pop", artist, release_date=release_date)
        assert single.release_date == release_date

    def test_album_track_album_starts_none(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        track = AlbumTrack("t1", "Track", 120, "pop", artist, track_number=1)
        assert track.album is None

    def test_album_track_track_number(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        track = AlbumTrack("t1", "Track", 120, "pop", artist, track_number=7)
        assert track.track_number == 7

    def test_podcast_defaults(self) -> None:
        pod = Podcast("p1", "Pod", 1800, "podcast", host="Host")
        assert pod.host == "Host"
        assert pod.description == ""

    def test_interview_episode_guest(self) -> None:
        episode = InterviewEpisode("p1", "Ep", 1800, "podcast", host="H", guest="G")
        assert episode.guest == "G"

    def test_narrative_episode_details(self) -> None:
        episode = NarrativeEpisode("p1", "Ep", 1800, "podcast", host="H", season=2, episode_number=4)
        assert episode.season == 2
        assert episode.episode_number == 4

    def test_audiobook_track_details(self) -> None:
        audio = AudiobookTrack("a1", "Chapter", 600, "audio", author="Auth", narrator="Narr")
        assert audio.author == "Auth"
        assert audio.narrator == "Narr"

    def test_song_is_track(self) -> None:
        artist = Artist("a1", "Artist", genre="pop")
        song = Song("t1", "Song", 120, "pop", artist)
        assert isinstance(song, Track)

    def test_podcast_is_track(self) -> None:
        pod = Podcast("p1", "Pod", 1800, "podcast", host="Host")
        assert isinstance(pod, Track)
