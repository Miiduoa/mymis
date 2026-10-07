from src.mymis import (
    check_guardrails,
    compare_binary,
    experiment_decision,
    minimum_detectable_lift,
    sample_ratio_mismatch,
    summarize_funnel,
    weekly_retention,
)

primary = compare_binary(1000, 10000, 1120, 10000)
srm = sample_ratio_mismatch(10000, 10000)
guardrails = check_guardrails([
    {
        "name": "crash_free",
        "control": 0.995,
        "variant": 0.994,
        "mode": "min",
        "tolerance": 0.002,
    },
])

print("Experiment")
print(primary)
print("Approx. absolute MDE:", minimum_detectable_lift(0.10, 10000))
print("Decision:", experiment_decision(primary, srm, guardrails))

print("\nFunnel")
for row in summarize_funnel([
    ("visit", 12000),
    ("signup", 3200),
    ("activate", 2100),
    ("pay", 780),
]):
    print(row)

print("\nWeekly retention")
events = [
    {"user_id": "u1", "event_name": "signup", "timestamp": "2026-09-30T10:00:00+08:00"},
    {"user_id": "u1", "event_name": "open", "timestamp": "2026-10-07T10:00:00+08:00"},
    {"user_id": "u2", "event_name": "signup", "timestamp": "2026-10-01T11:00:00+08:00"},
    {"user_id": "u2", "event_name": "open", "timestamp": "2026-10-16T11:00:00+08:00"},
]
for row in weekly_retention(
    events,
    activity_events={"open"},
    max_week=2,
    reporting_timezone="Asia/Taipei",
):
    print(row)
