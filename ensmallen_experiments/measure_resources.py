import multiprocessing as mp
from time import sleep, perf_counter


def get_used_ram():
    with open("/proc/meminfo") as f:
        txt = f.read()

    # These values are in kB
    # E.g
    # MemTotal:       32498812 kB
    # MemFree:        27522840 kB
    # MemAvailable:   28616336 kB
    # Buffers:          241344 kB
    # Cached:          1976624 kB
    data = {
        k: int(v.split(" ")[-2])
        for (k, v) in zip(["total", "free", "available", "buffers", "cached"], txt.split("\n"))
    }

    return (data["total"] - data["free"] - data["buffers"] - data["cached"]) / (1024**2)


def resources_logger(stop, path, refresh_delay=0.1):
    with open(path, "w") as f:
        f.write("ram_used,timestamp\n")
        while not stop.is_set():
            ram_used = get_used_ram()
            # TODO: set an initial time and write out deltas
            timestamp = perf_counter()
            f.write("{},{}\n".format(ram_used, timestamp))
            sleep(refresh_delay)

        ram_used = get_used_ram()
        timestamp = perf_counter()
        f.write("{},{}\n".format(ram_used, timestamp))


class MeasureResources(object):
    def __init__(self, file_name):
        self.stop = mp.Event()
        self.process = mp.Process(
            target=resources_logger, args=(self.stop, file_name))

    def __enter__(self):
        self.process.start()

    def __exit__(self, type, value, traceback):
        self.stop.set()
        self.process.join()
