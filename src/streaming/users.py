class User:
    def __init__(self, user_id: str, name: str, age: int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session) -> None:
        if session not in self.sessions:
            self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        return sum(session.duration_listened_seconds for session in self.sessions)

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self) -> set[str]:
        return {session.track.track_id for session in self.sessions}


class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6

    def __init__(self, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age)


class PremiumUser(User):
    def __init__(self, user_id: str, name: str, age: int, subscription_start=None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(PremiumUser):
    def __init__(self, user_id: str, name: str, age: int, subscription_start=None):
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users = []

    def add_sub_user(self, user) -> None:
        if user not in self.sub_users:
            self.sub_users.append(user)

    def all_members(self) -> list:
        return [self] + self.sub_users


class FamilyMember(User):
    def __init__(self, user_id: str, name: str, age: int, parent):
        super().__init__(user_id, name, age)
        self.parent = parent
        if self.parent is not None:
            self.parent.add_sub_user(self)