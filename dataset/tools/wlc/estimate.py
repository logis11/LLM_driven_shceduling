"""Static demand estimate policy (task-2.3 spec §7).

The estimate itself is computed exactly during synthesis (compiler.py
accumulates each task's CPU demand in context); this module owns the
window policy: `-single` files must land in the measurable oversubscription
regime unless their timeline declares the calibration demand class.
The RQ0 admission test remains the real enforcement (building-plan §5a).
"""

LANE_WINDOW = (1.00, 1.50)


def demand_estimate(report):
    """Summarize a compile report into (utilization, in_window)."""
    low, high = LANE_WINDOW
    utilization = report["utilization"]
    return utilization, low <= utilization <= high


def check_window(report, mode):
    """Returns a violation string, or None if the file passes policy."""
    utilization, in_window = demand_estimate(report)
    if mode != "single" or report["demand_class"] == "calibration":
        return None
    if not in_window:
        low, high = LANE_WINDOW
        return (f"-single demand estimate {utilization:.2f} outside "
                f"[{low:.2f}, {high:.2f}] and demand class is not calibration")
    return None
