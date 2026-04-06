from datetime import datetime

class ListeningSession:
    def __init__(self, session_id: str, user, track, timestamp: datetime, duration_listened_seconds: int):
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_listened_seconds

        if self.user is not None:
            self.user.add_session(self)

    def duration_listened_minutes(self) -> float:
        return self.duration_listened_seconds / 60.0