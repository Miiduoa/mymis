from src.mymis import compare_binary, sample_ratio_mismatch, summarize_funnel, validate_events

print("A/B result")
print(compare_binary(420, 5000, 468, 5020))

print("\nSRM check")
print(sample_ratio_mismatch(5000, 5020))

print("\nFunnel")
for row in summarize_funnel([
    ("visit", 12000),
    ("signup", 3200),
    ("activate", 2100),
    ("pay", 780),
]):
    print(row)

print("\nEvent contract")
print(validate_events([
    {"event_id":"e1","user_id":"u1","event_name":"visit","timestamp":"2026-10-01T10:00:00"},
    {"event_id":"e2","user_id":"u1","event_name":"signup","timestamp":"2026-10-01T10:02:00"},
]))
