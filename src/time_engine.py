from datetime import datetime, timedelta

from dao import Dao

# Ask user what they're doing
# If answer:
#   - check last log time
#   - if today:
#     - calc diff
#     - check if act already logged today
#     - if so:
#       - extend time len in db
#     - else:
#       - create act, and add diff as init len
#   - else:
#     - insert act with len 5 mins
# Update last_log time
#

DEFAULT_ACTIVITY_START_DURATION = timedelta(minutes=5)


class TimeEngine:
    def __init__(self, dao: Dao):
        self._dao = dao

    def log_activity(self, log_activity: str, log_time=datetime.now()):
        last_log = self._dao.get_last_log()
        if last_log is None or last_log.date() < log_time.date():
            self._dao.create_act_today(log_activity, DEFAULT_ACTIVITY_START_DURATION)
        elif last_log > log_time:
            raise ValueError("Last log time is older than current activity log time.")
        elif last_log.date() == log_time.date():
            time_diff = log_time - last_log
            act_today = self._dao.get_act_today(log_activity)
            if act_today is not None:  # already logged today
                new_duration = act_today.duration + time_diff
                self._dao.update_act_duration_today(log_activity, new_duration)
            else:  # not logged today
                self._dao.create_act_today(log_activity, time_diff)
        else:
            raise RuntimeWarning("Programmer fucked up. This branch should be impossible to reach.")

        self._dao.set_last_log(log_time)
