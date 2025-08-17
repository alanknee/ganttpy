"""
gantt.py: This module defines a class for creating a Gantt chart.
"""
import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_COLOR = 'tab:blue'


class Task:
    """Class representing a single task with some name, start date, 
    end date (or duration in days), and a color to be used when plotting.

    Dates must be in a format readable by pandas.to_datetime(), e.g.,
    'Sep 14, 2015' or '2015-09-14'.
    """
    def __init__(self, name, start, end=None, duration=None, color=None):
        self.name = name

        self.start = pd.to_datetime(start)
        if end is not None:
            self.end = pd.to_datetime(end)
            self.duration = self.end - self.start
        elif duration is not None:
            self.duration = pd.Timedelta(f'{duration} days')
            self.end = self.start + self.duration
        else:
            raise ValueError('Must specify either task end date or duration (in days)')

        if color:
            self.color = color
        else:
            self.color = DEFAULT_COLOR


def gantt(
    tasks, 
    begin_date=None, 
    figsize=(10, 5), 
    fname=None, 
    return_fig=False
):
    """Top-level function for making a Gantt chart. The input must be a list of Task
    objects, each containing a name, start and end dates, and optionally a colour
    for plotting. Entries are arranged from top to bottom in the order in
    which they appear in the input list.
    """
    # Check that the input is a list of Task objects
    for task in tasks:
        if not isinstance(task, Task):
            raise ValueError('Entries are not all Task objects')

    # If begin_date is given, use it as the beginning of the time axis, 
    # else use the earliest task start date
    if begin_date is None:
        start_timestamps = [task.start.timestamp() for task in tasks]
        begin_date = pd.to_datetime(min(start_timestamps), unit='s')
    else:
        begin_date = pd.to_datetime(begin_date)

    # Set up figure and add task entries one by one
    fig, ax = plt.subplots(figsize=figsize)
    for task in tasks:
        ax.barh(
            y=task.name,
            left=(task.start - begin_date).days,
            width=task.duration.days,
            color=task.color
        )
        
    if fname:
        fig.savefig(fname, dpi=400, bbox_inches='tight')

    if return_fig:
        return fig, ax
    
