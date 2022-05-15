import sqlite3
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


class SqliteDao(Dao):
    def __init__(self):
        super().__init__()
        self.db = sqlite3.connect('daagliks.db')
        curs = self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [x[0] for x in curs]
        if 'last_log' not in tables:  # assume fresh db
            self.db.execute("CREATE TABLE IF NOT EXISTS last_log (id INT PRIMARY KEY NOT NULL, ts INT8 NULLABLE)")
            self.db.execute("INSERT INTO last_log(id, ts) VALUES (1, NULL)")
            self.db.execute("CREATE TABLE IF NOT EXISTS activities (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                            "activity_name TEXT NOT NULL, date TEXT NOT NULL, duration_mins INT8 NOT NULL)")

    def get_last_log(self) -> datetime:
        curs = self.db.execute("SELECT ts FROM last_log where id=1")
        ts = curs.fetchone()[0]
        if ts is None:
            return None
        else:
            return datetime.utcfromtimestamp(ts)

    def close(self):
        self.db.close()
