from datetime import datetime, timedelta


class ActivitySummary:
    def __init__(self, name: str, duration: timedelta):
        self.name = name
        self.duration = duration


class Dao:
    def __init__(self):
        pass

    def get_last_log(self) -> datetime:
        pass

    def get_act_today(self, activity: str) -> ActivitySummary:
        pass

    def update_act_duration_today(self, activity: str, new_dur: timedelta):
        pass

    def create_act_today(self, activity: str, dur: timedelta):
        pass

    def set_last_log(self, when: datetime):
        pass
