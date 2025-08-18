"""
gantt.py: This module defines a class for creating a Gantt chart.
"""
import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_COLOR = 'tab:blue'


class Task:
    """Class representing a single task with some name, start date, 
    finish date (or duration in days), and a color to be used when plotting.
    """
    def __init__(
        self, 
        name,
        start,
        finish=None, 
        duration=None, 
        color=DEFAULT_COLOR
    ):
        """Initialize a Task.

        Dates must be in a format readable by pandas.to_datetime(), e.g.,
        'Sep 14, 2015' or '2015-09-14'.
        
        Args:
            name (str): Task name.
            start (str): Task start date.
            finish (str, optional): Task finish date.
            duration (float, optional): Task duration in days.
            color (str, optional): Task color.  
        """
        self.name = name

        self.start = pd.to_datetime(start)
        if finish is not None:
            self.finish = pd.to_datetime(finish)
            self.duration = self.finish - self.start
        elif duration is not None:
            self.duration = pd.Timedelta(f'{duration} days')
            self.finish = self.start + self.duration
        else:
            raise ValueError('Must specify either task finish date or duration (in days)')

        self.color = color or DEFAULT_COLOR

    def __repr__(self):
        cls = self.__class__.__name__
        return (
            f'{cls}(name={self.name}, start={self.start}, '
            f'finish={self.finish}, duration={self.duration}, color={self.color})'
        )


def gantt(
    tasks,
    order='start',
    begin_date=None, 
    figsize=(10, 4),
    figtitle=None, 
    date_freq='MS',
    date_format='%b %Y',
    date_rotation=0,
    fontsize=10,
    show_durations=False,
    duration_textcolor='w',
    fname=None, 
    return_fig=False
):
    """Top-level function for making a Gantt chart. The input must be a list of Task
    objects, each containing a name, start and end dates, and optionally a colour
    for plotting. By default, entries are arranged from top to bottom in the order in
    which they are listed.

    Args:
        tasks (list[Task]): A list of Task instances defining individual tasks.
        order (str, optional): Task order, either 'start' (default) to order by
            start time or 'listed' to go by list order.
        begin_date (str, optional): Beginning date of the time axis.
        figsize (tuple[float], optional): Figure width and height.
        figtitle (str, optional): Figure title.
        date_freq (str, optional): Date label frequency to pass to pandas.date_range().
        date_format (str, optional): Date format to pass to strftime().
        date_rotation (float, optional): Date label rotation.
        fontsize (float, optional): Tick label fontsize.
        show_durations (bool, optional): Show task durations in the plot.
        duration_textcolor (str, optional): Color of duration text.
        fname (str, optional): File path to save figure.
        return_fig (bool, optional): Return figure and axis objects. 
    """
    # Check that the input is a list of Task objects
    if not tasks:
        raise ValueError('Task list is empty')
    for task in tasks:
        if not isinstance(task, Task):
            raise ValueError('Entries are not all Task objects')

    # Task order
    if order == 'start':
        tasks = sorted(tasks, key=lambda task: task.start)
    elif order == 'listed':
        pass
    else:
        raise ValueError("Order must be either 'start' or 'listed'")

    # If begin_date is given, use it as the beginning of the time axis, 
    # else use the earliest task start date
    if begin_date is None:
        begin_date = min(task.start for task in tasks)
    else:
        begin_date = pd.to_datetime(begin_date)
    end_date = max(task.finish for task in tasks)

    # Set up figure and add task entries one by one
    fig, ax = plt.subplots(figsize=figsize)
    task_idxs = []
    task_labels = []
    # Traverse list in reverse order to plot top to bottom
    for idx, task in enumerate(reversed(tasks)):
        days_to_start = (task.start - begin_date).days
        ax.barh(
            y=idx,
            left=days_to_start,
            width=task.duration.days,
            color=task.color,
            edgecolor='k',
            linewidth=1,
        )
        task_idxs.append(idx)
        task_labels.append(task.name)

        # Print task durations
        if show_durations:
            ax.text(
                x=days_to_start+0.5, 
                y=idx, 
                s=f'{int(task.duration.days)} days',
                va='center',
                color=duration_textcolor,
                fontsize=fontsize
            )

    # Task labels
    ax.set_yticks(task_idxs)
    ax.set_yticklabels(task_labels, fontsize=fontsize)
    ax.set_title(figtitle, fontsize=fontsize)

    # Date labels
    ax.set_xlim(0, (end_date - begin_date).days)
    time_ticks = pd.date_range(start=begin_date, end=end_date, freq=date_freq)
    ax.set_xticks([(tt - begin_date).days for tt in time_ticks])
    time_labels = [tt.strftime(date_format) for tt in time_ticks]
    ax.set_xticklabels(time_labels, rotation=date_rotation, fontsize=fontsize)

    ax.grid(axis='x')
    ax.set_axisbelow(True)
        
    if fname:
        fig.savefig(fname, dpi=400, bbox_inches='tight')
    if return_fig:
        return fig, ax
    
