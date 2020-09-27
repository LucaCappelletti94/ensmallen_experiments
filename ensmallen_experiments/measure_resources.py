import os
import gc
import pandas as pd
import numpy as np
import multiprocessing as mp
from time import sleep, perf_counter
from typing import List, Tuple


def get_used_ram():
    """Return the ammout of ram used **BY THE SYSTEM**.

    The values are read from /proc/meminfo (LINUX ONLY) to be as close as precise
    as possible. Moreover, the ram used is computed by:

    MemTotal - MemFree - Buffers - Cached - Slab

    Where:
        - MemTotal is the total ammount of ram connected to the motherboard.
        - MemFree is the total ammout of ram free.
        - Buffers is the ammount of ram used for I/O buffers such as disks and
            sockets (This is supposed to be < 20Mb).
        - Cached is the total ammount of ram used for caching. This is used to 
            save the dirty pages of memory before they are synced with the disk
            and for the ramdisks.
        - Slab is the total ammount of ram used by the kernel.
    More infos at https://man7.org/linux/man-pages/man5/proc.5.html

    All of this is done to try to remove as much as possibles any system bias.
    """
    # Read the memory statistics
    with open("/proc/meminfo") as f:
        txt = f.read()

    # Convert the file into a dictionary with all the metrics
    data = {
        k: int(v.strip()[:-2])
        if v.lower().endswith("b")
        else int(v.strip())
        for (k, v) in [
            x.split(":")
            for x in txt.split("\n")
            if x.strip() != ""
        ]
    }
    # Total ram - Free Ram - Disks and sockets buffers - cache - kernel used memory
    return (data["MemTotal"] - data["MemFree"] - data["Buffers"] - data["Cached"] - data["Slab"]) / (1024**2)


def resources_logger(stop: mp.Event, queue: mp.Queue, metadata: dict, refresh_delay: float, calibration_offset: int = 0):
    """Worker that logs memory usage in a csv file until the stop event is set.

    Parameters
    ----------
        stop: mp.Event,
            The stop signal that must be set to stop the ram logging.
        path: str,
            The path of the csv where to log the data.
        refresh_delay: float,
            How many seconds to sleep between every read.
        calibration_offset: int = 0,
            The optional system offsets to remove from the data that will be logged.
    """
    start = perf_counter()
    while not stop.is_set():
        queue.put({
            "delta": perf_counter() - start,
            "ram": get_used_ram() - calibration_offset,
            **metadata
        })
        sleep(refresh_delay)
    queue.put({
        "delta": perf_counter() - start,
        "ram": get_used_ram() - calibration_offset,
        **metadata
    })


class MeasureResources(object):
    def __init__(self, refresh_delay: float = 0.1, end_delay: float = 4, calibrate: bool = True, calibration_seconds: float = 2, verbose=True):
        """Context manager that measure the time and ram a snipped of code use.

        Parameters
        ----------
            refresh_delay: float = 0.1,
                How much time (in seconds) to wait between measurements of ram.
            end_delay: float = 4,
                How much time the context manager will wait before exiting once
                the snipped has ended. This is used to measure the final ammount
                of ram used.
            calibrate: bool = True,
                If the context manager should do a calibration measurement before
                starting the code.
            calibration_seconds: float = 2,
                How much time, in seconds, the calibration step will take.
            verbose: bool = True,
                If the program should be verbose and print info or not.
        """
        self.refresh_delay = refresh_delay
        self.end_delay = end_delay
        self.calibrate = calibrate
        self.calibration_seconds = calibration_seconds
        self.verbose = verbose

        self.stop = mp.Event()
        self.results_queue = mp.Queue()

    def get_results(self) -> pd.DataFrame:
        """Return a dataframe with all the data obtained from all the trackings."""
        values = []
        while not self.results_queue.empty():
            values.append(self.results_queue.get())
        return pd.DataFrame(values)

    def __call__(self, **metadata):
        return Tracker(
            self.results_queue,
            self.stop,
            metadata,
            self.refresh_delay,
            self.end_delay,
            self.calibrate,
            self.calibration_seconds,
            self.verbose
        )


class Tracker(object):
    def __init__(self,
                 results_queue: mp.Queue,
                 stop: mp.Event,
                 metadata: dict,
                 refresh_delay: float = 0.1,
                 end_delay: float = 4,
                 calibrate: bool = True,
                 calibration_seconds: float = 2,
                 verbose: bool = True
                 ):
        """Context manager that measure the time and ram a snipped of code use.

        Parameters
        ----------
            file_name: str,
                The csv file where the ram measurements will be logged.
            refresh_delay: float = 0.1,
                How much time (in seconds) to wait between measurements of ram.
            end_delay: float = 4,
                How much time the context manager will wait before exiting once
                the snipped has ended. This is used to measure the final ammount
                of ram used.
            calibrate: bool = True,
                If the context manager should do a calibration measurement before
                starting the code.
            calibration_seconds: float = 2,
                How much time, in seconds, the calibration step will take.
            verbose: bool = True,
                If the program should be verbose and print info or not.
        """
        self.refresh_delay = refresh_delay
        self.end_delay = end_delay
        self.verbose = verbose
        self.stop = mp.Event()

        gc.collect()
        if calibrate:
            self.calibration_offset = self._calibrate(calibration_seconds)
        else:
            self.calibration_offset = 0

        self.process = mp.Process(target=resources_logger, args=[
                                  self.stop, results_queue, metadata, refresh_delay, self.calibration_offset])

    def _measure_ram(self, number_of_seconds: float) -> List[int]:
        """Returns a list of measurements

        Parameters
        ----------
            number_of_seconds: float,
                For how many seconds the function will measure the ram used
        """
        measurements = []
        start = perf_counter()
        while (perf_counter() - start) < number_of_seconds:
            measurements.append(get_used_ram())
            sleep(self.refresh_delay)
        return measurements

    def _measure_mean_ram_usage(self, number_of_seconds: float) -> Tuple[float, float]:
        """Return the mean ram used in an interval of time.

        Parameters
        ----------
            number_of_seconds: float,
                For how many seconds the function will measure the ram used
        """
        measurements = self._measure_ram(number_of_seconds)
        return np.mean(measurements), np.std(measurements)

    def _calibrate(self, calibration_seconds: float) -> float:
        """Before letting python continue we take a couple of seconds to measure
            the ram in use before the program enters this context manager.

            This is used to get better measurements.

        Parameters
        ----------
            number_of_seconds: float,
                For how many seconds the function will measure the ram used
        """
        if self.verbose:
            print("Starting calibration")
        calibration_offset, calibration_std = self._measure_mean_ram_usage(
            calibration_seconds)
        if self.verbose:
            print("Calibration done, the mean ram used by the system is {} ± {} Gb ".format(
                calibration_offset, calibration_std))
        return calibration_offset

    def __enter__(self):
        gc.collect()
        self.stop.clear()
        self.process.start()
        self.start_time = perf_counter()

    def __exit__(self, type, value, traceback):
        self.end_time = perf_counter()
        self.stop.set()
        self.process.join()
        self.process.close()
        end_ram, end_std = self._measure_mean_ram_usage(self.end_delay)
        if self.verbose:
            print("The ram used one che process finished is {} ± {} Gb".format(
                end_ram - self.calibration_offset, end_std))
            print("The process took {} seconds".format(
                self.end_time - self.start_time))
        gc.collect()