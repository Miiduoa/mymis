def validate_events(events, required=("event_id", "user_id", "event_name", "timestamp")):
    errors = []
    seen = set()
    for i, row in enumerate(events, start=1):
        missing = [key for key in required if row.get(key) in (None, "")]
        if missing:
            errors.append(f"row {i}: missing {missing}")
        event_id = row.get("event_id")
        if event_id in seen:
            errors.append(f"row {i}: duplicate event_id {event_id}")
        seen.add(event_id)
    return errors
