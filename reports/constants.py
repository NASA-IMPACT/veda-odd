from datetime import date

# Manually maintained PI date ranges
# Update these when new PIs are planned
PI_DATES = {
    "pi-25.2": ("20250119", "20250418"),
    "pi-25.3": ("20250419", "20250718"),
    "pi-25.4": ("20250719", "20251018"),
    "pi-26.1": ("20251019", "20260117"),
    "pi-26.2": ("20260118", "20260425"),
    "pi-26.3": ("20260426", "20260711"),
}


def get_current_pi():
    """Find the current PI based on today's date."""
    today = date.today().strftime("%Y%m%d")
    for pi_name, (start, end) in PI_DATES.items():
        if start <= today <= end:
            return pi_name
    return None


def get_time_range(pi: str = None):
    """Get date range for a PI, or current PI if not specified."""
    if pi:
        return PI_DATES.get(pi)
    current = get_current_pi()
    if current:
        return PI_DATES[current]
    # Fallback to most recent PI if not in any range
    return list(PI_DATES.values())[-1]


TIME_RANGE = get_time_range()
