import contextlib
import io
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import cycle

# 07:00 America/New_York maps to a different UTC hour depending on DST, so the
# workflow registers two Sunday cron entries and this gate lets exactly one of
# them through based on the current Eastern offset. Keep these in sync with the
# `on.schedule` block of the workflows.
EDT_CRON = "0 11 * * 0"  # 11:00 UTC == 07:00 EDT (summer)
EST_CRON = "0 12 * * 0"  # 12:00 UTC == 07:00 EST (winter)


def _parse_cycle_date(value):
    # get_version_start() returns YYYY-MM-DD in most repos and MM-DD-YYYY in
    # others, so accept either.
    for fmt in ("%Y-%m-%d", "%m-%d-%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unrecognised cycle date format: {value!r}")


def should_run():
    event = os.environ.get("EVENT", "")
    force = os.environ.get("FORCE", "").lower() == "true"
    schedule = os.environ.get("SCHEDULE", "")

    now_et = datetime.now(ZoneInfo("America/New_York"))

    # The next Thursday is the FAA cycle changeover day. We only build during the
    # week that leads into a changeover. (weekday: Mon=0 ... Thu=3 ... Sun=6)
    days_to_thursday = (3 - now_et.weekday()) % 7
    coming_thursday = now_et.date() + timedelta(days=days_to_thursday)

    # The upcoming cycle that will be written to the manifest. If its effective
    # date equals the Thursday at the end of this week then this is the release
    # week and FAA data is already published.
    with contextlib.redirect_stdout(io.StringIO()):
        next_cycle = cycle.get_cycle()
    next_cycle_start = _parse_cycle_date(cycle.get_version_start(next_cycle))
    release_week = next_cycle_start == coming_thursday

    # Pick the cron that corresponds to the current DST state. Comparing against
    # the triggering cron (rather than the observed clock hour) keeps "exactly
    # once" behaviour even if GitHub delays the scheduled run by an hour or more.
    expected_cron = EDT_CRON if now_et.utcoffset() == timedelta(hours=-4) else EST_CRON

    print(
        f"event={event} now_et={now_et.isoformat()} "
        f"coming_thursday={coming_thursday.isoformat()} "
        f"next_cycle={next_cycle} next_cycle_start={next_cycle_start.isoformat()} "
        f"release_week={release_week} schedule={schedule!r} "
        f"expected_cron={expected_cron!r} force={force}",
        file=sys.stderr,
    )

    if force:
        return True
    if event == "schedule":
        return release_week and schedule == expected_cron
    # Manual dispatch without force still respects the release-week gate but
    # ignores the time-of-day check (you can run it any time that week).
    return release_week


if __name__ == "__main__":
    print("run=true" if should_run() else "run=false")
