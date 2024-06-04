To create a new release, change the FAA cycles on top of cycle.py:


def get_cycle():

    return "2405" --> This is the current cycle


def get_cycle_download():

    return "2405" --> This is the cycle FAA advertizes on the download page (there are two at a time during switchover)

    

Then create a PR on cycle.py. The builds will start for all charts.
