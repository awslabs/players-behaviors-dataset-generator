# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from enum import Enum, auto

class WeekDay(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class PlayerEventType(Enum):
    BEGIN_SESSION = auto()
    END_SESSION = auto()
    BEGIN_STAGE = auto()
    END_STAGE = auto()

    @classmethod
    def names(cls):
        return list(map(lambda e: e.name, cls))

class PlayerEventField(Enum):
    id = auto()
    event_type = auto()
    timestamp = auto()
    cohort_id = auto()
    player_id = auto()
    player_type = auto()
    session_id = auto()
    stage_id = auto()
    stage_score = auto()

    @classmethod
    def names(cls):
        return list(map(lambda e: e.name, cls))

def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

