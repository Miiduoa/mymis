from collections import defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def _parse_timestamp(value, reporting_zone):
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("event timestamp must include timezone")
    return dt.astimezone(reporting_zone)


def _week_start(dt):
    day = dt.date()
    return day - timedelta(days=day.weekday())


def weekly_retention(
    events,
    signup_event="signup",
    activity_events=None,
    max_week=4,
    reporting_timezone="UTC",
):
    if max_week < 0:
        raise ValueError("max_week cannot be negative")

    reporting_zone = ZoneInfo(reporting_timezone)
    parsed = []
    for row in events:
        user_id = row.get("user_id")
        name = row.get("event_name")
        timestamp = row.get("timestamp")
        if not user_id or not name or not timestamp:
            raise ValueError("events require user_id, event_name and timestamp")
        parsed.append((str(user_id), str(name), _parse_timestamp(timestamp, reporting_zone)))

    first_signup = {}
    for user_id, name, ts in parsed:
        if name == signup_event and (user_id not in first_signup or ts < first_signup[user_id]):
            first_signup[user_id] = ts

    active_filter = None if activity_events is None else set(activity_events)
    cohort_users = defaultdict(set)
    active = defaultdict(set)

    for user_id, signup_ts in first_signup.items():
        cohort_users[_week_start(signup_ts)].add(user_id)

    for user_id, name, ts in parsed:
        signup_ts = first_signup.get(user_id)
        if signup_ts is None or ts < signup_ts:
            continue
        if active_filter is not None and name not in active_filter and name != signup_event:
            continue

        cohort = _week_start(signup_ts)
        event_week = _week_start(ts)
        week_index = (event_week - cohort).days // 7
        if 0 <= week_index <= max_week:
            active[(cohort, week_index)].add(user_id)

    rows = []
    for cohort in sorted(cohort_users):
        cohort_size = len(cohort_users[cohort])
        for week in range(max_week + 1):
            users = len(active[(cohort, week)])
            rows.append({
                "cohort": cohort.isoformat(),
                "week": week,
                "users": users,
                "cohort_size": cohort_size,
                "retention": users / cohort_size if cohort_size else 0,
            })
    return rows
