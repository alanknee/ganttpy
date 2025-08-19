# ganttpy

A simple Python tool for making Gantt charts.

### Instructions 

First define each of your tasks as a `ganttpy.Task` instance. Each `Task` should have a name, start and end date, and an associated plot colour. 

To make the Gantt chart, simply run `ganttpy.gantt(tasks)` where `tasks` is a list of the individual `Task` objects you want plotted. See the example in `example/example.ipynb`.

### Installation

Clone the repository to your machine and run `pip install .` in the root folder to install. You can then use it in your Python scripts as `import ganttpy as gp`.
