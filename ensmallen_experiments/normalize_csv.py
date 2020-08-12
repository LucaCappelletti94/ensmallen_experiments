import gc
import os
import pandas as pd
from .utils import logger
from tqdm.auto import tqdm
from typing import TextIO


def parse_line(row: pd.Series, line: str, dst: TextIO, sep: str):
    values = line.strip().split(row.separator)

    dst_values = [
        values[row.subject_col].strip(),
        values[row.object_col].strip()
    ]

    if not pd.isna(row.weight_col):
        dst_values += [values[int(row.weight_col)].strip()]

    dst.write(sep.join(dst_values) + "\n")


def normalize_csv(row: pd.Series, src_file: str, dst_file: str, sep: str = "\t", garbage_collecting_interval: int = 100000):
    try:
        with open(src_file, "r") as src:
            with open(dst_file, "w") as dst:
                # Skip the first rows (THIS MUST SKIP THE HEADER TOO)
                for _ in range(row.rows_to_skip):
                    src.readline()

                # Write the header to the dst file
                columns = ["subject", "object"]

                if not pd.isna(row.weight_col):
                    columns += ["weight"]

                dst.write(sep.join(columns) + "\n")

                for number, line in tqdm(
                    enumerate(src),
                    desc="Copying the normalize file",
                    leave=False
                ):
                    if number % garbage_collecting_interval == 0:
                        gc.collect()
                    parse_line(row, line, dst, sep)

    except Exception as e:
        logger.error(
            "Error while normalizing file at path {}.".format(src_file)
        )
        if os.path.exists(dst_file):
            os.remove(dst_file)
        raise e
