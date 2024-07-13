from datetime import datetime, timedelta, timezone


# returns (cycle 28, cycle 56)
# use 1 as future to get future cycle, and -1 for past, can be any number +-n
def calculate_cycle(future=0):

    # starting conditions from a known date
    start_utc = datetime(2020, 1, 2, 9, 0, 0, 0, timezone.utc)
    cycle = 1
    last_year = 2019
    combined = 2001
    is56 = True

    # all in UTC and current date, use future to current time
    now_utc = datetime.now(timezone.utc) + future * timedelta(28)

    # find all cycles through a loop
    while start_utc < now_utc:
        if last_year != start_utc.year:
            cycle = 1
            last_year = start_utc.year
        else:
            cycle = cycle + 1

        combined = (start_utc.year % 2000) * 100 + cycle
        is56 = not is56

        start_utc = start_utc + timedelta(days=28)

    if is56:
        return combined, combined
    else:
        # this is not 56, last must be, get it. should not recurse
        x, y = calculate_cycle(future - 1)
        return combined, x


def get_cycle():
    te, fs = calculate_cycle(1)
    print("Cycle to be put in manifest is " + str(te))
    return str(te)


def get_cycle_download():
    te, fs = calculate_cycle(1)
    print("Cycle to be downloaded is " + str(fs))
    return str(fs)


def get_first_date(year):
    # Date for first cycle every year in January starting 2014
    first_dates = {
        2020: 2,
        2021: 28,
        2022: 27,
        2023: 26,
        2024: 25,
        2025: 23,
        2026: 22,
        2027: 21,
        2028: 20,
        2029: 18
    }
    return first_dates.get(year, 0)


def get_version_start(cycle_name):
    try:
        cycle = int(cycle_name)
    except ValueError:
        return ""

    cycle_upper = cycle // 100
    cycle_lower = cycle - (cycle_upper * 100)
    first_date = get_first_date(2000 + cycle_upper)
    if first_date < 1:
        return ""

    epoch = datetime(2000 + cycle_upper, 1, first_date, 9, 0, 0)
    epoch += timedelta(days=28 * (cycle_lower - 1))
    fmt1 = epoch.strftime("%m-%d-%Y")
    return f"{fmt1}"
